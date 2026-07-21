# Rapid Revision Guide — 4-Page Interview Cheat Sheet

> **Read this the night before your interview. Everything that matters, nothing that doesn't.**

---

## PAGE 1: SQL Syntax & Execution Order

### SQL Execution Order (Memorize This!)
```
FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```
**Why it matters:**
- Can't use SELECT alias in WHERE (alias defined LATER in SELECT)
- Can't use aggregate functions in WHERE (aggregation happens AFTER WHERE)
- HAVING can use aggregates (it runs AFTER GROUP BY)
- ORDER BY CAN use SELECT aliases (it runs AFTER SELECT)

---

### Essential SQL Syntax

```sql
-- Basic Query
SELECT col1, col2, AGG(col3)
FROM table1
[JOIN table2 ON condition]
[WHERE filter_condition]           -- Filters ROWS (no aggregates)
[GROUP BY col1, col2]
[HAVING aggregate_condition]       -- Filters GROUPS (can use aggregates)
[ORDER BY col ASC|DESC]
[LIMIT n OFFSET m];

-- Window Function Syntax
SELECT col,
  FUNCTION() OVER (
    [PARTITION BY col]             -- Reset per group
    [ORDER BY col]
    [ROWS|RANGE BETWEEN frame]
  )

-- CTE Syntax
WITH cte_name AS (
  SELECT ...
)
SELECT * FROM cte_name;

-- Recursive CTE
WITH RECURSIVE cte AS (
  SELECT ...         -- Anchor (base case)
  UNION ALL
  SELECT ...         -- Recursive case
  FROM cte WHERE ... -- Termination condition
)

-- Subquery types:
-- Scalar: Returns 1 value  → used in SELECT, WHERE
-- Column: Returns 1 column → used with IN, ANY, ALL, EXISTS
-- Table:  Returns table    → used in FROM clause (derived table)
-- Correlated: References outer query → executed per outer row
```

---

### Window Function Quick Reference

| Function | Description |
|---|---|
| `ROW_NUMBER()` | Unique sequential number (no ties) |
| `RANK()` | Same rank for ties, gaps after |
| `DENSE_RANK()` | Same rank for ties, NO gaps |
| `NTILE(n)` | Divide into n equal buckets |
| `LAG(col, n)` | Previous nth row value |
| `LEAD(col, n)` | Next nth row value |
| `FIRST_VALUE(col)` | First value in window frame |
| `LAST_VALUE(col)` | Last value in window frame |
| `SUM/AVG/COUNT/MIN/MAX OVER()` | Running aggregate |

### Frame Clause Defaults (CRITICAL!)
```sql
-- Default frame when ORDER BY present:
RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

-- For LAST_VALUE to work correctly, MUST specify:
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
```

---

### Top NULL Traps
| Expression | Result |
|---|---|
| `NULL = NULL` | NULL (not TRUE!) |
| `NULL IS NULL` | TRUE ✅ |
| `NULL + 5` | NULL |
| `COUNT(*)` | Counts all rows including NULLs |
| `COUNT(col)` | Excludes NULL values |
| `col NOT IN (1, 2, NULL)` | Returns empty! (always UNKNOWN) |
| `SUM(NULL)` | NULL (not 0!) |
| `COALESCE(NULL, 0)` | 0 |
| `NULLIF(x, 0)` | NULL (to avoid division by zero) |

---

### JOIN Quick Reference
| Join Type | Returns |
|---|---|
| INNER JOIN | Only matching rows |
| LEFT JOIN | All left + matching right (NULL if no match) |
| RIGHT JOIN | All right + matching left |
| FULL OUTER JOIN | All rows from both |
| CROSS JOIN | Cartesian product (m × n rows) |
| SELF JOIN | Table joined to itself |

**Trap:** `LEFT JOIN + WHERE right.col = value` → Becomes INNER JOIN! Put condition in ON clause.

---

## PAGE 2: DBMS Concepts Rapid Fire

### ACID — Memory Aid: **A**tomic **C**onsistent **I**solated **D**urable
| Property | Implementation | Key Word |
|---|---|---|
| Atomicity | Undo/Redo log | All-or-Nothing |
| Consistency | Constraints, triggers | Valid state |
| Isolation | Locks, MVCC | Concurrent |
| Durability | WAL (Write-Ahead Log) | Crash survival |

---

### Isolation Levels — Problems Prevented
| Level | Dirty Read | Non-Repeatable | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | ❌ Can happen | ❌ Can happen | ❌ Can happen |
| READ COMMITTED (PostgreSQL default) | ✅ Prevented | ❌ Can happen | ❌ Can happen |
| REPEATABLE READ (MySQL default) | ✅ Prevented | ✅ Prevented | ❌ Can happen |
| SERIALIZABLE | ✅ Prevented | ✅ Prevented | ✅ Prevented |

---

### Normalization Cheat Sheet
| Form | Requirement |
|---|---|
| 1NF | Atomic values, unique rows |
| 2NF | 1NF + No partial dependency on composite PK |
| 3NF | 2NF + No transitive dependency |
| BCNF | For every A→B, A must be a super key |
| Denormalization | Add redundancy for performance (OLAP, reports) |

---

### Index Traps — When Index Is NOT Used
1. Function on indexed column: `WHERE YEAR(date) = 2024` ❌
2. Leading wildcard: `WHERE name LIKE '%smith'` ❌
3. Implicit type conversion: `WHERE int_col = '5'` ❌ (may skip index)
4. Low cardinality: Gender column (only M/F) ❌
5. Small table: Full scan cheaper ❌
6. NULL comparison with `=` instead of `IS NULL` ❌
7. Composite index wrong order: index(A,B) querying only B ❌

---

### Keys Summary
| Key Type | NULL allowed? | Duplicates? | Count per table |
|---|---|---|---|
| Primary Key | ❌ No | ❌ No | 1 |
| Unique Key | ✅ Yes (one) | ❌ No | Multiple |
| Foreign Key | ✅ Yes | ✅ Yes | Multiple |
| Candidate Key | (any valid PK candidate) | - | - |

---

### DELETE vs TRUNCATE vs DROP
| | DELETE | TRUNCATE | DROP |
|---|---|---|---|
| Type | DML | DDL | DDL |
| Rollback | ✅ Yes | ❌ No | ❌ No |
| WHERE clause | ✅ Yes | ❌ No | ❌ No |
| Triggers fire | ✅ Yes | ❌ No | ❌ No |
| Resets auto-increment | ❌ No | ✅ Yes | ✅ Yes (deleted) |
| Speed | Slow | Fast | Fast |

---

### CAP Theorem
```
Choose 2 of 3:  C = Consistency  A = Availability  P = Partition Tolerance
Partitions WILL happen → Real choice: CP or AP

CP systems: MongoDB, HBase, Zookeeper
AP systems: Cassandra, CouchDB, DynamoDB  
CA systems: Traditional RDBMS (single node)
```

---

### Sharding vs Partitioning
| | Partitioning | Sharding |
|---|---|---|
| Servers | Same server | Multiple servers |
| Type | Logical split | Physical split |
| Goal | Manageability | Horizontal scale |
| Strategies | Range, Hash, List | Range, Hash |

---

## PAGE 3: MongoDB Cheat Sheet

### CRUD Quick Reference
```javascript
// INSERT
db.col.insertOne({})
db.col.insertMany([{}, {}])

// READ
db.col.find({filter}, {projection})
db.col.findOne({filter})
db.col.countDocuments({filter})
db.col.distinct("field")

// UPDATE
db.col.updateOne({filter}, {update}, {upsert: bool})
db.col.updateMany({filter}, {update})
db.col.replaceOne({filter}, {replacement})  // Replaces whole doc!
db.col.findOneAndUpdate({filter}, {update}, {returnDocument: "after"})

// DELETE
db.col.deleteOne({filter})
db.col.deleteMany({filter})
```

---

### Update Operators
| Operator | Purpose |
|---|---|
| `$set` | Set field value |
| `$unset` | Remove field |
| `$inc` | Increment number |
| `$mul` | Multiply number |
| `$rename` | Rename field |
| `$push` | Add element to array |
| `$pull` | Remove element from array |
| `$addToSet` | Add only if not exists (no duplicates) |
| `$pop` | Remove first (-1) or last (1) array element |

---

### Aggregation Pipeline Stages
```javascript
db.collection.aggregate([
  { $match: {...} },         // WHERE (use FIRST for performance!)
  { $project: {...} },       // SELECT — include/exclude/compute
  { $addFields: {...} },     // Add computed fields (keeps existing)
  { $group: { _id: "$field", result: {$sum/avg/max/min: "$field"} } },
  { $sort: { field: 1 } },   // ORDER BY
  { $limit: n },             // LIMIT
  { $skip: n },              // OFFSET
  { $lookup: {from, localField, foreignField, as} },  // JOIN
  { $unwind: "$arrayField" }, // Flatten array (one doc per element)
  { $count: "field_name" },   // Count documents
  { $facet: { pipeline1: [...], pipeline2: [...] } }, // Multiple results
  { $out: "collection_name" } // Write to collection
])
```

---

### Comparison Operators
| SQL | MongoDB |
|---|---|
| `= 5` | `{ $eq: 5 }` or just `5` |
| `!= 5` | `{ $ne: 5 }` |
| `> 5` | `{ $gt: 5 }` |
| `>= 5` | `{ $gte: 5 }` |
| `< 5` | `{ $lt: 5 }` |
| `<= 5` | `{ $lte: 5 }` |
| `IN (1,2,3)` | `{ $in: [1,2,3] }` |
| `NOT IN` | `{ $nin: [1,2,3] }` |
| `AND` | `{ $and: [...] }` or multiple conditions |
| `OR` | `{ $or: [...] }` |

---

### Schema Design Decision
```
Embed when:
  ✅ Frequently accessed together
  ✅ One-to-few relationship
  ✅ Child data rarely changes independently

Reference when:
  ✅ Unbounded growth (thousands of children)
  ✅ Data shared across multiple documents
  ✅ Many-to-many relationships
  ✅ Independent access needed
```

---

### MongoDB vs SQL
| | MongoDB | SQL |
|---|---|---|
| Schema | Flexible (no ALTER TABLE) | Fixed, predefined |
| Scale | Horizontal (native sharding) | Vertical primarily |
| Joins | Manual ($lookup, expensive) | Native, optimized |
| Transactions | Yes (4.0+, replica set) | Yes (native) |
| Consistency | Eventual by default (configurable) | Strong (ACID) |
| Query language | BSON/JSON-like API | Declarative SQL |
| Best for | Flexible data, write-heavy, scale | Relational, transactions |

---

## PAGE 4: Most Frequently Asked Interview Questions

### The "Must Know" SQL Patterns
```sql
-- 1. Second Highest Salary
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);

-- 2. Nth Highest (generic)
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER(ORDER BY salary DESC) rnk FROM employees
) t WHERE rnk = N;

-- 3. Duplicates
SELECT col, COUNT(*) FROM table GROUP BY col HAVING COUNT(*) > 1;

-- 4. Delete duplicates (keep lowest ID)
DELETE FROM table WHERE id NOT IN (SELECT MIN(id) FROM table GROUP BY email);

-- 5. Running total
SELECT *, SUM(amount) OVER(ORDER BY date) AS running_total FROM orders;

-- 6. Month-over-month growth
SELECT yr, mo, revenue,
  LAG(revenue) OVER(ORDER BY yr, mo) AS prev_revenue FROM monthly_data;

-- 7. Employees earning more than their manager
SELECT e.name FROM employees e JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;

-- 8. Departments where ALL employees earn > X
SELECT dept_id FROM employees GROUP BY dept_id HAVING MIN(salary) > 50000;

-- 9. Customers with no orders
SELECT c.name FROM customers c LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.order_id IS NULL;

-- 10. Top N per group
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) rn
    FROM employees
) t WHERE rn <= 3;
```

---

### Common Interview Traps Summary

**SQL Traps:**
- `WHERE dept_id = NULL` → always use `WHERE dept_id IS NULL`
- `LEFT JOIN + WHERE right.col = 'value'` → becomes INNER JOIN
- `NOT IN (... NULL)` → returns empty result
- `HAVING dept_id > 2` instead of `WHERE dept_id > 2` → inefficient
- `SELECT *` in production queries → performance killer
- `LIMIT n OFFSET 10000` → slow pagination (use keyset pagination)
- `BETWEEN '2024-01-01' AND '2024-12-31'` for DATETIME → misses time portion of last day

**Normalization Traps:**
- "BCNF is always better than 3NF" → FALSE. BCNF can lose decomposability.
- "Normalization always improves performance" → FALSE. Too many joins can kill read performance.

**Index Traps:**
- "More indexes = faster queries" → FALSE. Indexes hurt INSERT/UPDATE/DELETE.
- "Composite index on (A,B) helps WHERE B=?" → FALSE (leftmost prefix rule).
- "Index makes LIKE '%abc%' fast" → FALSE (leading wildcard).

**Transaction Traps:**
- "READ COMMITTED prevents phantom reads" → FALSE (needs SERIALIZABLE).
- "Higher isolation = better performance" → FALSE (more locking = less concurrency).

---

### 20 Questions Most Likely To Be Asked

1. Second highest salary query (write it 3 ways)
2. Difference between WHERE and HAVING
3. What is a window function? Give an example.
4. RANK vs DENSE_RANK vs ROW_NUMBER
5. What is a self join? Write a manager-employee query.
6. How to find duplicates in a table?
7. Explain ACID properties.
8. What are isolation levels? What problems do they prevent?
9. Difference between clustered and non-clustered index?
10. When would a query NOT use an index?
11. What is normalization? Explain 1NF, 2NF, 3NF.
12. Difference between DELETE, TRUNCATE, DROP?
13. What is CAP theorem?
14. Explain sharding vs partitioning.
15. MongoDB `$lookup` vs SQL JOIN — differences?
16. What is a covering index?
17. Explain the aggregation pipeline in MongoDB.
18. What is optimistic vs pessimistic locking?
19. How would you design an e-commerce schema?
20. What is the N+1 query problem and how do you fix it?

---

### Query Optimization Checklist
```
Before submitting any query in an interview:
☐ Am I using SELECT * ? (Use specific columns)
☐ Is there a WHERE clause to filter early?
☐ Are indexed columns unmodified in WHERE? (No functions!)
☐ Is HAVING used for non-aggregate conditions? (Move to WHERE)
☐ Is JOIN producing unexpected duplicates?
☐ Is pagination using LIMIT+OFFSET on large tables? (Use keyset)
☐ Are NULL comparisons using IS NULL / IS NOT NULL?
☐ Is UNION needed or can UNION ALL be used?
☐ Would a window function be cleaner than a subquery?
☐ Would a CTE make this more readable?
```

---

*🎯 You're ready. Every query pattern has been covered. Good luck!*
