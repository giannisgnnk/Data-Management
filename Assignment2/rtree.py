import sys

_DIVISORS = [180.0 / 2 ** n for n in range(32)]

def interleave_latlng(lat, lng):
    if not isinstance(lat, float) or not isinstance(lng, float):
        raise ValueError("Supplied arguments must be of type float!")

    if (lng > 180):
        x = (lng % 180) + 180.0
    elif (lng < -180):
        x = (-((-lng) % 180)) + 180.0
    else:
        x = lng + 180.0

    if (lat > 90):
        y = (lat % 90) + 90.0
    elif (lat < -90):
        y = (-((-lat) % 90)) + 90.0
    else:
        y = lat + 90.0

    morton_code = ""
    for dx in _DIVISORS:
        digit = 0
        if (y >= dx):
            digit |= 2
            y -= dx
        if (x >= dx):
            digit |= 1
            x -= dx
        morton_code += str(digit)

    return morton_code

def read_data(coords_file, offsets_file):
    #read the coordinates from coords.txt
    with open(coords_file, 'r') as cf:
        coords = []
        for line in cf:
            x, y = map(float, line.strip().split(','))
            coords.append((x, y))

    objects = []

    #read each object from offsets.txt
    with open(offsets_file, 'r') as of:
        for line in of:
            id, start, end = map(int, line.strip().split(','))

            #find the points of the object from coords list
            points = coords[start:end + 1]

            #find the boundaries for the MBR
            x_values = [p[0] for p in points]
            y_values = [p[1] for p in points]
            xmin = min(x_values)
            xmax = max(x_values)
            ymin = min(y_values)
            ymax = max(y_values)
            mbr = [xmin, xmax, ymin, ymax]

            #calculate the center of MBR and z-order value
            center_x = (xmin + xmax) / 2
            center_y = (ymin + ymax) / 2
            z_value = interleave_latlng(center_y, center_x) 


            objects.append({'id': id, 'mbr': mbr, 'z': z_value})

    return objects


def build_rtree(objects):

    #sort the objects returned from read_data function by the z-value field
    objects.sort(key=lambda x: x['z'])

    node_id_counter = [0]
    levels = {}

    entries = objects
    is_leaf = True

    while True:
        isnonleaf = 0 if is_leaf else 1 #check if the node is leaf or not and put the correct value
        current_level = []
        i = 0

        while i < len(entries):
            group = entries[i:i+20] #split the entries in a group of 20 

            #if the group has less than 8 entries and there are more than 8 entries still available 
            if len(group) < 8 and len(entries[i:]) > 8:
                diff = 8 - len(group) #calculate how many are needed in order the group to have >=8 entries
                group = entries[i:i+20+diff] #then take a bigger range of entries
                i += 20 + diff #update the i counter to go to the next group
            else:
                i += 20

            node_id = node_id_counter[0] #create the node id
            node_id_counter[0] += 1 #update the counter to the next node 

            #list with all the mbrs of the group 
            mbrs = [e['mbr'] for e in group]
            x_min = min(m[0] for m in mbrs)
            x_max = max(m[1] for m in mbrs)
            y_min = min(m[2] for m in mbrs)
            y_max = max(m[3] for m in mbrs)
            mbr = [x_min, x_max, y_min, y_max]

            #node creation
            current_level.append({
                'isnonleaf': isnonleaf,
                'node_id': node_id,
                'entries': [[e['id'], e['mbr']] for e in group],
                'mbr': mbr
            })

        level_num = len(levels)

        #if the level being processed isnt in levels dict, then create a new list to store it 
        if level_num not in levels:
            levels[level_num] = []
        levels[level_num].extend(current_level)

        #if that level has only 1 node, it is the root, so break the recursive run 
        if len(current_level) == 1:
            break

        #otherwise continue the loop with the new entries (the children)
        else:
            entries = [{'id': node['node_id'], 'mbr': node['mbr']} for node in current_level]
            is_leaf = False

    return levels #at the end of build_rtree return the final levels dict



def write_rtree(levels, output_file):
    with open(output_file, 'w') as f:
        all_nodes = []
        #sorting the levels and iterating in a for-loop starting from level 0
        for lvl in sorted(levels):
            #iterating through each node of the level
            for node in levels[lvl]:
                line = [node['isnonleaf'], node['node_id'], node['entries']]
                all_nodes.append((node['node_id'], line)) #add a pair  of node_id and the line above in the final list
        all_nodes.sort() #sort the final list based on node_id 

        #iterate through the final sorted list and write each node in the output file
        for item in all_nodes:
            line = item[1] #take only the line from the pair (node_id,line)
            f.write(str(line) + "\n") #write this line to the output file


    #print node count per level
    for lvl in sorted(levels):
        count = len(levels[lvl])
        label = "node" if count == 1 else "nodes"
        print(str(count) + " " + label + " at level " + str(lvl))


#read the arguments from the cmd
coords_path = sys.argv[1] 
offsets_path = sys.argv[2]

objects = read_data(coords_path, offsets_path)
levels = build_rtree(objects)
write_rtree(levels, "Rtree.txt")