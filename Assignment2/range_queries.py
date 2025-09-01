import sys

#func to store the Rtree in a dictionary 
def load_rtree(rtree_file):
    nodes = {} #dict 
    with open(rtree_file, 'r') as f:
        for line in f:
            node = eval(line) #eval converts the text from the line to the desired python object
            nodes[node[1]] = node #stores the node_id as a key and the rest of the line as value  
    return nodes


#func to find the root id 
def find_root(rtree_file):
    with open(rtree_file, 'r') as f:
        lines = f.readlines()
        last_line = lines[-1]
        node = eval(last_line)
        return node[1]
    

#func to extract the mbr from the W rectangle in the desired format
def load_WRectangle(rqueries_file):
    with open(rqueries_file, 'r') as f:
        rectangle_lst = []
        for line in f:
            x_low, y_low, x_high, y_high = map(float, line.split())
            rectangle_lst.append([x_low, x_high, y_low, y_high])
        return rectangle_lst


#func to check if the rectangles have an intersection 
def rectangles_intersect(mbr, w):
    mbr_x_low, mbr_x_high, mbr_y_low, mbr_y_high = mbr
    w_x_low, w_x_high, w_y_low, w_y_high = w

    x_overlap = (mbr_x_low <= w_x_high) and (w_x_low <= mbr_x_high)
    y_overlap = (mbr_y_low <= w_y_high) and (w_y_low <= mbr_y_high)

    return x_overlap and y_overlap


#func to find the intersection of the 2 rectangles
def find_intersection(nodeid, W_rectangle):
    result = [] #list to save the id's of the objects intersecting w rect
    nonleaf, node_id, entries = nodes[nodeid] #from dict nodes the data of the node with id=nodeid

    for entry in entries:
        child_id, mbr = entry
        if rectangles_intersect(mbr, W_rectangle):
            if nonleaf == 0:
                #leaf node, so add object id
                result.append(child_id)
            else:
                #internal node, so do a recursive call
                result.extend(find_intersection(child_id, W_rectangle))
    
    return result



#take the arguments from the cmd
Rtree_file = sys.argv[1]
Rqueries_file = sys.argv[2]

# Load everything
nodes = load_rtree(Rtree_file)
root_id = find_root(Rtree_file)
queries = load_WRectangle(Rqueries_file)

for i, query in enumerate(queries):
    matches = find_intersection(root_id, query)
    print(str(i) + " (" + str(len(matches)) + "): " + ",".join(map(str, matches)))
