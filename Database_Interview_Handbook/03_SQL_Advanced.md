# SQL Advanced — Q81 to Q200+
## Window Functions, CTEs, Optimization, DB Design, Debug Queries

---

## WINDOW FUNCTIONS — Q81 to Q110

### Q81. ROW_NUMBER — Assign unique row numbers within each department
```sql
SELECT name, dept_id, salary,
       ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS row_num
FROM employees;
```

---

### Q82. RANK vs DENSE_RANK — Side-by-side comparison
```sql
SELECT name, salary,
       RANK()        OVER(ORDER BY salary DESC) AS rnk,       -- gaps after tie
       DENSE_RANK()  OVER(ORDER BY salary DESC) AS dense_rnk, -- no gaps
       ROW_NUMBER()  OVER(ORDER BY salary DESC) AS row_num     -- always unique
FROM employees;
-- For salary: 90k, 90k, 80k
-- RANK:        1,  1,  3
-- DENSE_RANK:  1,  1,  2
-- ROW_NUMBER:  1,  2,  3
```

---

### Q83. LAG and LEAD — Compare current row with previous/next
```sql
SELECT order_date, amount,
       LAG(amount, 1) OVER(ORDER BY order_date) AS prev_day_amount,
       LEAD(amount, 1) OVER(ORDER BY order_date) AS next_day_amount,
       amount - LAG(amount, 1) OVER(ORDER BY order_date) AS day_over_day_change
FROM orders;
```

---

### Q84. Running total using SUM window function
```sql
SELECT order_date, amount,
       SUM(amount) OVER(ORDER BY order_date) AS running_total
FROM orders;
```

---

### Q85. Moving average (7-day rolling average)
```sql
SELECT order_date, amount,
       AVG(amount) OVER(
           ORDER BY order_date
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) AS moving_avg_7day
FROM orders;
```

---

### Q86. First and Last value in each department
```sql
SELECT name, dept_id, salary,
       FIRST_VALUE(name) OVER(PARTITION BY dept_id ORDER BY salary DESC) AS highest_paid,
       LAST_VALUE(name)  OVER(PARTITION BY dept_id ORDER BY salary DESC
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS lowest_paid
FROM employees;
-- TRAP: LAST_VALUE needs explicit frame clause — default frame stops at current row!
```

---

### Q87. NTILE — Divide employees into salary quartiles
```sql
SELECT name, salary,
       NTILE(4) OVER(ORDER BY salary) AS salary_quartile
FROM employees;
-- Q1 = lowest 25%, Q4 = highest 25%
```

---

### Q88. Percentage rank (percentile)
```sql
SELECT name, salary,
       PERCENT_RANK() OVER(ORDER BY salary) AS percentile,
       CUME_DIST()    OVER(ORDER BY salary) AS cumulative_dist
FROM employees;
-- PERCENT_RANK: 0 to 1 (excludes last rank)
-- CUME_DIST: fraction of rows <= current row
```

---

### Q89. Window function — Department salary compared to company average
```sql
SELECT name, dept_id, salary,
       AVG(salary) OVER() AS company_avg,
       AVG(salary) OVER(PARTITION BY dept_id) AS dept_avg,
       salary - AVG(salary) OVER() AS diff_from_company_avg
FROM employees;
```

---

### Q90. Remove duplicates keeping highest salary row (using ROW_NUMBER)
```sql
DELETE FROM employees
WHERE emp_id NOT IN (
    SELECT emp_id FROM (
        SELECT emp_id,
               ROW_NUMBER() OVER(PARTITION BY email ORDER BY salary DESC) AS rn
        FROM employees
    ) t WHERE rn = 1
);
```

---

### Q91. Employees who joined consecutively within 30 days (LAG)
```sql
SELECT emp_id, name, hire_date,
       LAG(hire_date) OVER(ORDER BY hire_date) AS prev_hire_date,
       DATEDIFF(hire_date, LAG(hire_date) OVER(ORDER BY hire_date)) AS days_gap
FROM employees
HAVING days_gap <= 30;
```

---

### Q92. Year-over-year revenue growth
```sql
WITH yearly AS (
    SELECT YEAR(order_date) AS yr, SUM(amount) AS revenue
    FROM orders GROUP BY YEAR(order_date)
)
SELECT yr, revenue,
       LAG(revenue) OVER(ORDER BY yr) AS prev_year_revenue,
       ROUND((revenue - LAG(revenue) OVER(ORDER BY yr)) * 100.0 / LAG(revenue) OVER(ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly;
```

---

### Q93. Top 1 product per category by revenue
```sql
SELECT * FROM (
    SELECT p.category, p.product_name, SUM(o.amount) AS revenue,
           ROW_NUMBER() OVER(PARTITION BY p.category ORDER BY SUM(o.amount) DESC) AS rn
    FROM orders o JOIN products p ON o.product_id = p.product_id
    GROUP BY p.category, p.product_name
) t WHERE rn = 1;
```

---

### Q94. Cumulative percentage of orders per customer
```sql
SELECT customer_id, COUNT(*) AS order_count,
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS pct_of_total_orders
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;
```

---

### Q95. Gap and Island problem — Find consecutive date ranges
```sql
WITH numbered AS (
    SELECT order_date,
           ROW_NUMBER() OVER(ORDER BY order_date) AS rn
    FROM (SELECT DISTINCT DATE(order_date) AS order_date FROM orders) d
),
grouped AS (
    SELECT order_date,
           DATE_SUB(order_date, INTERVAL rn DAY) AS grp
    FROM numbered
)
SELECT MIN(order_date) AS period_start,
       MAX(order_date) AS period_end,
       COUNT(*) AS consecutive_days
FROM grouped
GROUP BY grp
ORDER BY period_start;
```

---

## CTEs — Q96 to Q110

### Q96. Basic CTE — Average salary by department
```sql
WITH dept_avg AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT e.name, e.salary, d.avg_salary
FROM employees e
JOIN dept_avg d ON e.dept_id = d.dept_id
WHERE e.salary > d.avg_salary;
```

---

### Q97. Multiple CTEs in one query
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
       ROUND(ht.high_count * 100.0 / dt.total_count, 2) AS pct_high_earners
FROM departments d
JOIN dept_total dt ON d.dept_id = dt.dept_id
JOIN high_earners ht ON d.dept_id = ht.dept_id;
```

---

### Q98. Recursive CTE — Fibonacci sequence
```sql
WITH RECURSIVE fib(n, a, b) AS (
    SELECT 1, 0, 1
    UNION ALL
    SELECT n + 1, b, a + b FROM fib WHERE n < 10
)
SELECT n, a AS fibonacci FROM fib;
```

---

### Q99. CTE vs Subquery — When to use which?
```sql
-- Same result, different readability:

-- Subquery (harder to read for complex logic):
SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);

-- CTE (self-documenting, reusable):
WITH avg_salary AS (SELECT AVG(salary) AS avg FROM employees)
SELECT * FROM employees e, avg_salary a WHERE e.salary > a.avg;

-- Key: CTEs improve readability. Use them for complex, multi-step queries.
-- Performance: In most databases, CTEs are NOT automatically materialized (they're just syntax sugar for subqueries), so performance is similar.
```

---

### Q100. Recursive CTE — Find all subordinates of a manager
```sql
WITH RECURSIVE subordinates AS (
    SELECT emp_id, name, manager_id, 1 AS depth
    FROM employees WHERE emp_id = 10  -- Start from manager ID 10
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, s.depth + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.emp_id
    WHERE s.depth < 10  -- Prevent infinite loop
)
SELECT * FROM subordinates ORDER BY depth;
```

---

### Q101. CTE for pagination with total count
```sql
WITH paginated AS (
    SELECT *, COUNT(*) OVER() AS total_rows
    FROM orders
    WHERE status = 'PENDING'
),
page AS (
    SELECT *, ROW_NUMBER() OVER(ORDER BY order_date DESC) AS rn
    FROM paginated
)
SELECT * FROM page WHERE rn BETWEEN 21 AND 40;  -- Page 2 (20 per page)
```

---

## QUERY OPTIMIZATION — Q102 to Q120

### Q102. Identify why this query is slow and fix it
```sql
-- SLOW: Function on indexed column prevents index use
SELECT * FROM orders WHERE DATE(order_date) = '2024-01-15';

-- FAST: Range condition allows index scan
SELECT * FROM orders 
WHERE order_date >= '2024-01-15 00:00:00' 
  AND order_date <  '2024-01-16 00:00:00';
```

---

### Q103. Why is SELECT * bad in production?
```sql
-- Problems with SELECT *:
-- 1. Fetches unnecessary columns (network + memory overhead)
-- 2. Breaks queries when columns are added/reordered
-- 3. Prevents covering index optimization
-- 4. Harder to understand what data is actually used

-- Always specify columns:
SELECT customer_id, name, email FROM customers WHERE city = 'Mumbai';
```

---

### Q104. Using FORCE INDEX (when optimizer makes wrong choice)
```sql
-- Force a specific index
SELECT * FROM orders FORCE INDEX (idx_order_date) WHERE order_date > '2024-01-01';

-- Or ignore a bad index choice:
SELECT * FROM orders IGNORE INDEX (idx_status) WHERE status = 'PENDING';
```

---

### Q105. Optimize a COUNT DISTINCT query
```sql
-- Slow for large tables:
SELECT COUNT(DISTINCT customer_id) FROM orders;

-- Faster (using approximate count with HyperLogLog in some DBs):
-- Or: Use a covering index on customer_id
CREATE INDEX idx_cust ON orders(customer_id);
SELECT COUNT(DISTINCT customer_id) FROM orders;  -- Now uses index
```

---

### Q106. Query that creates a temporary table bottleneck
```sql
-- Creates temp table (bad for GROUP BY on large data):
SELECT * FROM (
    SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id
) t WHERE avg_salary > 50000;  -- ❌ Can't push WHERE into subquery

-- Fix with HAVING:
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 50000;  -- Filter happens during aggregation
```

---

### Q107. Optimal way to check existence (COUNT vs EXISTS)
```sql
-- SLOW: Counts all matching rows (unnecessary work)
SELECT COUNT(*) > 0 FROM orders WHERE customer_id = 5;

-- FAST: EXISTS stops at first match
SELECT EXISTS(SELECT 1 FROM orders WHERE customer_id = 5);
```

---

### Q108. LIKE optimization — Prefix vs suffix search
```sql
-- Uses index (prefix pattern):
SELECT * FROM customers WHERE name LIKE 'Raj%';

-- CANNOT use index (leading wildcard):
SELECT * FROM customers WHERE name LIKE '%kumar';

-- FIX for suffix search: Store reversed name in another column and search that!
SELECT * FROM customers WHERE name_reversed LIKE REVERSE('%kumar');
```

---

### Q109. Join order optimization
```sql
-- Most restrictive filter should limit rows early
-- BAD: Join large tables first
SELECT * FROM orders o JOIN order_details od ON o.id = od.order_id WHERE o.customer_id = 5;

-- GOOD: Filter customer orders first (smaller result set for subsequent join)
SELECT * FROM (SELECT * FROM orders WHERE customer_id = 5) o 
JOIN order_details od ON o.id = od.order_id;
```

---

### Q110. Avoid HAVING for non-aggregate filtering
```sql
-- SLOW: HAVING re-filters after GROUP BY
SELECT dept_id, AVG(salary) FROM employees
GROUP BY dept_id
HAVING dept_id > 2;  -- Not an aggregate condition!

-- FAST: Use WHERE before grouping
SELECT dept_id, AVG(salary) FROM employees
WHERE dept_id > 2  -- Applied before GROUP BY
GROUP BY dept_id;
```

---

## DEBUG THE QUERY — Q111 to Q130

### Q111. Bug: HAVING without GROUP BY
```sql
-- WRONG:
SELECT name FROM employees HAVING salary > 50000;
-- HAVING without GROUP BY is valid in MySQL but unreliable in standard SQL

-- FIX:
SELECT name FROM employees WHERE salary > 50000;
```

---

### Q112. Bug: Ambiguous column name in JOIN
```sql
-- ERROR: Column 'dept_id' is ambiguous
SELECT name, dept_id FROM employees e JOIN departments d ON e.dept_id = d.dept_id;

-- FIX: Qualify with table alias
SELECT e.name, e.dept_id FROM employees e JOIN departments d ON e.dept_id = d.dept_id;
```

---

### Q113. Bug: Wrong join creates Cartesian product
```sql
-- BUG: Missing JOIN condition — full Cartesian product!
SELECT * FROM employees, departments;
-- 500 employees × 10 departments = 5000 rows!

-- FIX: Add ON clause
SELECT * FROM employees e JOIN departments d ON e.dept_id = d.dept_id;
```

---

### Q114. Bug: UPDATE without WHERE — destroys all data
```sql
-- EXTREMELY DANGEROUS:
UPDATE employees SET salary = 0;  -- Sets ALL employees' salaries to 0!

-- FIX:
UPDATE employees SET salary = 0 WHERE emp_id = 5;

-- Best practice: Always SELECT first to verify which rows you'll affect
SELECT * FROM employees WHERE emp_id = 5;
-- Then UPDATE
```

---

### Q115. Bug: Incorrect NULL comparison
```sql
-- WRONG (always returns empty result!):
SELECT * FROM employees WHERE manager_id = NULL;

-- FIX:
SELECT * FROM employees WHERE manager_id IS NULL;

-- Trap: NULL = NULL is NULL (not TRUE)
```

---

### Q116. Bug: IN with NULL values behaves unexpectedly
```sql
-- If dept_id_list contains NULL:
SELECT * FROM employees WHERE dept_id NOT IN (1, 2, NULL);
-- Returns EMPTY RESULT! Because NOT IN with NULL uses NOT (x=1 OR x=2 OR x=NULL)
-- x=NULL is UNKNOWN, so whole expression becomes UNKNOWN

-- FIX: Use NOT IN without NULLs, or use NOT EXISTS
SELECT * FROM employees e WHERE NOT EXISTS (
    SELECT 1 FROM dept_exclude d WHERE d.dept_id = e.dept_id
);
```

---

### Q117. Bug: GROUP BY with non-aggregated columns
```sql
-- ERROR in strict SQL:
SELECT dept_id, name, MAX(salary) FROM employees GROUP BY dept_id;
-- 'name' is neither aggregated nor in GROUP BY

-- FIX Option 1: Add name to GROUP BY (if you want unique name+dept combos)
SELECT dept_id, name, MAX(salary) FROM employees GROUP BY dept_id, name;

-- FIX Option 2: Use window function
SELECT dept_id, name, salary, MAX(salary) OVER(PARTITION BY dept_id) AS dept_max
FROM employees;
```

---

### Q118. Bug: Off-by-one in date range
```sql
-- WRONG: Misses records from Dec 31 at time > 00:00:00
SELECT * FROM orders WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';
-- For DATETIME: 2024-12-31 23:59:59 is NOT between ... AND '2024-12-31 00:00:00'

-- FIX:
SELECT * FROM orders 
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';
```

---

### Q119. Performance Bug: Implicit type conversion kills index
```sql
-- employee_id is INT, but string passed — forces implicit conversion on all rows!
SELECT * FROM employees WHERE emp_id = '5';  -- May not use index

-- FIX:
SELECT * FROM employees WHERE emp_id = 5;
```

---

### Q120. Bug: Division by zero
```sql
-- CRASH:
SELECT total_sales / total_orders FROM monthly_summary;  -- Crash if orders = 0

-- FIX using NULLIF:
SELECT total_sales / NULLIF(total_orders, 0) AS avg_order_value FROM monthly_summary;
-- NULLIF returns NULL instead of dividing by zero
```

---

## DATABASE DESIGN — Q121 to Q150

### Q121. Design an E-commerce database schema
```sql
-- Core tables:
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE addresses (
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT REFERENCES users(user_id),
    type ENUM('HOME','WORK','OTHER'),
    street TEXT, city VARCHAR(50), state VARCHAR(50), pincode VARCHAR(10)
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    parent_category_id INT REFERENCES categories(category_id)  -- Self-referential for subcategories
);

CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200),
    category_id INT REFERENCES categories(category_id),
    seller_id INT REFERENCES users(user_id),
    price DECIMAL(10,2),
    stock INT DEFAULT 0,
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
    quantity INT,
    price_at_purchase DECIMAL(10,2)  -- Snapshot of price at time of purchase
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT REFERENCES orders(order_id),
    method ENUM('CARD','UPI','COD','NETBANKING'),
    status ENUM('PENDING','SUCCESS','FAILED','REFUNDED'),
    amount DECIMAL(10,2),
    transaction_id VARCHAR(100)
);
```

---

### Q122. Design a WhatsApp/Messaging system
```sql
CREATE TABLE users (user_id INT PK, phone VARCHAR(15) UNIQUE, name VARCHAR(100));

CREATE TABLE chats (
    chat_id INT PK AUTO_INCREMENT,
    type ENUM('PERSONAL','GROUP'),
    created_at TIMESTAMP
);

CREATE TABLE chat_members (
    chat_id INT FK → chats,
    user_id INT FK → users,
    joined_at TIMESTAMP,
    role ENUM('MEMBER','ADMIN'),
    PRIMARY KEY(chat_id, user_id)
);

CREATE TABLE messages (
    message_id BIGINT PK AUTO_INCREMENT,
    chat_id INT FK → chats,
    sender_id INT FK → users,
    content TEXT,
    type ENUM('TEXT','IMAGE','VIDEO','DOCUMENT'),
    sent_at TIMESTAMP,
    INDEX(chat_id, sent_at)  -- Critical for fetching chat history in order
);

CREATE TABLE message_status (
    message_id BIGINT FK → messages,
    user_id INT FK → users,
    status ENUM('SENT','DELIVERED','READ'),
    timestamp TIMESTAMP,
    PRIMARY KEY(message_id, user_id)
);
```

**Interview Follow-up:** "How would you scale this to 2 billion users?"
→ Shard by `chat_id`. Use Cassandra for messages (write-heavy, time-series). Use Redis for online presence. Use CDN for media.

---

### Q123. Design a Hospital Management System
```sql
CREATE TABLE doctors (
    doctor_id INT PK, name VARCHAR(100), specialty VARCHAR(100), license_no VARCHAR(50) UNIQUE
);
CREATE TABLE patients (
    patient_id INT PK, name VARCHAR(100), dob DATE, blood_group VARCHAR(5), phone VARCHAR(15)
);
CREATE TABLE appointments (
    appt_id INT PK AUTO_INCREMENT,
    patient_id INT FK → patients,
    doctor_id INT FK → doctors,
    scheduled_at DATETIME,
    status ENUM('BOOKED','COMPLETED','CANCELLED','NO_SHOW'),
    notes TEXT
);
CREATE TABLE prescriptions (
    rx_id INT PK AUTO_INCREMENT,
    appt_id INT FK → appointments,
    medicine_name VARCHAR(200),
    dosage VARCHAR(100),
    duration VARCHAR(50)
);
CREATE TABLE medical_records (
    record_id INT PK AUTO_INCREMENT,
    patient_id INT FK → patients,
    diagnosis TEXT, treatment TEXT,
    recorded_at TIMESTAMP
);
```

---

### Q124. Design a Food Delivery System (Zomato/Swiggy)
```sql
CREATE TABLE restaurants (
    restaurant_id INT PK, name VARCHAR(200), city VARCHAR(50),
    lat DECIMAL(9,6), lng DECIMAL(9,6),
    avg_rating DECIMAL(3,2), is_open BOOLEAN
);
CREATE TABLE menu_items (
    item_id INT PK, restaurant_id INT FK, name VARCHAR(200),
    price DECIMAL(8,2), category VARCHAR(50), is_available BOOLEAN
);
CREATE TABLE delivery_agents (
    agent_id INT PK, name VARCHAR(100), phone VARCHAR(15), rating DECIMAL(3,2)
);
CREATE TABLE orders (
    order_id INT PK AUTO_INCREMENT,
    user_id INT FK, restaurant_id INT FK, agent_id INT FK,
    total DECIMAL(10,2), status ENUM('PLACED','ACCEPTED','PREPARING','PICKED','DELIVERED','CANCELLED'),
    placed_at TIMESTAMP, delivered_at TIMESTAMP
);
CREATE TABLE order_items (
    order_id INT FK, item_id INT FK,
    quantity INT, price DECIMAL(8,2),
    PRIMARY KEY(order_id, item_id)
);
```

**Interview Question:** "How do you find the nearest available restaurant?"
→ Use geospatial index (MySQL SPATIAL INDEX or PostGIS). Calculate distance using Haversine formula or ST_Distance_Sphere.

---

### Q125. Design a Library Management System
```sql
CREATE TABLE books (
    book_id INT PK, isbn VARCHAR(20) UNIQUE,
    title VARCHAR(300), author VARCHAR(200), genre VARCHAR(100),
    published_year INT, total_copies INT, available_copies INT
);
CREATE TABLE members (
    member_id INT PK, name VARCHAR(100), email VARCHAR(100) UNIQUE,
    membership_type ENUM('STUDENT','STAFF','PUBLIC'), expiry_date DATE
);
CREATE TABLE borrowings (
    borrowing_id INT PK AUTO_INCREMENT,
    member_id INT FK, book_id INT FK,
    borrowed_on DATE, due_date DATE, returned_on DATE,
    fine_amount DECIMAL(8,2) DEFAULT 0
);
```

---

### Q126. SQL for: Find customers who spent more than the average customer spending
```sql
WITH customer_spending AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM orders GROUP BY customer_id
),
avg_spend AS (
    SELECT AVG(total_spent) AS avg_spent FROM customer_spending
)
SELECT c.name, cs.total_spent
FROM customers c
JOIN customer_spending cs ON c.customer_id = cs.customer_id
CROSS JOIN avg_spend
WHERE cs.total_spent > avg_spend.avg_spent
ORDER BY cs.total_spent DESC;
```

---

### Q127. Median salary (without MEDIAN function in MySQL)
```sql
-- Method: Use ROW_NUMBER and count
WITH ranked AS (
    SELECT salary,
           ROW_NUMBER() OVER(ORDER BY salary) AS rn,
           COUNT(*) OVER() AS total
    FROM employees
)
SELECT AVG(salary) AS median
FROM ranked
WHERE rn IN (FLOOR((total + 1) / 2), CEIL((total + 1) / 2));
```

---

### Q128. Find the most popular product in each city
```sql
SELECT city, product_id, order_count FROM (
    SELECT c.city, o.product_id, COUNT(*) AS order_count,
           RANK() OVER(PARTITION BY c.city ORDER BY COUNT(*) DESC) AS rn
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.city, o.product_id
) t WHERE rn = 1;
```

---

### Q129. Cohort analysis — Customer retention by signup month
```sql
WITH cohorts AS (
    SELECT customer_id,
           DATE_FORMAT(joined_date, '%Y-%m') AS cohort_month
    FROM customers
),
orders_monthly AS (
    SELECT customer_id,
           DATE_FORMAT(order_date, '%Y-%m') AS order_month
    FROM orders
)
SELECT c.cohort_month,
       om.order_month,
       COUNT(DISTINCT om.customer_id) AS active_customers
FROM cohorts c
JOIN orders_monthly om ON c.customer_id = om.customer_id
GROUP BY c.cohort_month, om.order_month
ORDER BY c.cohort_month, om.order_month;
```

---

### Q130. Sessionization — Group user events into sessions (30-min gap = new session)
```sql
WITH events_with_gaps AS (
    SELECT user_id, event_time,
           LAG(event_time) OVER(PARTITION BY user_id ORDER BY event_time) AS prev_event,
           TIMESTAMPDIFF(MINUTE,
               LAG(event_time) OVER(PARTITION BY user_id ORDER BY event_time),
               event_time
           ) AS gap_minutes
    FROM user_events
),
sessions AS (
    SELECT user_id, event_time,
           SUM(CASE WHEN gap_minutes > 30 OR gap_minutes IS NULL THEN 1 ELSE 0 END)
               OVER(PARTITION BY user_id ORDER BY event_time) AS session_id
    FROM events_with_gaps
)
SELECT user_id, session_id,
       MIN(event_time) AS session_start,
       MAX(event_time) AS session_end,
       COUNT(*) AS events_in_session
FROM sessions
GROUP BY user_id, session_id;
```

---

### Q131-Q150: Additional Interview Queries

**Q131. Count orders per customer with 0 for customers with no orders**
```sql
SELECT c.customer_id, c.name, COALESCE(COUNT(o.order_id), 0) AS order_count
FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

**Q132. Products that have never been ordered**
```sql
SELECT p.product_name FROM products p
WHERE p.product_id NOT IN (SELECT DISTINCT product_id FROM orders);
-- Better (handles NULLs):
SELECT p.product_name FROM products p
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE product_id = p.product_id);
```

**Q133. Employee with the maximum salary in each job title**
```sql
SELECT job_title, name, salary FROM employees
WHERE (job_title, salary) IN (
    SELECT job_title, MAX(salary) FROM employees GROUP BY job_title
);
```

**Q134. Orders placed on weekends**
```sql
SELECT * FROM orders WHERE DAYOFWEEK(order_date) IN (1, 7);  -- 1=Sunday, 7=Saturday
-- PostgreSQL: WHERE EXTRACT(DOW FROM order_date) IN (0, 6)
```

**Q135. Customers whose total purchase > category average**
```sql
WITH customer_category_spend AS (
    SELECT o.customer_id, p.category, SUM(o.amount) AS spend
    FROM orders o JOIN products p ON o.product_id = p.product_id
    GROUP BY o.customer_id, p.category
),
category_avg AS (
    SELECT category, AVG(spend) AS avg_spend
    FROM customer_category_spend GROUP BY category
)
SELECT cs.customer_id, cs.category, cs.spend
FROM customer_category_spend cs
JOIN category_avg ca ON cs.category = ca.category
WHERE cs.spend > ca.avg_spend;
```

**Q136. Format output: Show salary as ₹X,XX,XXX**
```sql
SELECT name, CONCAT('₹', FORMAT(salary, 0)) AS formatted_salary FROM employees;
```

**Q137. Employees hired in the same month as birth month (example of date comparison)**
```sql
SELECT name FROM employees WHERE MONTH(hire_date) = MONTH(dob);
```

**Q138. Find the 5th order placed by each customer**
```sql
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER(PARTITION BY customer_id ORDER BY order_date) AS rn
    FROM orders
) t WHERE rn = 5;
```

**Q139. Moving sum — Total last 3 orders per customer**
```sql
SELECT customer_id, order_id, amount,
       SUM(amount) OVER(
           PARTITION BY customer_id
           ORDER BY order_date
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS last_3_orders_total
FROM orders;
```

**Q140. Find consecutive orders placed on the same day by the same customer**
```sql
SELECT customer_id, order_date, COUNT(*) AS same_day_orders
FROM orders GROUP BY customer_id, DATE(order_date) HAVING COUNT(*) > 1;
```

**Q141. All orders with revenue contribution percentage**
```sql
SELECT order_id, customer_id, amount,
       ROUND(amount * 100.0 / SUM(amount) OVER(), 2) AS pct_of_total
FROM orders ORDER BY pct_of_total DESC;
```

**Q142. Hierarchy levels — Depth of each employee in org chart**
```sql
WITH RECURSIVE org_tree AS (
    SELECT emp_id, name, manager_id, 0 AS depth
    FROM employees WHERE manager_id IS NULL
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, ot.depth + 1
    FROM employees e JOIN org_tree ot ON e.manager_id = ot.emp_id
)
SELECT * FROM org_tree ORDER BY depth;
```

**Q143. Pivot table — Monthly revenue by category**
```sql
SELECT 
    MONTH(o.order_date) AS month,
    SUM(CASE WHEN p.category = 'Electronics' THEN o.amount ELSE 0 END) AS electronics,
    SUM(CASE WHEN p.category = 'Clothing' THEN o.amount ELSE 0 END) AS clothing,
    SUM(CASE WHEN p.category = 'Books' THEN o.amount ELSE 0 END) AS books
FROM orders o JOIN products p ON o.product_id = p.product_id
GROUP BY MONTH(o.order_date)
ORDER BY month;
```

**Q144. Unpivot — Convert wide format to long format**
```sql
SELECT customer_id, 'Q1' AS quarter, q1_revenue AS revenue FROM sales
UNION ALL SELECT customer_id, 'Q2', q2_revenue FROM sales
UNION ALL SELECT customer_id, 'Q3', q3_revenue FROM sales
UNION ALL SELECT customer_id, 'Q4', q4_revenue FROM sales;
```

**Q145. Full text search simulation**
```sql
-- Simple LIKE-based search:
SELECT * FROM products WHERE product_name LIKE '%wireless headphone%';

-- MySQL FULLTEXT index:
CREATE FULLTEXT INDEX ft_idx ON products(product_name, description);
SELECT *, MATCH(product_name, description) AGAINST('wireless headphone' IN NATURAL LANGUAGE MODE) AS relevance
FROM products
WHERE MATCH(product_name, description) AGAINST('wireless headphone');
```

**Q146. RANK employees by salary, reset rank for each department**
```sql
SELECT name, dept_id, salary,
       RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employees;
```

**Q147. Find orders where the total is an exact multiple of 100**
```sql
SELECT * FROM orders WHERE amount % 100 = 0;
```

**Q148. Customers who placed orders in EVERY month of 2024**
```sql
SELECT customer_id FROM orders
WHERE YEAR(order_date) = 2024
GROUP BY customer_id
HAVING COUNT(DISTINCT MONTH(order_date)) = 12;
```

**Q149. Find the employee who has been with the company the longest**
```sql
SELECT name, hire_date, TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS tenure
FROM employees ORDER BY hire_date ASC LIMIT 1;
```

**Q150. Schema design question: How do you store a product with multiple attributes (size: S/M/L, color: red/blue)?**
```sql
-- Pattern 1: EAV (flexible but hard to query)
CREATE TABLE product_attributes (product_id INT, attr_name VARCHAR(50), attr_value VARCHAR(200));

-- Pattern 2: JSON column (PostgreSQL/MySQL 5.7+)
ALTER TABLE products ADD COLUMN attributes JSON;
-- INSERT: {"size": ["S","M","L"], "color": ["red","blue"]}

-- Pattern 3: Separate variant table (recommended for e-commerce)
CREATE TABLE product_variants (
    variant_id INT PK, product_id INT FK,
    size VARCHAR(10), color VARCHAR(50),
    sku VARCHAR(100) UNIQUE, price DECIMAL(10,2), stock INT
);
```

---

## SQL vs MongoDB Comparison — Q151 to Q165

### Q151. Simple SELECT equivalent
```sql
-- SQL:
SELECT name, salary FROM employees WHERE dept_id = 3;
```
```javascript
// MongoDB:
db.employees.find({ dept_id: 3 }, { name: 1, salary: 1, _id: 0 })
```

### Q152. GROUP BY with COUNT equivalent
```sql
-- SQL:
SELECT dept_id, COUNT(*) as count FROM employees GROUP BY dept_id;
```
```javascript
// MongoDB:
db.employees.aggregate([
    { $group: { _id: "$dept_id", count: { $sum: 1 } } }
])
```

### Q153. JOIN vs $lookup
```sql
-- SQL:
SELECT e.name, d.dept_name FROM employees e JOIN departments d ON e.dept_id = d.dept_id;
```
```javascript
// MongoDB:
db.employees.aggregate([
    { $lookup: { from: "departments", localField: "dept_id", foreignField: "dept_id", as: "dept" } },
    { $unwind: "$dept" },
    { $project: { name: 1, "dept.dept_name": 1 } }
])
```

### Q154. SQL vs MongoDB scenarios

| Scenario | Use SQL | Use MongoDB |
|---|---|---|
| Financial transactions | ✅ (ACID critical) | ❌ |
| User profiles with varying fields | ❌ | ✅ (flexible schema) |
| Complex reporting with joins | ✅ | ❌ |
| High-write logging/events | ❌ (slow) | ✅ |
| E-commerce orders | ✅ | Can work |
| Product catalog with varied attributes | ❌ | ✅ |
| Real-time analytics at scale | ❌ | ✅ |

---

## OUTPUT PREDICTION QUESTIONS — Q165 to Q200

**Q165.**
```sql
SELECT COUNT(*) FROM employees WHERE salary > NULL;
```
**Answer:** 0 — Any comparison with NULL returns UNKNOWN (not TRUE), so no rows match.

---

**Q166.**
```sql
SELECT 1 = 1, 1 = '1', 'a' = 'A';
```
**Answer (MySQL):** 1, 1, 0 (case-insensitive string compare for '1'; case-sensitive for 'a' vs 'A' in binary collation)

---

**Q167.**
```sql
SELECT RANK() OVER(ORDER BY salary DESC) FROM employees;
-- Employees: salary = 90k, 90k, 80k, 70k
```
**Answer:** 1, 1, 3, 4 (RANK skips 2 after tie)

---

**Q168.**
```sql
SELECT dept_id FROM employees GROUP BY dept_id ORDER BY COUNT(*) DESC LIMIT 2;
```
**Answer:** The 2 departments with the most employees, returned in descending order of count.

---

**Q169.**
```sql
UPDATE employees SET salary = salary + 5000 WHERE dept_id = 3;
SELECT AVG(salary) FROM employees WHERE dept_id = 3;
-- Before update: 3 employees with salaries 40k, 50k, 60k
```
**Answer:** AVG = (45000 + 55000 + 65000) / 3 = 55000

---

**Q170.**
```sql
SELECT name FROM employees WHERE name IN ('Alice', 'Bob', NULL);
```
**Answer:** Returns employees named 'Alice' or 'Bob'. NOT rows where name IS NULL. NULL in IN list is simply ignored for comparison.

---

**Q171.**
```sql
SELECT COALESCE(NULL, 0, NULL, 5);
```
**Answer:** 0 — First non-NULL value.

---

**Q172.**
```sql
SELECT COUNT(1), COUNT(*), COUNT(NULL) FROM employees;
```
**Answer:** COUNT(1) = total rows, COUNT(*) = total rows, COUNT(NULL) = 0 (NULL values excluded from COUNT).

---

**Q173.**
```sql
-- employees table has 5 rows: emp_id 1,2,3,4,5
DELETE FROM employees WHERE emp_id > 3;
SELECT COUNT(*) FROM employees;
```
**Answer:** 3 (rows 4 and 5 deleted)

---

**Q174.**
```sql
SELECT 'Hello' LIKE 'H_llo';
```
**Answer:** 1 (TRUE). `_` matches any single character.

---

**Q175.**
```sql
SELECT TRIM(BOTH 'x' FROM 'xxxHelloxx');
```
**Answer:** 'Hello' — TRIM removes specified characters from both ends.

---

*This file contains Q81-Q200+. Continue practicing with LeetCode Database, DataLemur, and StrataScratch.*
