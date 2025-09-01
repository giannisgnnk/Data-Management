# Ioannis Giannakos 4970

def merge_join(r_sorted_file, s_sorted_file, RjoinS_file):
    with open(r_sorted_file, 'r') as r_f, open(s_sorted_file, 'r') as s_f, open(RjoinS_file, 'w') as out_f:

        r_line = r_f.readline()
        s_line = s_f.readline()

        s_buffer = []
        checked_s_key = None
        max_buffer_size = 0

        #read the R file line by line  
        while r_line:
            r_parts = r_line.strip().split('\t')
            r_key = r_parts[0]
            r_value = r_parts[1]

            #if R key has changed, clear and fill the buffer again 
            if checked_s_key != r_key:
                s_buffer = []

                #read the S file line by line  
                while s_line:
                    s_parts = s_line.strip().split('\t')
                    s_key = s_parts[0]
                    s_value = s_parts[1]

                    if s_key < r_key:
                        s_line = s_f.readline()  
                    elif s_key == r_key:
                        s_buffer.append(s_value)
                        s_line = s_f.readline() 
                    else:
                        break  #we reached to an S key bigger than R key, so stop

                checked_s_key = r_key  #remember the last key we checked
                max_buffer_size = max(max_buffer_size, len(s_buffer))

            #if there are matches, write them to the output file 
            for s_val in s_buffer:
                out_f.write(f"{r_key}\t{r_value}\t{s_val}\n")

            r_line = r_f.readline()

    print(f"Max buffer size: {max_buffer_size}")



R_file = "C:/Users/ggian/Desktop/Data_Management/R_sorted.tsv"
S_file = "C:/Users/ggian/Desktop/Data_Management/S_sorted.tsv"
RjoinS_file = "C:/Users/ggian/Desktop/Data_Management/RjoinS.tsv"

merge_join(R_file, S_file, RjoinS_file)
