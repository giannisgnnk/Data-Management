#Ioannis Giannakos 4970

def difference_merge_join(r_sorted_file, s_sorted_file, RdifferenceS_file):
    with open(r_sorted_file, 'r') as r_f, open(s_sorted_file, 'r') as s_f, open(RdifferenceS_file, 'w') as out_f:

        r_line = r_f.readline() #read the first line of R file  
        s_line = s_f.readline() #read the first line of R file
        last_written = None #var to check in case we already written this tuple 

        while r_line:

            #split the files in 2 parts, key and value 
            if r_line:
                r_parts = r_line.strip().split('\t')
                r_key = r_parts[0]
                r_value = r_parts[1]
                r_tuple = (r_key, r_value)
            else:
                r_tuple = None
            
            if s_line:
                s_parts = s_line.strip().split('\t')
                s_key = s_parts[0]
                s_value = s_parts[1]
                s_tuple = (s_key, s_value)
            else:
                s_tuple = None

             # if S is finished, write the rest of R
            if not s_line:
                if r_tuple != last_written:
                    out_f.write(r_tuple[0] + "\t" + r_tuple[1] + "\n")
                    last_written = r_tuple

                r_line = r_f.readline()

            #if the tuples match, don't write it to the output file, because it is present in S 
            if r_tuple == s_tuple:

                r_line = r_f.readline()
                s_line = s_f.readline()

            #if the r_tuple is before the s_tuple write it, beacuse it is present in R and not in S 
            elif r_tuple < s_tuple:
                if r_tuple != last_written:
                    out_f.write(r_tuple[0] + "\t" + r_tuple[1] + "\n")
                    last_written = r_tuple

                r_line = r_f.readline()
                
            #else go to the next lines of the s file
            else:
                s_line = s_f.readline()


R_file = "C:/Users/ggian/Desktop/Data_Management/R_sorted.tsv"
S_file = "C:/Users/ggian/Desktop/Data_Management/S_sorted.tsv"
RdifferenceS_file = "C:/Users/ggian/Desktop/Data_Management/RdifferenceS.tsv"

difference_merge_join(R_file, S_file, RdifferenceS_file)