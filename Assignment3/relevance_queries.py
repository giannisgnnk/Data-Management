#Ioannis Giannakos 4970

import sys
import time


def read_file(file):
    transactions = []
    with open(file, 'r') as tf:
        for line in tf:
            item = eval(line.strip())
            transactions.append(item)
    return transactions


def build_inverted_index(transactions):
    inv_index = {}
    trf = {}

    for tid, transaction in enumerate(transactions):
        occ_count = {}
        #count how many times each item of the transaction is shown
        #store in the dict occ_count as key=item and as value=frequency
        for item in transaction:
            if item in occ_count:
                occ_count[item] += 1
            else:
                occ_count[item] = 1

        for item, occ in occ_count.items():

            #store in the inv_index as key=item and as value=[transaction_id, frequency of this item in that trans]
            if item not in inv_index:
                inv_index[item] = []
            inv_index[item].append([tid, occ]) 

            #store in the trf as key=item and as value=in how many different transactions it appears
            if item in trf:
                trf[item] += 1
            else:
                trf[item] = 1

    total_transactions = len(transactions)
    weights = {}
    for item, freq in trf.items():
        weights[item] = total_transactions / freq


    with open("invfileocc.txt", "w") as f:
        for item in sorted(inv_index.keys()):
            f.write(f"{item}: {weights[item]}, {inv_index[item]}\n")

    return inv_index, weights


def compute_relevance_naive(transactions_lst, queries_list, weights, qnum, k):
    results = []

    if qnum == -1:
        queries_to_run = queries_list
    else:
        queries_to_run = [queries_list[qnum]]

    for query in queries_to_run:
        query_results = []
        for tid, transaction in enumerate(transactions_lst):
            rel = 0.0
            for item in query:
                occ = transaction.count(item)
                if occ > 0 and item in weights:
                    rel += occ * weights[item]
            if rel > 0:
                query_results.append([rel, tid])
        query_results.sort(reverse=True) #sort descending by rel 

        results.append(query_results[:k]) #add and return the top k results

    return results


def compute_relevance_inverted(queries_list, inv_index, weights, qnum, k):
    results = []
    if qnum == -1:
        queries_to_run = queries_list
    else:
        queries_to_run = [queries_list[qnum]]

    for query in queries_to_run:
        rel_scores = {}
        query_results = []
        for item in query:
            if item in inv_index:
                for tid, occ in inv_index[item]:
                    if tid not in rel_scores:
                        rel_scores[tid] = 0.0
                    rel_scores[tid] += occ * weights[item]

        for tid, rel in rel_scores.items():
            if rel > 0:
                query_results.append([rel, tid])

        query_results.sort(reverse=True)

        results.append(query_results[:k]) #add and return the top k results

    return results


def main():
   
    transactions_file = sys.argv[1]
    queries_file = sys.argv[2]
    qnum = int(sys.argv[3])
    method = int(sys.argv[4])
    k = int(sys.argv[5])

    transactions = read_file(transactions_file)
    queries = read_file(queries_file)
    inv_index, weights = build_inverted_index(transactions)

    if method == 0:
        start_naive = time.time()
        method = compute_relevance_naive(transactions, queries, weights, qnum, k)
        end_naive = time.time()
        elapsed_naive = end_naive - start_naive
        if qnum != -1:
            print("Naive Method result:")
            for i in method:
                print(i)
        print("Naive Method computation time = ", elapsed_naive)

    elif method == 1:
        start_inverted = time.time()
        method = compute_relevance_inverted(queries, inv_index, weights, qnum, k)
        end_inverted = time.time()
        elapsed_inverted = end_inverted - start_inverted
        if qnum != -1:
            print("Inverted File result:")
            for i in method:
                print(i)
        print("Inverted File computation time = ", elapsed_inverted)

    elif method == -1:
        start_naive = time.time()
        method = compute_relevance_naive(transactions, queries, weights, qnum, k)
        end_naive = time.time()
        elapsed_naive = end_naive - start_naive
        if qnum != -1:
            print("Naive Method result:")
            for i in method:
                print(i)
        print("Naive Method computation time = ", elapsed_naive)

        start_inverted = time.time()
        method = compute_relevance_inverted(queries, inv_index, weights, qnum, k)
        end_inverted = time.time()
        elapsed_inverted = end_inverted - start_inverted
        if qnum != -1:
            print("Inverted File result:")
            for i in method:
                print(i)
        print("Inverted File computation time = ", elapsed_inverted)


main()
