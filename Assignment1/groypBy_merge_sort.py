#Ioannis Giannakos 4970

def merge_sort(data):
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i][0] <= right[j][0]:  # compare keys
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append remaining items
    result.extend(left[i:])
    result.extend(right[j:])
    return result




def R_groupBY(R_file, RgroupBy_file):

    with open(R_file, 'r') as r_f, open(RgroupBy_file, 'w') as out_f:

        r_line = r_f.readline() #read the first line of R file  
        buffer = []
        last_written = None #var to check in case we already written this tuple 
        res = []
        processed_keys = []

        while r_line:

            if r_line:
                r_parts = r_line.strip().split('\t')
                r_key = r_parts[0]
                r_value = r_parts[1]
                r_tuple = (r_key, r_value)
            else:
                r_tuple = None


            if r_tuple is not None:
                if r_tuple != last_written:
                    buffer.append(r_tuple)
                    last_written = r_tuple 
                    r_line = r_f.readline()
                else:
                    r_line = r_f.readline()

        #double loop the buffer list 
        for ikey, ivalue in buffer:
            if ikey in processed_keys:
                continue  #skip duplicates

            total = 0 
            for jkey, jvalue in reversed(buffer):
                jvalue = int(jvalue)
                if ikey == jkey:
                    total = sum([total, int(jvalue)])  
        
            res.append((ikey, total))
            processed_keys.append(ikey)

        res = merge_sort(res)
        for key, value in res:
            value = str(value)
            out_f.write(key + "\t" + value + "\n")



R_file = "C:/Users/ggian/Desktop/Data_Management/R.tsv"
RgroupBy_file = "C:/Users/ggian/Desktop/Data_Management/RgroupBy.tsv"

R_groupBY(R_file, RgroupBy_file)


            