#Ioannis Giannakos 4970

import sys 
import time 

def read_file(file):
    transactions = []
    with open(file, 'r') as tf:
        for line in tf:
            item = eval(line.strip())
            transactions.append(set(item))
    return transactions



def naive_method(queries_list, transactions_lst, qnum):
    results =[]
    
    #qnum==-1 then run all the queries
    if qnum == -1:
        queries_to_run = queries_list
    #otherwise only the selected one 
    else:
        queries_to_run = [queries_list[qnum]]

    for query in queries_to_run:
        query_set = set(query)
        match_ids = [] #id of the transactions that contain the query

        for tid, transaction in enumerate(transactions_lst):
            if query_set.issubset(transaction): 
                match_ids.append(tid)

        results.append(set(match_ids))
    return results




def compute_bitmap(itemset):
    bitmap = 0
    for item in itemset:
        bitmap = bitmap | (1 << item) #move the '1' value left by item positions
    return bitmap

def build_signature_file(transactions_lst):
    sigfile = []
    with open("sigfile.txt", 'w') as sf:
        for transaction in transactions_lst:
            signature = compute_bitmap(transaction)
            sigfile.append(signature)
            sf.write(f"{signature}\n")
    return sigfile

def exact_signature_file(queries_list, sigfile, qnum):
    results = []

    if qnum == -1:
        queries_to_run = queries_list
    else:
        queries_to_run = [queries_list[qnum]]

    for query in queries_to_run:
        query_set = set(query)
        query_sig = compute_bitmap(query_set)
        match_ids = []

        for tid, transaction_sig in enumerate(sigfile):
            #turn to '1' only the values that are '1' in the 2 bitmaps
            #if the result of the AND operation is the same as the query sig then all the query items are in the transacion
            if (query_sig & transaction_sig) == query_sig:
                match_ids.append(tid)

        results.append(set(match_ids))

    return results




#for each value [0-243 example for transactions.txt] turns '1' in the trans_id that exists 
def build_bitslice(transactions_lst):
    bitslices = {} #store as key = item and value = bitmap 

    for tid, transaction in enumerate(transactions_lst):
        for item in transaction:
            if item not in bitslices:
                bitslices[item] = 0
                
            bitslices[item] = bitslices[item] | (1 << tid)

    with open("bitslice.txt", 'w') as bf:
        for item in sorted(bitslices):
            bf.write(f"{item}: {bitslices[item]}\n")

    return bitslices

def exact_bitslice_signature_file(queries_lst, bitslices, qnum, num_transactions):
    results = []

    if qnum == -1:
        queries_to_run = queries_lst
    else:
        queries_to_run = [queries_lst[qnum]]

    for query in queries_to_run:
        #we start by saying that all the transactions satisfy the query
        bitmap = (1 << num_transactions) - 1
 
        #for every value in the query
        #we remove with the bitslice all those that dont contain the item from the query 
        for item in query:
            if item in bitslices:
                bitmap &= bitslices[item]
            else:
                bitmap = 0  
                break

        #check the pos where bit is '1'
        matching_transactions = []
        #for every trans_id we check if the corresponding bit in the bitmap is 1
        #and if that happens we add it to the final list with the matching trans_ids
        for tid in range(num_transactions):
            if (bitmap >> tid) & 1:
                matching_transactions.append(tid)

        results.append(set(matching_transactions))

    return results




def build_inverted_file(transactions_lst):
    inverted_file = {}
    for tid, transaction in enumerate(transactions_lst):
        for item in transaction:
            if item not in inverted_file:
                inverted_file[item] = []
            inverted_file[item].append(tid)
    
    with open('invfile.txt', 'w') as invf:
        for item in sorted(inverted_file.keys()):
            invf.write(f"{item}: {inverted_file[item]}\n")

    return inverted_file

def intersect_sorted_lists(lists):
    if not lists:
        return set()
    if len(lists) == 1:
        return set(lists[0])
    
    #start from the first list 
    result = lists[0]

    #start from the second list
    for lst in lists[1:]:
        i, j = 0, 0
        merged = []

        #iterate through every sub-list and compare the items to find the intersection
        while i < len(result) and j < len(lst):
            if result[i] == lst[j]:
                merged.append(result[i])
                i += 1
                j += 1
            elif result[i] < lst[j]:
                i += 1
            else:
                j += 1

        result = merged

        if not result:
            break  #if intersection is empty, stop earlier

    return set(result)

def inverted_file_query(queries_lst, inverted_file, qnum):
    results = []

    if qnum == -1:
        queries_to_run = queries_lst
    else:
        queries_to_run = [queries_lst[qnum]]

    for query in queries_to_run:
        lists = []
        for item in query:
            if item in inverted_file:
                lists.append(inverted_file[item])
            else:
                lists = []
                break
        
        if lists:
            matching_transactions = intersect_sorted_lists(lists)
        else:
            matching_transactions = set()

        results.append(matching_transactions)

    return results




def main():
    transaction_file = sys.argv[1]
    queries_file = sys.argv[2]
    qnum = int(sys.argv[3])
    method = int(sys.argv[4])

    transactions_lst = read_file(transaction_file)
    queries_lst = read_file(queries_file)

    if method == 0:
        start_time = time.time()
        method = naive_method(queries_lst, transactions_lst, qnum)
        end_time = time.time()
        elapsed = end_time - start_time
        if qnum != -1:
            print("Naive Method result:")
            for i in method:
                print(i)
        print("Naive Method computation time = ", elapsed)

    elif method == 1:
        start_time = time.time()
        sigfile = build_signature_file(transactions_lst)
        method = exact_signature_file(queries_lst, sigfile, qnum)
        end_time = time.time()
        elapsed = end_time - start_time
        if qnum != -1:
            print("Signature File result:")
            for i in method:
                print(i)
        print("Signature File computation time = ", elapsed)
    
    elif method == 2:
        bitslices = build_bitslice(transactions_lst)
        start_time = time.time()
        method = exact_bitslice_signature_file(queries_lst, bitslices, qnum, len(transactions_lst))
        end_time = time.time()
        elapsed = end_time - start_time
        if qnum != -1:
            print("Bitsliced Signature File result:")
            for i in method:
                print(i)
        print("Bitsliced Signature File computation time = ", elapsed)

    elif method == 3:
        inverted_file = build_inverted_file(transactions_lst)
        start_time = time.time()
        method = inverted_file_query(queries_lst, inverted_file, qnum)
        end_time = time.time()
        elapsed = end_time - start_time
        if qnum != -1:
            print("Inverted File result:")
            for i in method:
                print(i)
        print("Inverted File computation time = ", elapsed)
    
    elif method == -1:
        start_time_naive = time.time()
        method = naive_method(queries_lst, transactions_lst, qnum)
        end_time_naive = time.time()
        elapsed_naive = end_time_naive - start_time_naive
        if qnum != -1:
            print("Naive Method result:")
            for i in method:
                print(i)
        print("Naive Method computation time = ", elapsed_naive)

        start_time_signature = time.time()
        sigfile = build_signature_file(transactions_lst)
        method = exact_signature_file(queries_lst, sigfile, qnum)
        end_time_signature = time.time()
        elapsed_signature = end_time_signature - start_time_signature
        if qnum != -1:
            print("Signature File result:")
            for i in method:
                print(i)
        print("Signature File computation time = ", elapsed_signature)

        bitslices = build_bitslice(transactions_lst)
        start_time_bitsliced = time.time()
        method = exact_bitslice_signature_file(queries_lst, bitslices, qnum, len(transactions_lst))
        end_time_bitsliced = time.time()
        elapsed_bitsliced = end_time_bitsliced - start_time_bitsliced
        if qnum != -1:
            print("Bitsliced Signature File result:")
            for i in method:
                print(i)
        print("Bitsliced Signature File computation time = ", elapsed_bitsliced)

        inverted_file = build_inverted_file(transactions_lst)
        start_time_inverted = time.time()
        method = inverted_file_query(queries_lst, inverted_file, qnum)
        end_time_inverted = time.time()
        elapsed_inverted = end_time_inverted - start_time_inverted
        if qnum != -1:
            print("Inverted File result:")
            for i in method:
                print(i)
        print("Inverted File computation time = ", elapsed_inverted)
       

main()