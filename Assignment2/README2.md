# Assignment: Building and Using an R-Tree for Spatial Data

The goal of this assignment is to build and use an **R-tree index** for spatial data.

---

## Part 1: Building an R-Tree through Bulk Loading

You are asked to write a program that will **build an R-Tree** for a set of polygons, which you will read from two text files.

Your program should:

1. Calculate the **Minimum Bounding Rectangles (MBRs)** of the objects.  
2. Perform **bulk loading** of the tree after sorting the MBRs using a **space-filling curve**, specifically the **z-order curve**.

> **Note:** Space-filling curves map a multidimensional vector to a single-dimensional value. Objects that are close together spatially are likely to be mapped to close values. Consequently, MBRs that are close together are likely to be placed in the same leaf of the tree.

More information:  
- [Space-filling curve - Wikipedia](https://en.wikipedia.org/wiki/Space-filling_curve)  
- [Z-order curve - Wikipedia](https://en.wikipedia.org/wiki/Z-order_curve)

---

### Input Files

You are given two input files:

- `coords.txt` → Contains coordinates of points in the form `<x>,<y>`.  
- `offsets.txt` → Contains records in the form `<id>,<startOffset>,<endOffset>` where:
  - `id` → Unique identifier of a polygon object  
  - `startOffset` / `endOffset` → Line numbers in `coords.txt` marking the start/end of the points forming each object

---

### Program Requirements

1. **Read the two files** and find the coordinates for each object.  
2. Calculate the **MBR** of each object.  
3. Transform the **center of each MBR** to calculate its **z-order curve value**.  
4. **Sort the MBRs** based on the z-order values.  
5. "Package" the MBRs into **leaves** and recursively build the next levels of the R-tree up to the **root**.  
   - For levels above leaves, you do **not** need to redo z-order sorting.  
6. **Node capacity:**  
   - Maximum: 20 records per node  
   - Minimum: 0.4 × 20 = 8 records per node  
   - Last node adjustment: If fewer than 8, adjust to exactly 8 and reduce the previous node to < 20.  
   - **Root node:** Can have 2 to 20 children.  
7. **Leaf nodes:** Contain records of the form `[id, MBR]`  
   - `MBR = [x-low, x-high, y-low, y-high]`  
8. **Non-leaf nodes:** Contain records of the form `[id, MBR]`  
   - `id` → Node ID  
   - `MBR` → Bounding rectangle covering all child records

---

### Z-Order Transformation

To transform a coordinate `(x, y)` to a **z-order code**, you can use the `interleave_latlng` function from:  
- [pymorton.py](https://github.com/trevorprater/pymorton/blob/master/pymorton/pymorton.py)  

> Call it as `interleave_latlng(y, x)` to get a z-value in alphanumeric form.  
> Sort your MBRs based on these alphanumeric values.

---

### Program Output

1. Print the **number of nodes per level**:

```
  500 nodes at level 0
  25 nodes at level 1
  2 nodes at level 2
  1 node at level 3
```


2. Write all the nodes of the tree to `Rtree.txt` **ordered by node IDs**.  

**Node format:**
```
[isnonleaf, node-id, [[id1, MBR1], [id2, MBR2], …, [idn, MBRn]]]
```


- `isnonleaf = 1` → node is not a leaf  
- `isnonleaf = 0` → node is a leaf  
- Each `id` is either a **node ID** (points to a child node) or **object ID** (points to a polygon)  
- `MBR = [x-low, x-high, y-low, y-high]` → Node or object bounding rectangle

**Example first line of `Rtree.txt`:**

```
[0, 0, [[5868, [-170.844179, -170.707084, -14.373776, -14.287277]],
..., [3060, [-157.850181, -157.848054, 21.301518, 21.303834]]]]
```

- The **last line** of the file should correspond to the **root node**.

---

## Part 2: Range Queries

Implement a **range query evaluation** function in the R-Tree you created.  

### Goal
- The query range is defined by a **rectangle `W`**.  
- The function should find all **MBRs that intersect `W`**.

### Function Inputs
- `nodeid` → ID of the **root node** of the R-tree  
- `W` → Query rectangle in the form `[x-low, x-high, y-low, y-high]`  

The function should calculate the results of the query using the R-tree.

---

### Test Data

You are given the file `Rqueries.txt` containing queries of the form:

```
<x_low> <y_low> <x_high> <y_high>
```


- `x_low` → lower bound of the x-dimension of the query window  
- `x_high` → upper bound of the x-dimension of the query window  
- `y_low` → lower bound of the y-dimension of the query window  
- `y_high` → upper bound of the y-dimension of the query window  

---

### Program Requirements

1. The program should take as **command-line arguments**:
   - The **R-tree file** created in Part 1  
   - The `Rqueries.txt` query file
2. Create the **tree** from the R-tree file.  
3. Read and **execute queries sequentially** from the query file.  
4. For each query, print to the output:
   - The **query line number** (starting from 0)  
   - The **number of results** in parentheses  
   - The **IDs of the objects** whose MBR overlaps the query window (`filter step`)

---

### Example Output
```
0 (7): 2527,2712,8371,5042,7080,7656,7944
```
