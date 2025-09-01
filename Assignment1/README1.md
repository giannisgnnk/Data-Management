# Assignment: Set Operators and Merge-Join

The aim of this assignment is to develop programs for evaluating **union**, **intersection**, **difference**, and **union** operators.

We will use **synthetic data** provided.  
The data can be found in the following files:

- `R.tsv`
- `R_sorted.tsv`
- `S_sorted.tsv`

These files can be viewed as **relational tables** with two fields:
- `A` → 2-character alphanumeric
- `B` → integer  

Each line in each file corresponds to a tuple, where the values of `A` and `B` are separated by a **tab**.  

- The file `R_sorted.tsv` contains the same tuples as `R.tsv`, but sorted.  
- The file `S_sorted.tsv` contains the tuples of a relation `S`, also sorted.  

⚠️ **Note:** Tuples are **not unique** in each file (bag semantics). A tuple can occur more than once.  
Make sure you open the files and understand their contents before proceeding.

---

## Part 1: Merge-Join

Write a program that reads the files `R_sorted.tsv` and `S_sorted.tsv` and calculates the **join of R and S**, considering that they have only their **first field** in common.  

The result should be written to a file `RjoinS.tsv`.

### Example
- Input tuples:  
  - From `R_sorted.tsv`: `('aa', 33)`  
  - From `S_sorted.tsv`: `('aa', 45)`  

- Output tuple:  
    aa 33 45

The output tuples are written to RjoinS.tsv separated by tabs, for example:
```
  ab 33 45 
  ab 33 48 
  ab 90 45.
```

---

## 🔑 Merge-Join Algorithm Requirements

Your program must **faithfully implement the merge-join algorithm**:

1. **Single-pass reading:**  
   - Each of the files `R_sorted.tsv` and `S_sorted.tsv` must be read **only once**.  

2. **No full in-memory storage:**  
   - You are **not allowed** to read all lines into tables/lists and then compute the join afterwards.  
   - For each line read, you must immediately handle join matches.  

3. **Buffer for matching tuples:**  
   - The only permitted in-memory storage is a **buffer** that temporarily holds the lines from **S** that match the current line of **R**.  
   - This ensures that if the **next line in R** has the same join field value, you can reuse the matching lines from **S** without rereading them.  

4. **Buffer size reporting:**  
   - At the end of the program, print the **maximum size** of this buffer (in lines).  

---


## Part 2: Union

Write a program that reads the files `R_sorted.tsv` and `S_sorted.tsv` and calculates the **union of R and S**, writing the result to a file `RunionS.tsv`, assuming that they have exactly the same fields.  

### Requirements
- The program must:
  1. Read the lines of the files `R_sorted.tsv` and `S_sorted.tsv` **only once**.  
  2. At the same time, calculate their **union** and write the tuples of the union to the output file.  
  3. Implement a **variation of the merge-join algorithm**.  
  4. **Not use any buffers**.  

- Since `R_sorted.tsv` and `S_sorted.tsv` may contain **duplicates**, the program should:  
  - Eliminate duplicates from the inputs.  
  - Avoid writing duplicates to the output file.  

### Output Example
  aa 11
  ab 33
  ab 45


---

## Part 3: Intersection

Write a program that reads the files `R_sorted.tsv` and `S_sorted.tsv` and calculates the **intersection of R and S**, writing the result to a file `RintersectionS.tsv`, assuming that they have exactly the same fields.  

### Requirements
- The program must:
  1. Read the lines of the files `R_sorted.tsv` and `S_sorted.tsv` **only once**.  
  2. Simultaneously calculate their **intersection** and write the tuples of the intersection to the output file.  
  3. Implement a **variation of the merge-join algorithm**.  
  4. **Not use any buffers**.  

- Since `R_sorted.tsv` and `S_sorted.tsv` may contain **duplicates**, the program should:  
  - Eliminate duplicates from the inputs.  
  - Avoid writing duplicates to the output file.  

### Output Example
  bb 94
  bh 10
  cl 41


---

## Part 4: Set-Difference

Write a program that reads the files `R_sorted.tsv` and `S_sorted.tsv` and calculates the **difference between R and S**, writing the result to a file `RdifferenceS.tsv`, assuming that they have exactly the same fields.  

### Requirements
- The program must:
  1. Read the lines of the files `R_sorted.tsv` and `S_sorted.tsv` **only once**.  
  2. Simultaneously calculate their **difference** and write the tuples of the difference to the output file.  
  3. Implement a **variation of the merge-join algorithm**.  
  4. **Not use any buffers**.  

- Since `R_sorted.tsv` and `S_sorted.tsv` may contain **duplicates**, the program should:  
  - Eliminate duplicates from the inputs.  
  - Avoid writing duplicates to the output file.  

### Output Example
  aa 11
  ab 33
  ab 90


---

## Part 5: Grouping and Aggregation

Write a program that reads the unsorted file `R.tsv` and calculates the **grouping and aggregation** of its tuples, writing the result to a file `Rgroupby.tsv`.  

The grouping is based on the **first field** of each tuple, and the aggregation is the **sum** of the values in the second field.  

### Example
- Input tuples:  
  ('ab', 33), ('ab', 90)

- Grouped result:  
  ('ab', 123)

  
### Requirements
- The implementation will be done **in main memory**:
1. Read the entire file `R.tsv` into an array (list).  
2. Implement and run the **classic sort-merge algorithm** in memory.  
3. Modify the merge step as follows:  
   - If two tuples being merged are identical in the **first field**, then create a **single tuple** with the **sum of the second fields**.  

### Output Example
  aa 11
  ab 123
  ac 54
  ad 46
