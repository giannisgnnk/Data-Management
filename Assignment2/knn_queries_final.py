#Ioannis Giannakos 4970
import sys
import heapq

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
    
#func to extract the x,y points in the desired format
def load_points(nnqueries_file):
    points = []
    with open(nnqueries_file, 'r') as f:
        for line in f:
            x, y = map(float, line.split())
            points.append((x, y))
    return points

#func to calculate the euclidean distance between the point and the rectangle 
def calculate_distance(point, mbr):
    x, y = point
    x_low, x_high, y_low, y_high = mbr

    #calculate for x-axis
    if x < x_low:
        dx = x_low - x
    elif x > x_high:
        dx = x - x_high
    else:
        dx = 0

    #calculate for y-axis
    if y < y_low:
        dy = y_low - y
    elif y > y_high:
        dy = y - y_high
    else:
        dy = 0


    return (dx**2 + dy**2)**0.5

#func to implement the best first search for NN
def best_first_search(root_id, query_point, k, nodes):
    Q = []
    results = []

    #start from root
    root = nodes[root_id]
    isnonleaf, _, entries = root

    #push root's children and their distance from query_point
    for child_id, mbr  in entries:
        distance = calculate_distance(query_point, mbr)
        heapq.heappush(Q, (distance, isnonleaf, child_id, mbr)) 

    #as long as we haven't found k results loop
    while Q and len(results) < k:
        distance, isnonleaf, id_or_obj, mbr = heapq.heappop(Q) #take from the heap the entry with the shorter distance (in the top)

        if isnonleaf == 0 and id_or_obj in nodes:
            #leaf node - it is an object, so take the object mbr's
            node = nodes[id_or_obj]  
            _, _, object_entries = node
            
            #for every object take the id and mbr and calculate their distance from query point
            for obj_id, obj_mbr in object_entries:
                distance = calculate_distance(query_point, obj_mbr)
                heapq.heappush(Q, (distance, -1, obj_id, obj_mbr))
        
        elif isnonleaf > 0:
            #it is an internal node, so expand it
            node = nodes[id_or_obj]
            isnonleaf, _, child_entries = node

            #for every child, take the id and mbr and calculate their distance from query poitn
            for child_id, child_mbr in child_entries:
                distance = calculate_distance(query_point, child_mbr)
                heapq.heappush(Q, (distance, isnonleaf, child_id, child_mbr))
        
        #if we have examine all the nodes add the id to the final list 
        else:
            results.append(id_or_obj)


    return results


#take the arguments from the cmd
Rtree_file = sys.argv[1]
NNqueries_file = sys.argv[2]
k = int(sys.argv[3])

nodes = load_rtree(Rtree_file)
root_id = find_root(Rtree_file)
queries = load_points(NNqueries_file)


for i, query_point in enumerate(queries):
    neighbors = best_first_search(root_id, query_point, k, nodes)
    print(str(i) + ": " + ",".join(map(str, neighbors)))

