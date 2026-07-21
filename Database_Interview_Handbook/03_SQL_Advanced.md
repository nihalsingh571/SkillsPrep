# SQL Advanced — Q81 to Q200+
## Window Functions, CTEs, Query Optimization, Debug Queries, DB Design

> **All queries use the dataset from [README.md](./README.md).**

---

## SECTION 1 — WINDOW FUNCTIONS (Q81–Q110)

> **Section Data reminder:**
> employees: Alice(90k,dept1), Bob(75k,dept1), Carol(85k,dept2), David(60k,dept2), Eve(95k,dept3), Frank(70k,dept3), Grace(75k,dept1), Hank(60k,dept2), Ivy(55k,NULL), Jack(90k,dept3)

---

### Q81. ROW_NUMBER — Assign unique row numbers within each department

📌 **New Concept — ROW_NUMBER():** Assigns a unique sequential integer to each row. No ties — even if two rows have the same value in `ORDER BY`, they get different numbers.

📌 **New Concept — OVER():** Defines the "window" of rows the function operates on. `PARTITION BY` divides rows into groups; `ORDER BY` sets the sequence within each group.

📌 **New Concept — PARTITION BY:** Divides the rows into groups (similar to `GROUP BY`), but WITHOUT collapsing the result into one row per group. The window function runs independently for each partition.

```sql
SELECT name, dept_id, salary,
       ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS row_num
FROM employees
WHERE dept_id IS NOT NULL;
```

**Output:**
| name  | dept_id | salary | row_num |
|-------|---------|--------|---------|
| Alice | 1       | 90000  | 1       |
| Bob   | 1       | 75000  | 2       |
| Grace | 1       | 75000  | 3       |
| Carol | 2       | 85000  | 1       |
| David | 2       | 60000  | 2       |
| Hank  | 2       | 60000  | 3       |
| Eve   | 3       | 95000  | 1       |
| Jack  | 3       | 90000  | 2       |
| Frank | 3       | 70000  | 3       |

> Bob and Grace both have 75000, but get different row_nums (2 and 3) because ROW_NUMBER never ties.

---

### Q82. RANK vs DENSE_RANK vs ROW_NUMBER — Side-by-side

📌 **New Concept — RANK():** Same rank for tied rows. **Skips** the next rank(s) after a tie. e.g., two rows at rank 1 → next rank is 3 (not 2).

📌 **New Concept — DENSE_RANK():** Same rank for tied rows. **Does NOT skip** ranks. e.g., two rows at rank 1 → next rank is 2.

```sql
SELECT name, salary,
       RANK()       OVER(ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER(ORDER BY salary DESC) AS dense_rnk,
       ROW_NUMBER() OVER(ORDER BY salary DESC) AS row_num
FROM employees
WHERE dept_id IS NOT NULL;
```

**Output:**
| name  | salary | rnk | dense_rnk | row_num |
|-------|--------|-----|-----------|---------|
| Eve   | 95000  | 1   | 1         | 1       |
| Alice | 90000  | 2   | 2         | 2       |
| Jack  | 90000  | 2   | 2         | 3       |
| Carol | 85000  | 4   | 3         | 4       |
| Bob   | 75000  | 5   | 4         | 5       |
| Grace | 75000  | 5   | 4         | 6       |
| Frank | 70000  | 7   | 5         | 7       |
| David | 60000  | 8   | 6         | 8       |
| Hank  | 60000  | 8   | 6         | 9       |

> Alice & Jack both 90000: RANK skips 3 (next is 4). DENSE_RANK goes to 3 (no gap).

---

### Q83. LAG and LEAD — Compare current row with previous/next order

📌 **New Concept — LAG(col, n):** Returns the value of `col` from **n rows before** the current row within the window. `n` defaults to 1. Returns NULL for the first row (no previous row).

📌 **New Concept — LEAD(col, n):** Returns the value of `col` from **n rows after** the current row. Returns NULL for the last row.

```sql
SELECT order_id, customer_id, amount, order_date,
       LAG(amount,  1) OVER(ORDER BY order_date) AS prev_amount,
       LEAD(amount, 1) OVER(ORDER BY order_date) AS next_amount
FROM orders;
```

**Output:**
| order_id | amount | order_date | prev_amount | next_amount |
|----------|--------|------------|-------------|-------------|
| 101      | 75000  | 2024-01-10 | NULL        | 12000       |
| 103      | 12000  | 2024-01-20 | 75000       | 1500        |
| 102      | 1500   | 2024-02-14 | 12000       | 800         |
| 104      | 800    | 2024-03-05 | 1500        | 75000       |
| 105      | 75000  | 2024-03-18 | 800         | 25000       |
| 106      | 25000  | 2024-04-02 | 75000       | 1200        |
| 107      | 1200   | 2024-04-15 | 25000       | 1500        |
| 108      | 1500   | 2024-05-01 | 1200        | 800         |
| 109      | 800    | 2024-05-20 | 1500        | 25000       |
| 110      | 25000  | 2024-06-10 | 800         | NULL        |

---

### Q84. Running total using SUM window function

```sql
SELECT order_id, order_date, amount,
       SUM(amount) OVER(ORDER BY order_date) AS running_total
FROM orders;
```

**Output:**
| order_id | order_date | amount | running_total |
|----------|------------|--------|---------------|
| 101      | 2024-01-10 | 75000  | 75000         |
| 103      | 2024-01-20 | 12000  | 87000         |
| 102      | 2024-02-14 | 1500   | 88500         |
| 104      | 2024-03-05 | 800    | 89300         |
| 105      | 2024-03-18 | 75000  | 164300        |
| 106      | 2024-04-02 | 25000  | 189300        |
| 107      | 2024-04-15 | 1200   | 190500        |
| 108      | 2024-05-01 | 1500   | 192000        |
| 109      | 2024-05-20 | 800    | 192800        |
| 110      | 2024-06-10 | 25000  | 217800        |

---

### Q85. Moving average — 3-order rolling average

📌 **New Concept — ROWS BETWEEN n PRECEDING AND CURRENT ROW:** Defines the window frame. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` means: current row + 2 rows before it = a rolling window of up to 3 rows.

```sql
SELECT order_id, order_date, amount,
       ROUND(AVG(amount) OVER(
           ORDER BY order_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ), 2) AS rolling_avg_3
FROM orders;
```

**Output:**
| order_id | order_date | amount | rolling_avg_3 |
|----------|------------|--------|---------------|
| 101      | 2024-01-10 | 75000  | 75000.00      |
| 103      | 2024-01-20 | 12000  | 43500.00      |
| 102      | 2024-02-14 | 1500   | 29500.00      |
| 104      | 2024-03-05 | 800    | 4766.67       |
| 105      | 2024-03-18 | 75000  | 25766.67      |
| 106      | 2024-04-02 | 25000  | 33600.00      |
| 107      | 2024-04-15 | 1200   | 33733.33      |
| 108      | 2024-05-01 | 1500   | 9233.33       |
| 109      | 2024-05-20 | 800    | 1166.67       |
| 110      | 2024-06-10 | 25000  | 9100.00       |

---

### Q86. FIRST_VALUE and LAST_VALUE

📌 **New Concept — FIRST_VALUE(col) / LAST_VALUE(col):** Returns the first or last value within the window frame. `LAST_VALUE` requires an explicit `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` frame — otherwise the default frame stops at the current row and `LAST_VALUE` just returns the current row's value!

```sql
SELECT name, dept_id, salary,
       FIRST_VALUE(name) OVER(PARTITION BY dept_id ORDER BY salary DESC) AS top_earner,
       LAST_VALUE(name)  OVER(PARTITION BY dept_id ORDER BY salary DESC
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS lowest_earner
FROM employees WHERE dept_id IS NOT NULL;
```

**Output:**
| name  | dept_id | salary | top_earner | lowest_earner |
|-------|---------|--------|------------|---------------|
| Alice | 1       | 90000  | Alice      | Grace         |
| Bob   | 1       | 75000  | Alice      | Grace         |
| Grace | 1       | 75000  | Alice      | Grace         |
| Carol | 2       | 85000  | Carol      | Hank          |
| David | 2       | 60000  | Carol      | Hank          |
| Hank  | 2       | 60000  | Carol      | Hank          |
| Eve   | 3       | 95000  | Eve        | Frank         |
| Jack  | 3       | 90000  | Eve        | Frank         |
| Frank | 3       | 70000  | Eve        | Frank         |

---

### Q87. NTILE — Divide employees into salary quartiles

📌 **New Concept — NTILE(n):** Divides rows into `n` roughly equal buckets and assigns each row a bucket number (1 to n). Rows are distributed based on the `ORDER BY` in the window.

```sql
SELECT name, salary,
       NTILE(4) OVER(ORDER BY salary) AS salary_quartile
FROM employees WHERE dept_id IS NOT NULL;
```

**Output:**
| name  | salary | salary_quartile |
|-------|--------|-----------------|
| David | 60000  | 1               |
| Hank  | 60000  | 1               |
| Frank | 70000  | 1               |
| Bob   | 75000  | 2               |
| Grace | 75000  | 2               |
| Carol | 85000  | 3               |
| Alice | 90000  | 3               |
| Jack  | 90000  | 4               |
| Eve   | 95000  | 4               |

---

### Q88. Department salary vs company average (no GROUP BY collapse)

```sql
SELECT name, dept_id, salary,
       ROUND(AVG(salary) OVER(), 2)                    AS company_avg,
       ROUND(AVG(salary) OVER(PARTITION BY dept_id), 2) AS dept_avg,
       salary - AVG(salary) OVER()                     AS diff_from_avg
FROM employees WHERE dept_id IS NOT NULL;
```

**Output:**
| name  | dept_id | salary | company_avg | dept_avg | diff_from_avg |
|-------|---------|--------|-------------|----------|---------------|
| Alice | 1       | 90000  | 78888.89    | 80000.00 | 11111.11      |
| Bob   | 1       | 75000  | 78888.89    | 80000.00 | -3888.89      |
| Grace | 1       | 75000  | 78888.89    | 80000.00 | -3888.89      |
| Carol | 2       | 85000  | 78888.89    | 68333.33 | 6111.11       |
| ...   | ...     | ...    | ...         | ...      | ...           |

---

### Q89. Top 1 product per category by revenue

```sql
SELECT * FROM (
    SELECT p.category, p.product_name, SUM(o.amount) AS revenue,
           ROW_NUMBER() OVER(PARTITION BY p.category ORDER BY SUM(o.amount) DESC) AS rn
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category, p.product_name
) t WHERE rn = 1;
```

**Output:**
| category    | product_name  | revenue | rn |
|-------------|---------------|---------|----|
| Books       | Java Book     | 1600    | 1  |
| Electronics | Laptop Pro    | 150000  | 1  |
| Furniture   | Standing Desk | 50000   | 1  |

---

### Q90. Delete duplicates keeping highest salary row (ROW_NUMBER)

```sql
-- (Demonstration — add duplicate first)
INSERT INTO employees VALUES (11, 'Alice', 1, 88000, 1, '2023-01-01', 'Mumbai');

DELETE FROM employees
WHERE emp_id NOT IN (
    SELECT emp_id FROM (
        SELECT emp_id,
               ROW_NUMBER() OVER(PARTITION BY name ORDER BY salary DESC) AS rn
        FROM employees
    ) t WHERE rn = 1
);
-- Alice with 90000 is kept; Alice with 88000 is deleted.
```

---

### Q91. Year-over-year revenue growth

```sql
WITH yearly AS (
    SELECT YEAR(order_date) AS yr, SUM(amount) AS revenue
    FROM orders GROUP BY YEAR(order_date)
)
SELECT yr, revenue,
       LAG(revenue) OVER(ORDER BY yr) AS prev_year_revenue,
       ROUND((revenue - LAG(revenue) OVER(ORDER BY yr)) * 100.0
             / LAG(revenue) OVER(ORDER BY yr), 2) AS yoy_pct
FROM yearly;
```

**Output (with only 2024 data):**
| yr   | revenue | prev_year_revenue | yoy_pct |
|------|---------|-------------------|---------|
| 2024 | 217800  | NULL              | NULL    |

> Two years of data needed to show growth. With a 2023 dataset, the YoY column would populate.

---

## SECTION 2 — CTEs (Q92–Q101)

---

### Q92. Basic CTE — Employees above department average salary

📌 **New Concept — CTE (Common Table Expression):** A named temporary result set defined with `WITH`. It exists only for the duration of the query. Makes complex queries more readable by breaking them into named logical steps.

```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary, ROUND(d.avg_salary, 2) AS dept_avg
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_salary;
```

**Output:**
| name  | salary | dept_avg  |
|-------|--------|-----------|
| Alice | 90000  | 80000.00  |
| Carol | 85000  | 68333.33  |
| Eve   | 95000  | 85000.00  |
| Jack  | 90000  | 85000.00  |

---

### Q93. Multiple CTEs in one query

```sql
WITH
high_earners AS (
    SELECT dept_id, COUNT(*) AS high_count
    FROM employees WHERE salary > 80000
    GROUP BY dept_id
),
dept_total AS (
    SELECT dept_id, COUNT(*) AS total_count
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_id,
       ht.high_count,
       dt.total_count,
       ROUND(ht.high_count * 100.0 / dt.total_count, 1) AS pct_high
FROM departments d
JOIN dept_total dt ON d.dept_id = dt.dept_id
LEFT JOIN high_earners ht ON d.dept_id = ht.dept_id;
```

**Output:**
| dept_id | high_count | total_count | pct_high |
|---------|------------|-------------|----------|
| 1       | 1          | 3           | 33.3     |
| 2       | 1          | 3           | 33.3     |
| 3       | 2          | 3           | 66.7     |

---

### Q94. Recursive CTE — Employee hierarchy under Eve (emp_id=5)

```sql
WITH RECURSIVE subordinates AS (
    SELECT emp_id, name, manager_id, 0 AS depth
    FROM employees WHERE emp_id = 5
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, s.depth + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.emp_id
)
SELECT * FROM subordinates;
```

**Output:**
| emp_id | name  | manager_id | depth |
|--------|-------|------------|-------|
| 5      | Eve   | NULL       | 0     |
| 6      | Frank | 5          | 1     |
| 10     | Jack  | 5          | 1     |

---

### Q95. CTE for pagination with total count

📌 **New Concept — COUNT(*) OVER():** A window function that counts **all rows** in the entire result (no partition). Used to get total row count alongside paginated rows in a single query.

```sql
WITH paginated AS (
    SELECT *, COUNT(*) OVER() AS total_rows
    FROM orders
    WHERE status = 'DELIVERED'
),
paged AS (
    SELECT *, ROW_NUMBER() OVER(ORDER BY order_date DESC) AS rn FROM paginated
)
SELECT * FROM paged WHERE rn BETWEEN 1 AND 5;
```

**Output:**
| order_id | customer_id | amount | status    | order_date | total_rows | rn |
|----------|-------------|--------|-----------|------------|------------|----|
| 109      | 1           | 800    | DELIVERED | 2024-05-20 | 6          | 1  |
| 107      | 5           | 1200   | DELIVERED | 2024-04-15 | 6          | 2  |
| 106      | 4           | 25000  | DELIVERED | 2024-04-02 | 6          | 3  |
| 104      | 3           | 800    | DELIVERED | 2024-03-05 | 6          | 4  |
| 102      | 1           | 1500   | DELIVERED | 2024-02-14 | 6          | 5  |

---

### Q96. Cumulative % of orders per customer

```sql
SELECT customer_id, COUNT(*) AS order_count,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;
```

**Output:**
| customer_id | order_count | pct_of_total |
|-------------|-------------|--------------|
| 1           | 3           | 30.00        |
| 2           | 2           | 20.00        |
| 3           | 2           | 20.00        |
| 4           | 2           | 20.00        |
| 5           | 1           | 10.00        |

---

### Q97. Gap and Island — Consecutive order dates

```sql
WITH numbered AS (
    SELECT DISTINCT DATE(order_date) AS odate,
           ROW_NUMBER() OVER(ORDER BY DATE(order_date)) AS rn
    FROM orders
),
grouped AS (
    SELECT odate, DATE_SUB(odate, INTERVAL rn DAY) AS grp
    FROM numbered
)
SELECT MIN(odate) AS start_date, MAX(odate) AS end_date, COUNT(*) AS days
FROM grouped
GROUP BY grp
ORDER BY start_date;
```

**Output (with our non-consecutive dates):**
| start_date | end_date   | days |
|------------|------------|------|
| 2024-01-10 | 2024-01-10 | 1    |
| 2024-01-20 | 2024-01-20 | 1    |
| 2024-02-14 | 2024-02-14 | 1    |
| ...        | ...        | ...  |

> Each order date is isolated → each forms its own "island" of 1 day.

---

## SECTION 3 — QUERY OPTIMIZATION (Q98–Q115)

---

### Q98. Function on indexed column — Kills index

```sql
-- ❌ SLOW: YEAR() wraps the column — optimizer can't use index on hire_date
EXPLAIN SELECT * FROM employees WHERE YEAR(hire_date) = 2020;
-- Result: type = ALL (full table scan)

-- ✅ FAST: Range condition allows index scan
EXPLAIN SELECT * FROM employees
WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31';
-- Result: type = range (index used if index exists on hire_date)
```

**Output of bad query:** Scans all 10 rows.
**Output of good query (with index):** Scans only 2020 rows.

---

### Q99. Leading wildcard kills LIKE index usage

```sql
-- ❌ Cannot use index (no leftmost prefix to anchor):
SELECT * FROM customers WHERE name LIKE '%rah%';

-- ✅ Can use index (prefix anchored):
SELECT * FROM customers WHERE name LIKE 'Rah%';
```

**Output of `LIKE 'Rah%'`:**
| customer_id | name  | city   |
|-------------|-------|--------|
| 1           | Rahul | Mumbai |

---

### Q100. EXISTS vs COUNT — For checking existence

```sql
-- ❌ Slower: Counts all matching rows unnecessarily
SELECT COUNT(*) > 0 FROM orders WHERE customer_id = 6;

-- ✅ Faster: Stops at first match
SELECT EXISTS(SELECT 1 FROM orders WHERE customer_id = 6) AS has_orders;
```

**Output:**
| has_orders |
|------------|
| 0          |

> Nisha (customer_id=6) has no orders.

---

### Q101. HAVING vs WHERE — Filter placement matters

```sql
-- ❌ HAVING for non-aggregate condition (runs after aggregation — wasteful):
SELECT dept_id, AVG(salary) FROM employees
GROUP BY dept_id HAVING dept_id IS NOT NULL;

-- ✅ WHERE filters before aggregation (less data to group):
SELECT dept_id, AVG(salary) FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id;
```

**Output (both give same result):**
| dept_id | AVG(salary) |
|---------|-------------|
| 1       | 80000.00    |
| 2       | 68333.33    |
| 3       | 85000.00    |

---

## SECTION 4 — DEBUG THE QUERY (Q102–Q115)

---

### Q102. Bug: NOT IN with NULL subquery — Empty result

```sql
-- ❌ BUG: If subquery returns ANY NULL, NOT IN always returns empty!
SELECT name FROM employees
WHERE dept_id NOT IN (SELECT dept_id FROM employees);
-- dept_id column has NULL for Ivy → subquery returns NULL → NOT IN with NULL = always UNKNOWN

-- ✅ FIX: Use NOT EXISTS which handles NULLs correctly
SELECT e.name FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM departments d WHERE d.dept_id = e.dept_id
);
```

**Buggy Output:** *(Empty — 0 rows)*

**Fixed Output:**
| name |
|------|
| Ivy  |

---

### Q103. Bug: WHERE on RIGHT table in LEFT JOIN

```sql
-- ❌ BUG: Turns LEFT JOIN into INNER JOIN
SELECT e.name, d.dept_name FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location = 'Mumbai';

-- ✅ FIX: Move condition to ON clause
SELECT e.name, d.dept_name FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id AND d.location = 'Mumbai';
```

**Buggy Output:** Only 3 rows (Alice, Bob, Grace). Ivy disappears.

**Fixed Output:** All 10 employees shown, non-Mumbai departments show `dept_name = NULL`.

---

### Q104. Bug: NULL comparison with =

```sql
-- ❌ BUG: Always returns 0 rows!
SELECT * FROM employees WHERE manager_id = NULL;

-- ✅ FIX:
SELECT * FROM employees WHERE manager_id IS NULL;
```

**Buggy Output:** *(Empty)*

**Fixed Output:**
| name  | manager_id |
|-------|------------|
| Alice | NULL       |
| Carol | NULL       |
| Eve   | NULL       |
| Ivy   | NULL       |

---

### Q105. Bug: GROUP BY with non-aggregated column

```sql
-- ❌ ERROR in MySQL strict mode / PostgreSQL:
SELECT dept_id, name, MAX(salary)
FROM employees GROUP BY dept_id;

-- ✅ FIX — Include name in GROUP BY (get unique dept+name combos):
SELECT dept_id, name, salary FROM employees
WHERE (dept_id, salary) IN (
    SELECT dept_id, MAX(salary) FROM employees GROUP BY dept_id
);
```

**Fixed Output:**
| dept_id | name  | salary |
|---------|-------|--------|
| 1       | Alice | 90000  |
| 2       | Carol | 85000  |
| 3       | Eve   | 95000  |

---

### Q106. Bug: BETWEEN with DATETIME — Misses end of day

```sql
-- ❌ Misses records after 2024-03-18 00:00:00 on that day:
SELECT * FROM orders WHERE order_date BETWEEN '2024-03-05' AND '2024-03-18';

-- ✅ FIX:
SELECT * FROM orders
WHERE order_date >= '2024-03-05' AND order_date < '2024-03-19';
```

**Output (both — with DATE columns in our dataset):**
| order_id | order_date | amount |
|----------|------------|--------|
| 104      | 2024-03-05 | 800    |
| 105      | 2024-03-18 | 75000  |

---

### Q107. Bug: Division by zero without NULLIF

```sql
-- ❌ Crashes with division by zero if any customer has 0 orders:
SELECT customer_id, total_amount / total_orders AS avg_order
FROM customer_summary;

-- ✅ FIX:
SELECT customer_id, total_amount / NULLIF(total_orders, 0) AS avg_order
FROM customer_summary;
-- NULLIF(0, 0) returns NULL → NULL / anything = NULL (no crash)
```

---

## SECTION 5 — DATABASE DESIGN (Q108–Q130)

---

### Q108. E-commerce schema (interview standard)

```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100), phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE addresses (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT REFERENCES users(user_id),
    type ENUM('HOME','WORK'), street TEXT, city VARCHAR(50), pincode VARCHAR(10)
);
CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    parent_id INT REFERENCES categories(category_id) -- Self-referential for subcategories
);
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200), category_id INT REFERENCES categories(category_id),
    price DECIMAL(10,2), stock INT DEFAULT 0,
    status ENUM('ACTIVE','INACTIVE','OUT_OF_STOCK')
);
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT REFERENCES users(user_id),
    shipping_address_id INT REFERENCES addresses(address_id),
    total_amount DECIMAL(10,2),
    status ENUM('PENDING','CONFIRMED','SHIPPED','DELIVERED','CANCELLED'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT, price_at_purchase DECIMAL(10,2) -- Snapshot at time of purchase!
);
```

**Interview follow-up:** "Why store `price_at_purchase` instead of joining products.price?"
→ Product prices change over time. Storing price at purchase preserves historical accuracy.

---

### Q109. WhatsApp schema

```sql
CREATE TABLE users (user_id INT PK, phone VARCHAR(15) UNIQUE, name VARCHAR(100));
CREATE TABLE chats (chat_id INT PK AUTO_INCREMENT, type ENUM('PERSONAL','GROUP'), created_at TIMESTAMP);
CREATE TABLE chat_members (
    chat_id INT FK → chats, user_id INT FK → users,
    joined_at TIMESTAMP, role ENUM('MEMBER','ADMIN'),
    PRIMARY KEY(chat_id, user_id)
);
CREATE TABLE messages (
    message_id BIGINT PK AUTO_INCREMENT,
    chat_id INT FK → chats, sender_id INT FK → users,
    content TEXT, type ENUM('TEXT','IMAGE','VIDEO'),
    sent_at TIMESTAMP,
    INDEX(chat_id, sent_at)  -- Critical index for fetching chat history in order
);
CREATE TABLE message_status (
    message_id BIGINT FK, user_id INT FK,
    status ENUM('SENT','DELIVERED','READ'), updated_at TIMESTAMP,
    PRIMARY KEY(message_id, user_id)
);
```

**Scale question:** "How to scale to 2B users?"
→ Shard by `chat_id`. Cassandra for messages (time-series write-heavy). Redis for presence. CDN for media.

---

### Q110. Hospital schema

```sql
CREATE TABLE doctors (doctor_id INT PK, name VARCHAR(100), specialty VARCHAR(100), license_no VARCHAR(50) UNIQUE);
CREATE TABLE patients (patient_id INT PK, name VARCHAR(100), dob DATE, blood_group VARCHAR(5), phone VARCHAR(15));
CREATE TABLE appointments (
    appt_id INT PK AUTO_INCREMENT,
    patient_id INT FK, doctor_id INT FK,
    scheduled_at DATETIME,
    status ENUM('BOOKED','COMPLETED','CANCELLED','NO_SHOW'),
    notes TEXT
);
CREATE TABLE prescriptions (
    rx_id INT PK AUTO_INCREMENT, appt_id INT FK,
    medicine_name VARCHAR(200), dosage VARCHAR(100), duration VARCHAR(50)
);
```

---

### Q111. Customers who spent more than average customer spending

```sql
WITH customer_spending AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders GROUP BY customer_id
),
avg_spend AS (
    SELECT AVG(total_spent) AS avg FROM customer_spending
)
SELECT c.name, cs.total_spent
FROM customers c
JOIN customer_spending cs ON c.customer_id = cs.customer_id
CROSS JOIN avg_spend
WHERE cs.total_spent > avg_spend.avg
ORDER BY cs.total_spent DESC;
```

**Output (avg = 217800/5 = 43560):**
| name  | total_spent |
|-------|-------------|
| Sneha | 100000      |
| Rahul | 77300       |

---

### Q112. Median salary (MySQL — no MEDIAN function)

```sql
WITH ranked AS (
    SELECT salary,
           ROW_NUMBER() OVER(ORDER BY salary) AS rn,
           COUNT(*) OVER() AS total
    FROM employees WHERE dept_id IS NOT NULL
)
SELECT ROUND(AVG(salary), 2) AS median
FROM ranked
WHERE rn IN (FLOOR((total + 1) / 2), CEIL((total + 1) / 2));
```

**Output (9 employees sorted: 60,60,70,75,75,85,90,90,95 → median position 5):**
| median  |
|---------|
| 75000.00|

---

### Q113. Output Prediction — Window vs GROUP BY

```sql
-- Query A:
SELECT dept_id, SUM(salary) FROM employees GROUP BY dept_id;

-- Query B:
SELECT dept_id, SUM(salary) OVER(PARTITION BY dept_id) AS dept_total FROM employees;
```

**Query A Output:** 4 rows (one per group):
| dept_id | SUM(salary) |
|---------|-------------|
| 1       | 240000      |
| 2       | 205000      |
| 3       | 255000      |
| NULL    | 55000       |

**Query B Output:** 10 rows (one per employee, with dept total repeated):
| dept_id | dept_total |
|---------|------------|
| Alice→1 | 240000     |
| Bob→1   | 240000     |
| Grace→1 | 240000     |
| Carol→2 | 205000     |
| ...     | ...        |

> **Key difference:** GROUP BY collapses rows into groups. Window functions keep all rows and add the aggregate as a new column.

---

### Q114–Q130: Additional Query Outputs

**Q114. Count orders per customer — include 0 for no orders**
```sql
SELECT c.name, COALESCE(COUNT(o.order_id), 0) AS order_count
FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```
| name   | order_count |
|--------|-------------|
| Rahul  | 3           |
| Priya  | 2           |
| Arun   | 2           |
| Sneha  | 2           |
| Vikram | 1           |
| Nisha  | 0           |

**Q115. Find consecutive order dates (output prediction)**
```sql
SELECT order_date, COUNT(*) AS orders_on_day
FROM orders GROUP BY DATE(order_date) HAVING COUNT(*) > 1;
```
| order_date | orders_on_day |
|---|---|
| *(empty — no date has more than 1 order in our dataset)* | |

**Q116. Top product by revenue**
```sql
SELECT p.product_name, SUM(o.amount) AS revenue
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name ORDER BY revenue DESC LIMIT 3;
```
| product_name  | revenue |
|---------------|---------|
| Laptop Pro    | 150000  |
| Standing Desk | 50000   |
| Office Chair  | 12000   |

**Q117. Cohort — Customer first-order month**
```sql
SELECT DATE_FORMAT(MIN(order_date), '%Y-%m') AS first_order_month,
       COUNT(DISTINCT customer_id) AS new_customers
FROM orders GROUP BY customer_id
ORDER BY first_order_month;
```
| first_order_month | new_customers |
|---|---|
| 2024-01 | 2 |
| 2024-03 | 2 |
| 2024-04 | 1 |

**Q118. Employees by city — pivot across departments**
```sql
SELECT city,
    SUM(CASE WHEN dept_id = 1 THEN 1 ELSE 0 END) AS engineering,
    SUM(CASE WHEN dept_id = 2 THEN 1 ELSE 0 END) AS marketing,
    SUM(CASE WHEN dept_id = 3 THEN 1 ELSE 0 END) AS sales
FROM employees GROUP BY city;
```
| city      | engineering | marketing | sales |
|-----------|-------------|-----------|-------|
| Mumbai    | 3           | 0         | 0     |
| Delhi     | 0           | 3         | 0     |
| Bangalore | 0           | 0         | 3     |
| Pune      | 0           | 0         | 0     |
