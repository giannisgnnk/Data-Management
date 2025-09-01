#Ioannis Giannakos 4970

def intersection_merge_join(r_sorted_file, s_sorted_file, RintersectionS_file):
    with open(r_sorted_file, 'r') as r_f, open(s_sorted_file, 'r') as s_f, open(RintersectionS_file, 'w') as out_f:

        r_line = r_f.readline() #read the first line of R file  
        s_line = s_f.readline() #read the first line of R file
        last_written = None #var to check in case we already written this tuple 

        while r_line and s_line:

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

            #check if the tuples from the 2 files are equal
            if r_tuple == s_tuple:
                #check if that tuple has been written before 
                if r_tuple != last_written:
                    out_f.write(r_tuple[0] + "\t" + r_tuple[1] + "\n")
                    last_written = r_tuple
                
                #go to the next line of the 2 files 
                r_line = r_f.readline()
                s_line = s_f.readline()

            #if the tuples dont match, then compare the tuples in lexicographical order
            elif r_tuple < s_tuple:
                r_line = r_f.readline()
            else:
                s_line = s_f.readline()
            


R_file = "C:/Users/ggian/Desktop/Data_Management/R_sorted.tsv"
S_file = "C:/Users/ggian/Desktop/Data_Management/S_sorted.tsv"
RintersectionS_file = "C:/Users/ggian/Desktop/Data_Management/RintersectionS.tsv"

intersection_merge_join(R_file, S_file, RintersectionS_file)