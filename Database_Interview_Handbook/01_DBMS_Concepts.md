# DBMS Concepts — Theory, Interview Q&A, and Traps

> **20% theory, 80% interview. Every section has traps and follow-ups.**

---

## 1. KEYS

**Quick Revision:**
- **Primary Key:** Uniquely identifies a row. No NULL, no duplicates.
- **Candidate Key:** Any column(s) that could be a primary key.
- **Super Key:** Any set of columns that uniquely identifies a row (superset of candidate key).
- **Foreign Key:** References a primary key in another table. Enforces referential integrity.
- **Composite Key:** Primary key made of multiple columns.
- **Surrogate Key:** Artificially generated key (e.g., auto-increment ID). Has no business meaning.
- **Natural Key:** A real-world column used as PK (e.g., email, Aadhaar number).

**Interview Trap ⚠️:**
- "Can a foreign key have NULL values?" → YES! A NULL FK means the row doesn't reference any parent row.
- "Can a table have multiple unique keys?" → YES! Only one PRIMARY key, but multiple UNIQUE constraints.
- "Difference between super key and candidate key?" → Every candidate key is a super key, but NOT every super key is a candidate key. A super key may contain extra columns.

**Frequently Asked:**
1. What is the difference between primary key and unique key?
   - PK: NOT NULL + UNIQUE. Only one per table.
   - UNIQUE: Allows one NULL. Multiple allowed per table.

2. Can a foreign key reference a non-primary key?
   - YES — it can reference any UNIQUE key column in the parent table.

---

## 2. NORMALIZATION

**Quick Revision:**
- Process of organizing data to reduce redundancy and improve integrity.
- **1NF:** Atomic values, no repeating groups, each row is unique.
- **2NF:** 1NF + No partial dependency (non-key attribute depends on the whole composite key).
- **3NF:** 2NF + No transitive dependency (non-key attribute depends on another non-key attribute).
- **BCNF:** 3NF + For every functional dependency X→Y, X must be a super key.
- **Denormalization:** Intentionally adding redundancy for performance (used heavily in MongoDB, OLAP).

**Interview Trap ⚠️:**
- "Is BCNF stricter than 3NF?" → YES. Every BCNF relation is in 3NF, but NOT vice versa.
- "Can normalization hurt performance?" → YES! Too many joins degrade read performance. That's why we denormalize for reporting.
- "What is a transitive dependency?" → A→B and B→C means A→C transitively (violates 3NF).

**Example:**
```
Table: Orders(order_id, customer_id, customer_name, product_id)
customer_name depends on customer_id (transitive) — VIOLATES 3NF
Fix: Split into Orders(order_id, customer_id, product_id) and Customers(customer_id, customer_name)
```

---

## 3. ACID PROPERTIES

**Quick Revision:**
- **Atomicity:** Transaction is all-or-nothing. (undo on failure via rollback logs)
- **Consistency:** DB moves from one valid state to another. Constraints always satisfied.
- **Isolation:** Concurrent transactions don't interfere. Managed via locks/MVCC.
- **Durability:** Committed transactions survive crashes. (Write-ahead log, WAL)

**Interview Trap ⚠️:**
- "Which ACID property is hardest to achieve in distributed systems?" → Consistency (conflicts with Availability in CAP theorem).
- "How is Atomicity implemented?" → Undo/Redo logs (Write-Ahead Logging). On failure, transaction is rolled back.
- "How is Durability implemented?" → WAL (Write-Ahead Log). Changes are written to disk log BEFORE applying to DB.

**Follow-up:** "What happens if a system crashes mid-transaction?"
→ On restart, DB uses the WAL to REDO committed transactions and UNDO uncommitted ones.

---

## 4. TRANSACTIONS & ISOLATION LEVELS

**Quick Revision:**
```
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 500 WHERE id = 1;
  UPDATE accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;  -- or ROLLBACK on error
```

**Concurrency Problems:**
| Problem | Description |
|---|---|
| **Dirty Read** | T2 reads data written by T1 that hasn't committed yet |
| **Non-Repeatable Read** | T1 reads same row twice, gets different values (T2 updated it in between) |
| **Phantom Read** | T1 reads a range, T2 inserts rows matching the range, T1 re-reads and sees new rows |
| **Lost Update** | Two transactions read the same data and both write back, one overwrites the other |

**Isolation Levels (Strictest to Loosest):**
| Level | Dirty Read | Non-Repeatable | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | ✅ Possible | ✅ Possible | ✅ Possible |
| READ COMMITTED | ❌ Prevented | ✅ Possible | ✅ Possible |
| REPEATABLE READ | ❌ Prevented | ❌ Prevented | ✅ Possible |
| SERIALIZABLE | ❌ Prevented | ❌ Prevented | ❌ Prevented |

**Interview Trap ⚠️:**
- "MySQL InnoDB default isolation level?" → REPEATABLE READ (not Serializable!)
- "PostgreSQL default?" → READ COMMITTED
- "Higher isolation = lower or higher performance?" → LOWER (more locking, less concurrency)
- "What is MVCC?" → Multi-Version Concurrency Control. Maintains multiple versions of data to allow reads without blocking writes. Used by PostgreSQL, MySQL InnoDB.

---

## 5. INDEXES

**Quick Revision:**
- Data structure (B-Tree or Hash) that speeds up data retrieval.
- **Clustered Index:** Physical order of rows matches index order. One per table (usually PK).
- **Non-Clustered Index:** Separate structure with pointers to actual data. Multiple allowed.
- **Composite Index:** Index on multiple columns. Column ORDER matters!
- **Covering Index:** Index includes all columns needed by a query — no table lookup required.
- **Partial Index:** Index on a subset of rows (WHERE condition).

**Interview Trap ⚠️:**
- "Does a SELECT on an unindexed column use the index?" → NO — full table scan occurs.
- "Why can too many indexes hurt performance?" → Every INSERT/UPDATE/DELETE must also update all indexes.
- "Composite index on (A, B) — which queries benefit?" → WHERE A=?, WHERE A=? AND B=? → YES. WHERE B=? alone → NO! (Leftmost prefix rule)
- "Difference between clustered and non-clustered index?" → Table can have ONE clustered (data physically sorted), MANY non-clustered (separate structure).

**Follow-up:** "When would you NOT create an index?"
→ On small tables, on columns with low cardinality (e.g., gender: M/F), on rarely-queried columns, on write-heavy tables.

---

## 6. JOINS (Theory)

**Types:**
| Join Type | Returns |
|---|---|
| INNER JOIN | Rows with matching values in BOTH tables |
| LEFT JOIN | All rows from left + matching from right (NULL if no match) |
| RIGHT JOIN | All rows from right + matching from left |
| FULL OUTER JOIN | All rows from both tables |
| CROSS JOIN | Cartesian product (every row × every row) |
| SELF JOIN | Table joined with itself |

**Interview Trap ⚠️:**
- "INNER JOIN vs WHERE clause join?" → Functionally same, but INNER JOIN is more readable and modern.
- "Can you JOIN on non-equal conditions?" → YES! `ON a.salary BETWEEN b.min AND b.max` is valid.
- "LEFT JOIN with WHERE on right table?" → Effectively becomes INNER JOIN! Filter right-table columns in ON clause, not WHERE.

---

## 7. VIEWS

**Quick Revision:**
- Virtual table. No data stored — just the query definition.
- **Updatable View:** Can INSERT/UPDATE/DELETE if based on single table, no DISTINCT/GROUP BY/aggregation.
- **Materialized View:** Physically stores the result. Must be REFRESHED. Better for reporting.

**Interview Trap ⚠️:**
- "Does a view store data?" → Regular view: NO. Materialized view: YES.
- "Can you create an index on a view?" → YES on materialized views. No on regular views (nothing to index).

---

## 8. STORED PROCEDURES & TRIGGERS

**Quick Revision:**
- **Stored Procedure:** Precompiled SQL + procedural logic (loops, conditions). Reduces network trips.
- **Trigger:** Automatically executes on INSERT/UPDATE/DELETE events. BEFORE or AFTER.
- **Function:** Returns a value. Can be used in SELECT. Cannot have side effects (in pure functions).

**Interview Trap ⚠️:**
- "Stored Procedure vs Function?" → SP: Can return multiple result sets, can use transactions, cannot be used in SELECT. Function: Returns single value/table, can be used in SELECT, should have no side effects.
- "Can a trigger call another trigger?" → YES — can cause infinite loops if not careful (cascading triggers).
- "What is a mutating table error?" → In Oracle — a row-level trigger trying to read/write the same table it's defined on.

---

## 9. LOCKING & DEADLOCKS

**Lock Types:**
- **Shared Lock (S):** Read lock. Multiple transactions can hold simultaneously.
- **Exclusive Lock (X):** Write lock. Only one at a time. Blocks all other locks.
- **Row-level Lock:** Locks only the specific row (finer granularity, better concurrency).
- **Table-level Lock:** Locks the whole table (simpler, worse concurrency).
- **Intention Locks (IX, IS):** Signal intent to lock at finer granularity.

**Deadlock Example:**
```
T1 locks Row A, waits for Row B
T2 locks Row B, waits for Row A
→ Deadlock! Neither can proceed.
```

**Deadlock Resolution:** DB detects cycle in wait-for graph → kills one transaction (victim selection).

**Interview Trap ⚠️:**
- "How to prevent deadlocks?" → Always acquire locks in the same order. Use shorter transactions. Use LOCK TIMEOUT. Use optimistic locking for read-heavy workloads.
- "What is optimistic vs pessimistic locking?" → Pessimistic: Lock before read (for write-heavy). Optimistic: Read without lock, check version at write time (for read-heavy).

---

## 10. CAP THEOREM

**Quick Revision:**
In a distributed system, you can only guarantee **2 of 3**:
- **C**onsistency: Every read gets the most recent write.
- **A**vailability: Every request receives a response (not necessarily latest data).
- **P**artition Tolerance: System continues even when network partitions occur.

Since partitions WILL happen in distributed systems, the real choice is **CP vs AP**.

| System | Type | Examples |
|---|---|---|
| CP | Consistent + Partition tolerant | MongoDB, HBase, Zookeeper |
| AP | Available + Partition tolerant | Cassandra, CouchDB, DynamoDB |
| CA | Consistent + Available | Traditional RDBMS (no partition tolerance) |

**Interview Trap ⚠️:**
- "Is MongoDB CP or AP?" → By default AP (eventual consistency), but can be configured for CP using write concerns.
- "Can you have all three?" → NO. This is the theorem's guarantee. Network partitions make C and A impossible simultaneously.

---

## 11. SHARDING & PARTITIONING

**Quick Revision:**
- **Partitioning:** Splitting one large table into smaller pieces on the SAME server.
  - **Range Partitioning:** By date range (e.g., Jan, Feb, Mar).
  - **Hash Partitioning:** Hash of partition key distributes rows evenly.
  - **List Partitioning:** By specific values (e.g., country = 'IN', 'US').
- **Sharding:** Distributing data across MULTIPLE servers (horizontal scaling).
  - **Shard Key:** Column used to determine which shard a row goes to. Critical choice!

**Interview Trap ⚠️:**
- "Difference between sharding and partitioning?" → Partitioning: same machine, logical split. Sharding: different machines, physical split.
- "What is a hot shard?" → One shard receives disproportionately more traffic (bad shard key choice). Fix: choose high-cardinality, evenly distributed key.
- "What is re-sharding?" → Adding more shards and redistributing data. Painful — plan shard key carefully upfront!

---

## 12. REPLICATION

**Quick Revision:**
- Copying data from one DB server (primary/master) to one or more (replica/slave) servers.
- **Synchronous Replication:** Primary waits for replica to confirm write. Strong consistency, slower.
- **Asynchronous Replication:** Primary doesn't wait. Faster, but replica may be slightly behind (replication lag).
- **Read Replicas:** Offload read traffic from primary.

**Interview Trap ⚠️:**
- "What is replication lag?" → Time delay between write on primary and availability on replica.
- "What is split-brain?" → When network partition causes two nodes to both think they're the primary and accept writes, leading to data divergence.

---

## 50 DBMS Interview Questions with Answers

**Q1. What is the difference between DELETE, TRUNCATE, and DROP?**
- DELETE: DML, row-by-row, can rollback, triggers fire, WHERE clause allowed, slow on large tables.
- TRUNCATE: DDL, removes all rows, cannot rollback (in most DBs), no triggers, resets identity, FAST.
- DROP: DDL, removes entire table structure + data + indexes. Cannot rollback.

**Q2. What is a self-join? Give an example.**
```sql
-- Find employees and their managers (both in same table)
SELECT e.name AS employee, m.name AS manager
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id;
```

**Q3. What is referential integrity?**
Ensures foreign key values always point to an existing primary key value. Enforced via FK constraints with ON DELETE CASCADE/RESTRICT/SET NULL.

**Q4. What is a correlated subquery?**
A subquery that references a column from the outer query — executed once per row of the outer query.
```sql
-- Employees who earn more than the average salary in their department
SELECT * FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id);
```

**Q5. What is the difference between HAVING and WHERE?**
- WHERE: Filters rows BEFORE grouping. Cannot use aggregate functions.
- HAVING: Filters groups AFTER GROUP BY. CAN use aggregate functions.

**Q6. What is an execution plan / query plan?**
The database engine's step-by-step strategy for executing a query. Use `EXPLAIN` or `EXPLAIN ANALYZE` to view it. Shows whether index is used, join strategy, estimated row counts.

**Q7. What is OLTP vs OLAP?**
- OLTP (Online Transaction Processing): Many small, fast read/write transactions. Normalized schema. e.g., banking system.
- OLAP (Online Analytical Processing): Complex queries on huge historical data. Denormalized/star schema. e.g., reporting dashboard.

**Q8. What is a star schema vs snowflake schema?**
- Star: One fact table surrounded by denormalized dimension tables. Faster queries.
- Snowflake: Dimension tables further normalized. Less redundancy, more joins.

**Q9. What is a materialized view?**
A database object that stores the physical result of a query. Must be periodically refreshed (REFRESH MATERIALIZED VIEW). Faster reads, but stale data risk.

**Q10. How does B-Tree index work?**
B-Tree (Balanced Tree) keeps data sorted. Supports =, <, >, BETWEEN, LIKE 'abc%' queries. Tree traversal from root to leaf — O(log n) lookups.

**Q11. What is a hash index?**
Uses a hash function on the key. Only supports equality (=) lookups — O(1). CANNOT support range queries (BETWEEN, <, >).

**Q12. What is denormalization and when do you use it?**
Intentionally adding redundancy (violating normalization rules) to improve read performance. Used in: reporting systems, OLAP, MongoDB schemas, high-read-low-write scenarios.

**Q13. Explain the two-phase locking protocol (2PL).**
Phase 1 (Growing): Transaction acquires locks but never releases.
Phase 2 (Shrinking): Transaction releases locks but never acquires new ones.
Guarantees serializability but can cause deadlocks.

**Q14. What is phantom read? How is it prevented?**
Transaction T1 reads rows matching condition. T2 inserts new matching rows. T1 re-reads, sees new "phantom" rows.
Prevention: SERIALIZABLE isolation level (uses range locks or predicate locks).

**Q15. What is the difference between optimistic and pessimistic locking?**
- Pessimistic: Lock the row before reading (prevents conflicts). Good for write-heavy systems.
- Optimistic: Read without lock, check version/timestamp at write. If changed, retry. Good for read-heavy.
```sql
-- Optimistic locking pattern
UPDATE orders SET status='SHIPPED', version=version+1
WHERE order_id=1 AND version=5; -- Only succeeds if version hasn't changed
```

**Q16. What is a covering index?**
An index that contains all columns required by a query — eliminates the need to access the actual table rows. Dramatically improves performance.
```sql
-- If query is: SELECT name, salary FROM employees WHERE dept_id = 3
-- Covering index: CREATE INDEX idx_covering ON employees(dept_id, name, salary);
```

**Q17. What is index selectivity?**
Ratio of distinct values to total rows. High selectivity (closer to 1) = more useful for indexes.
Gender (M/F) = low selectivity = bad index candidate.
email = high selectivity = great index candidate.

**Q18. When does a query NOT use an index?**
- Function applied to the indexed column: `WHERE YEAR(hire_date) = 2023` (use `WHERE hire_date BETWEEN '2023-01-01' AND '2023-12-31'`)
- Using `!=` or `NOT IN`
- Leading wildcard: `WHERE name LIKE '%John'`
- Low cardinality column
- Table is very small (full scan is cheaper)

**Q19. What is the N+1 problem?**
1 query to fetch N parent records, then N queries to fetch each child — total N+1 queries. Fix: Use JOIN or eager loading.
```sql
-- Bad: N+1 (1 query for customers + N queries for each customer's orders)
-- Good: JOIN customers and orders in one query
SELECT c.*, o.* FROM customers c JOIN orders o ON c.customer_id = o.customer_id;
```

**Q20. What is connection pooling?**
Maintaining a pool of reusable database connections instead of opening/closing one per request. Reduces overhead of TCP handshake + DB authentication per request.

**Q21. What is a surrogate key vs natural key? Which is better?**
- Surrogate: System-generated (INT auto_increment, UUID). Always unique, stable, no business meaning.
- Natural: Real-world data (email, SSN). Can change, can be long strings — bad for FK joins.
- **Interview Answer:** Surrogate keys are generally better for PK in relational DBs.

**Q22. What is WAL (Write-Ahead Log)?**
Before any change is made to the actual data pages, the change is first written to a log file. On crash, DB replays the log to restore consistency. Guarantees Durability (ACID).

**Q23. Difference between UNION and UNION ALL?**
- UNION: Removes duplicates (sorts/hashes intermediate result). Slower.
- UNION ALL: Keeps all rows including duplicates. Faster.
- **Trap:** Use UNION ALL when you KNOW there are no duplicates — avoid unnecessary de-duplication cost.

**Q24. What is a recursive CTE?**
```sql
-- Find employee hierarchy (manager → employee chain)
WITH RECURSIVE hierarchy AS (
    SELECT emp_id, name, manager_id, 0 AS level
    FROM employees WHERE manager_id IS NULL -- Root (CEO)
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, h.level + 1
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.emp_id
)
SELECT * FROM hierarchy;
```

**Q25. What is the difference between a clustered and non-clustered index?**
- Clustered: The table data IS the index. Rows physically stored in index order. One per table.
- Non-clustered: Separate structure. Leaf nodes contain pointers (row ID) to actual data. Multiple allowed.

**Q26. Explain SAVEPOINT.**
```sql
BEGIN;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  SAVEPOINT sp1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
  -- If error:
  ROLLBACK TO sp1; -- Only undoes the second update
COMMIT;
```

**Q27. What is MVCC (Multi-Version Concurrency Control)?**
DB maintains multiple versions of a row. Readers see a snapshot of the DB at the time their transaction started — no blocking between readers and writers. Used by PostgreSQL (always), MySQL InnoDB (for REPEATABLE READ), Oracle.

**Q28. Difference between VARCHAR and CHAR?**
- CHAR(n): Fixed length. Always uses n bytes. Padded with spaces. Faster for fixed-width data.
- VARCHAR(n): Variable length. Uses only as many bytes as needed + 1-2 bytes overhead. Better for variable-width data.

**Q29. What is a foreign key ON DELETE CASCADE?**
When a parent row is deleted, all child rows with that FK are automatically deleted too.
```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);
```

**Q30. What is an ER Diagram? Key components?**
Entity-Relationship Diagram. Shows: Entities (rectangles), Attributes (ovals), Relationships (diamonds), Cardinality (1:1, 1:N, M:N), Weak Entities (double rectangle).

**Q31. How do you handle M:N relationships in SQL?**
Use a junction/bridge table:
```sql
CREATE TABLE student_courses (
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

**Q32. What is the difference between a database and a schema?**
- Database: Physical container of all objects (tables, views, procedures).
- Schema: Logical namespace within a database to group related objects.
- In PostgreSQL: schema is a namespace inside a database. In MySQL: database = schema (interchangeable).

**Q33. What is an anti-pattern in database design?**
- **EAV (Entity-Attribute-Value):** One table for all attributes — hard to query, no type safety.
- **One table for everything:** No normalization, massive columns.
- **Using NULL as a sentinel value:** Confuses "unknown" with "not applicable".
- **Storing comma-separated values in one column:** Violates 1NF.

**Q34. What is query optimization? Key strategies?**
1. Use indexes on WHERE, JOIN, ORDER BY columns.
2. Avoid SELECT * — specify only needed columns.
3. Avoid functions on indexed columns in WHERE.
4. Use EXPLAIN to identify full table scans.
5. Use covering indexes.
6. Partition large tables.
7. Use appropriate join type.
8. Limit result sets with pagination (LIMIT/OFFSET).

**Q35. What is a full table scan and when does it occur?**
DB reads every row in the table. Occurs when: no applicable index, query uses functions on indexed column, low selectivity column, very small table (optimizer prefers scan over index lookup).

**Q36. Explain database connection pooling architecture.**
Pool manager maintains N pre-opened connections. App requests connection from pool → uses it → returns to pool. Tools: HikariCP (Java), pgBouncer (PostgreSQL), ProxySQL (MySQL).

**Q37. What is the difference between horizontal and vertical scaling?**
- Vertical (Scale Up): Add more CPU/RAM to existing server. Simple but has a ceiling.
- Horizontal (Scale Out): Add more servers. Requires sharding/partitioning. More complex.

**Q38. What is eventual consistency?**
In distributed systems, if no new updates are made, all replicas will eventually converge to the same value. AP systems (Cassandra, DynamoDB) use this model.

**Q39. What is a database cursor?**
A server-side pointer to iterate through query results row-by-row. Used in stored procedures. Memory-intensive — avoid for large result sets; prefer set-based operations.

**Q40. What is the difference between SQL and NoSQL?**
| | SQL | NoSQL |
|---|---|---|
| Schema | Fixed, predefined | Dynamic, flexible |
| Scaling | Vertical (primarily) | Horizontal |
| Consistency | Strong (ACID) | Eventual (BASE) |
| Joins | Native | Manual ($lookup) |
| Use case | Transactions, reporting | Big data, unstructured |

**Q41. What is a transaction log?**
Sequential record of all DB changes. Used for: crash recovery (REDO/UNDO), replication (log shipping), point-in-time recovery.

**Q42. What is the purpose of EXPLAIN in SQL?**
Shows the execution plan the optimizer chose. Key things to look for:
- `Seq Scan` vs `Index Scan` — prefer Index Scan for selective queries.
- Estimated vs actual row counts — large discrepancy = stale statistics.
- Join strategy: Hash Join, Nested Loop, Merge Join.

**Q43. What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()?**
```
Data: salaries 5000, 5000, 4000
ROW_NUMBER():  1, 2, 3  (always unique)
RANK():        1, 1, 3  (gaps after ties)
DENSE_RANK():  1, 1, 2  (no gaps)
```

**Q44. What is a window function?**
Performs calculation across a set of rows related to the current row WITHOUT collapsing them into groups (unlike GROUP BY). Uses OVER() clause.
```sql
SELECT name, salary, AVG(salary) OVER(PARTITION BY dept_id) AS dept_avg FROM employees;
```

**Q45. What is the difference between INNER JOIN and EXISTS?**
Both check for matching rows, but:
- JOIN: Returns columns from both tables. Can cause row duplication if many-to-many.
- EXISTS: Returns only the outer table's rows. More efficient when you just need to check existence.

**Q46. What is database normalization vs denormalization trade-off?**
| | Normalized | Denormalized |
|---|---|---|
| Storage | Less (no redundancy) | More |
| Read performance | Slower (more joins) | Faster (fewer joins) |
| Write performance | Faster (update one place) | Slower (update multiple places) |
| Use case | OLTP | OLAP, MongoDB |

**Q47. What is cascading in FK constraints?**
```sql
ON DELETE CASCADE -- Delete child rows when parent deleted
ON DELETE SET NULL -- Set FK to NULL when parent deleted  
ON DELETE RESTRICT -- Prevent parent deletion if children exist (DEFAULT)
ON UPDATE CASCADE -- Update FK in child when parent PK changes
```

**Q48. What are database statistics and why do they matter?**
Statistics = metadata about data distribution (e.g., number of distinct values, histogram of column values). Query optimizer uses statistics to choose the best execution plan. Stale statistics → bad execution plans → slow queries. Fix: `ANALYZE` (PostgreSQL) or `UPDATE STATISTICS` (SQL Server).

**Q49. Explain the concept of a database buffer pool/cache.**
Memory area where DB caches frequently accessed data pages to avoid disk I/O. Key metric: **buffer hit ratio** — should be > 95% for production. Low hit ratio = too little memory allocated to buffer pool.

**Q50. What is a two-phase commit (2PC)?**
Distributed transaction protocol ensuring atomicity across multiple DBs:
1. **Prepare Phase:** Coordinator asks all participants if they can commit.
2. **Commit Phase:** If ALL say YES → commit. If ANY says NO → rollback.
Problem: Blocking protocol — if coordinator fails, participants are stuck. Modern systems use Saga pattern instead.
