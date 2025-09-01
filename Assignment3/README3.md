# Assignment: Containment Queries on Transaction Data

You will use the `transactions.txt` dataset file.  

- Each line contains an (unordered) set of **item identifiers**.  
- Each line is considered a **transaction** by a customer.  
- A transaction may contain **duplicate items** (bag semantics).  
  - Example: In line 5, item `4` appears three times.  
- Transaction IDs correspond to line numbers: first line → ID `0`, second line → ID `1`, etc.

---

## Part 1: Containment Queries

Write a program that **reads the transactions** and constructs structures to evaluate **containment queries**.  

- Transactions are treated as **sets** (set semantics).  
- Queries are sets of items.  
- Goal: Find transactions that **contain all items** in the query.  

Example:  
- Transaction ID `4` (5th line) is a result for query `q = {2,4,16}` because it contains all three items.

---

### Implementation Steps

1. **Read transactions** and store them in memory as a **table or list**, where each record contains the set of items.  

2. Implement the following **methods**:

#### a) Simple (Naïve) Reference Method
- For each query, scan all transactions.  
- If a transaction contains all query items, add its ID to the results.  
- Return the results at the end.

#### b) Exact Signature File
- Create a **sigfile table** with the same size as the transactions table.  
- For each transaction:
  - Create a **bitmap**: least significant bit → item 0, second bit → item 1, etc.  
  - Set bits for items present in the transaction.  
  - Example: Transaction `{0,1,5}` → bitmap `100011` → number `35`.  
- Store the bitmap in the sigfile table.  
- Containment query evaluation:
  - Convert the query to a bitmap.  
  - Traverse the sigfile table: if all 1-bits of the query are set in a transaction, include its ID in the results.  
  - Use **bitwise operations** for checks.  
- Output: `sigfile.txt`, one line per transaction ID.

#### c) Exact Bitslice Signature File
- Create a **bitslice structure**: for each item, a bitmap where:
  - Least significant bit → transaction 0, second bit → transaction 1, etc.  
  - Example: Item `165` appears in transactions 7379 and 8930 → bitmap = `27379 + 28930`.  
- Containment query evaluation:
  - Calculate **logical AND** of bitmaps of query items.  
  - IDs corresponding to 1-bits → result transactions.  
- Output: `bitslice.txt`, one line per item.

#### d) Inverted File
- For each item, create a **list of transaction IDs** containing that item.  
- Containment query evaluation:
  - Calculate **intersection** of the lists corresponding to query items using a **merge algorithm**.  
  - IDs in the intersection → result transactions.  
- Output: `invfile.txt`, one line per item with transaction IDs in **reversed order**.

---

### Program Parameters

Your program must take the following **command-line parameters**:
```
<transactions file> <queries file> <qnum> <method>
```

- `<transactions file>` → e.g., `transactions.txt`  
- `<queries file>` → e.g., `queries.txt`  
- `<qnum>` → query ID to execute (`-1` for all queries)  
- `<method>` → method to run:  
  - `-1` = all  
  - `0` = naïve  
  - `1` = exact signature file  
  - `2` = exact bitslice signature file  
  - `3` = inverted file  

- Measure **execution time** for each method.  
- Display **results** only if executing a specific query.

---

### Example Executions
```
<program> transactions.txt queries.txt 0 0
Naive Method result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227,
5523, 2454, 4854, 9752, 7641}
Naive Method computation time = ***

<program> transactions.txt queries.txt 0 -1
Naive Method result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227,
5523, 2454, 4854, 9752, 7641}
Naive Method computation time = ***
Signature File result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227,
5523, 2454, 4854, 9752, 7641}
Signature File computation time = ***
Bitsliced Signature File result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 2227,
5523, 2454, 4854, 9752, 7641}
Bitsliced Signature File computation time = ***
Inverted File result:
{322, 5923, 6596, 8131, 8838, 1258, 77, 7182, 2063, 2289, 9650, 5523,
2227, 2454, 4854, 9752, 7641}
Inverted File Computation time = ***

<program> transactions.txt queries.txt -1 -1
Naive Method computation time = ***
Signature File computation time = ***
Bitsliced Signature File computation time = ***
Inverted File Computation time = ***
```

---

## Part 2: Relevance Queries

Write a program that reads data from the transactions file and constructs an **inverted file structure** for **relevance queries**.

---

### Goal

- Consider:
  1. An object may appear **multiple times** in a transaction.  
  2. The **rarity of objects**.  

- Let `T` be the set of transactions and `|T|` its cardinality.  
- For a transaction `τ ∈ T` and a query `q` consisting of a set of objects, the **relevance** is defined as:

\[
rel(τ,q) = \sum_{i \in q} \big( occ(i,τ) \cdot \frac{|T|}{trf(i,T)} \big)
\]

Where:  
- `occ(i,τ)` → number of times object `i` appears in transaction `τ`  
- `trf(i,T)` → number of transactions in `T` that contain object `i`

- Goal: Calculate transactions `τ` with `rel(τ,q) > 0`, **sorted descending** by `rel(τ,q)`.

---

### Inverted File Structure

1. Each inverted list for object `i` contains **pairs `(τ, occ(i,τ))`**, sorted by transaction ID.  
2. Maintain a second structure storing **|T| / trf(i,T)** for each object.  

---

### Query Evaluation

- For a query:
  1. **Union** the lists corresponding to query items (merge algorithm).  
  2. Calculate `rel(τ,q)` for each transaction in the union.  
  3. **Sort results** by `rel(τ,q)` and return the top `k` results (or all if fewer than `k`).  

- Output file: `invfileocc.txt`  
  - Each line: `|T|/trf(i,T)` followed by the reversed list of `[τ, occ(i,τ)]`.  
  - Example:
```
  0: 2.515090543259557, [[4, 2], [6, 3], [7, 1], [8, 2], ..., [9999, 1]]
  1: 2.6602819898909282, [[2, 1], [5, 1], [6, 1], [12, 3], ..., [9999, 1]]
  ...
```


---

### Naïve Reference Method

- For each query, read transactions from memory and calculate `rel(τ,q)` for each transaction.  
- Uses the second structure (`|T| / trf(i,T)`) but **does not** use the inverted file.

---

### Program Parameters
```
<transactions file> <queries file> <qnum> <method> <k>
```


- `<transactions file>` → e.g., `transactions.txt`  
- `<queries file>` → e.g., `queries.txt`  
- `<qnum>` → query ID to execute (`-1` for all queries)  
- `<method>` → method to run:  
  - `-1` = all  
  - `0` = naïve  
  - `1` = inverted file  
- `<k>` → number of most relevant results to return  

- Measure **execution time** for each method.  
- Display **results** as `[rel(τ,q), τ]` sorted by `rel(τ,q)` for a specific query.  

---

### Example Executions
```
<program> transactions.txt queries.txt 0 -1 2
Naive Method result:
[[263.1578947368421, 8346], [145.0651240373354, 7641]]
Naive Method computation time = ***
Inverted File result:
[[263.1578947368421, 8346], [145.0651240373354, 7641]]
Inverted File computation time = ***

<program> transactions.txt queries.txt -1 -1 10
Naive Method computation time = ***
Inverted File computation time = ***
```
