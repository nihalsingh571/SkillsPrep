# SQL Fundamentals — Q1 to Q80

> **Schemas used:** employees, departments, orders, products, customers (see README)

---

## JOINS — Q1 to Q20

### Q1. Get all employees with their department names (INNER JOIN)
```sql
SELECT e.name, e.salary, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```
**Output Prediction Trap:** Employees with NULL dept_id will NOT appear in INNER JOIN result.

---

### Q2. Get ALL employees including those without a department (LEFT JOIN)
```sql
SELECT e.name, e.salary, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;
-- Employees with no dept: dept_name will be NULL
```

---

### Q3. Find employees who have NO department assigned
```sql
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_id IS NULL;
-- Trap: Filter on the RIGHT table's column (not e.dept_id) to find non-matching rows
```

---

### Q4. Get departments that have NO employees (find unused departments)
```sql
SELECT d.dept_name
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
WHERE e.emp_id IS NULL;
```

---

### Q5. Find each employee and their manager's name (SELF JOIN)
```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
-- LEFT JOIN so we see employees with no manager (CEO) too
```

---

### Q6. Get all combinations of employees and departments (CROSS JOIN)
```sql
SELECT e.name, d.dept_name
FROM employees e
CROSS JOIN departments d;
-- Returns: (# employees) × (# departments) rows
```
**Interview Trap:** CROSS JOIN without WHERE = Cartesian product. Use carefully!

---

### Q7. Employees who earn more than their manager
```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```

---

### Q8. INNER JOIN with multiple conditions
```sql
-- Employees in the same department AND same city as their department location
SELECT e.name, e.city, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id AND e.city = d.location;
```

---

### Q9. Three-table JOIN: Employee + Department + Orders
```sql
SELECT e.name, d.dept_name, COUNT(o.order_id) AS total_orders
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
JOIN orders o ON o.customer_id = e.emp_id
GROUP BY e.name, d.dept_name;
```

---

### Q10. Find customers who have placed orders (EXISTS vs JOIN)
```sql
-- Using EXISTS (more efficient — stops scanning after first match)
SELECT c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Using JOIN (may cause duplicates if multiple orders)
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

---

### Q11. Find customers who have NEVER placed an order (NOT EXISTS)
```sql
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);

-- Alternative: LEFT JOIN + NULL check
SELECT c.name FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

---

### Q12. FULL OUTER JOIN — All employees and all departments (even unmatched)
```sql
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;

-- MySQL doesn't support FULL OUTER JOIN — emulate with UNION:
SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.dept_id
UNION
SELECT e.name, d.dept_name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.dept_id;
```

---

### Q13. Find products that were NEVER ordered
```sql
SELECT p.product_name FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
WHERE o.order_id IS NULL;
```

---

### Q14. JOIN with aggregation — Total sales per department
```sql
SELECT d.dept_name, SUM(o.amount) AS total_sales
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
JOIN orders o ON e.emp_id = o.customer_id
GROUP BY d.dept_name
ORDER BY total_sales DESC;
```

---

### Q15. Non-equi JOIN — Employees in a salary band
```sql
-- Find all employees and which salary grade they belong to
SELECT e.name, e.salary, sg.grade
FROM employees e
JOIN salary_grades sg ON e.salary BETWEEN sg.min_salary AND sg.max_salary;
```

---

### Q16. Debug this query: Why does LEFT JOIN behave like INNER JOIN?
```sql
-- BUGGY: WHERE filter on right table kills LEFT JOIN behavior
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location = 'Mumbai';  -- ❌ This filters out NULLs!

-- FIX: Move condition to ON clause
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id AND d.location = 'Mumbai';
```

---

### Q17. Duplicate rows with JOIN — Spot the bug
```sql
-- If a customer has 5 orders, this returns 5 rows per customer!
SELECT c.name, SUM(o.amount)
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;  -- This is actually fine — GROUP BY aggregates them
-- But WITHOUT GROUP BY: SELECT c.name, o.amount — would give 5 rows
```

---

### Q18. Find employees who work in the same department as 'Alice'
```sql
SELECT e.name FROM employees e
WHERE e.dept_id = (SELECT dept_id FROM employees WHERE name = 'Alice')
AND e.name != 'Alice';
```

---

### Q19. Employees in departments located in 'Mumbai' OR 'Delhi'
```sql
SELECT e.name, d.dept_name, d.location
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location IN ('Mumbai', 'Delhi');
```

---

### Q20. Find the department with the highest average salary using JOIN
```sql
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY avg_salary DESC
LIMIT 1;
```

---

## GROUP BY, HAVING, AGGREGATE — Q21 to Q40

### Q21. Count employees in each department
```sql
SELECT dept_id, COUNT(*) AS employee_count
FROM employees
GROUP BY dept_id;
```
**Trap:** COUNT(*) counts all rows including NULLs. COUNT(salary) excludes NULL salaries.

---

### Q22. Departments with more than 5 employees (HAVING)
```sql
SELECT dept_id, COUNT(*) AS emp_count
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 5;
-- TRAP: Cannot use WHERE COUNT(*) > 5 — WHERE runs before aggregation!
```

---

### Q23. Average salary per department, only show departments where avg > 60000
```sql
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING AVG(e.salary) > 60000;
```

---

### Q24. Find the highest salary in each department
```sql
SELECT dept_id, MAX(salary) AS max_salary
FROM employees
GROUP BY dept_id;
```

---

### Q25. Total, Average, Min, Max salary across all employees
```sql
SELECT 
    COUNT(*) AS total_employees,
    SUM(salary) AS total_salary,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary
FROM employees;
```

---

### Q26. Number of orders per customer per month
```sql
SELECT customer_id,
       YEAR(order_date) AS yr,
       MONTH(order_date) AS mo,
       COUNT(*) AS order_count
FROM orders
GROUP BY customer_id, YEAR(order_date), MONTH(order_date)
ORDER BY customer_id, yr, mo;
```

---

### Q27. Second highest salary (classic interview question)
```sql
-- Method 1: LIMIT + OFFSET (MySQL)
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;

-- Method 2: Subquery (works everywhere)
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 3: DENSE_RANK() — most robust
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER(ORDER BY salary DESC) AS rnk
    FROM employees
) t WHERE rnk = 2;
```

---

### Q28. Top 3 highest-paid employees per department
```sql
SELECT * FROM (
    SELECT name, dept_id, salary,
           RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) AS rnk
    FROM employees
) t
WHERE rnk <= 3;
```

---

### Q29. Employees whose salary is above the department average
```sql
SELECT e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id
);
-- Correlated subquery — executes once per employee row
```

---

### Q30. Count employees with salary NULL vs NOT NULL
```sql
SELECT 
    COUNT(salary) AS with_salary,          -- NULLs excluded
    COUNT(*) - COUNT(salary) AS null_salary -- NULL count
FROM employees;
```

---

### Q31. Find duplicate emails in customers table
```sql
SELECT email, COUNT(*) AS cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

---

### Q32. Delete duplicate rows, keep the one with lowest customer_id
```sql
DELETE FROM customers
WHERE customer_id NOT IN (
    SELECT MIN(customer_id) FROM customers GROUP BY email
);
```

---

### Q33. Revenue by product category
```sql
SELECT p.category, SUM(o.amount) AS revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```

---

### Q34. Customers who ordered more than 3 times
```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 3;
```

---

### Q35. Monthly revenue trend
```sql
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    SUM(amount) AS monthly_revenue,
    COUNT(*) AS total_orders
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

---

### Q36. Output Prediction: What does this return?
```sql
SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING dept_id > 2;
```
**Answer:** Groups employees by dept_id, THEN filters groups where dept_id > 2. Returns count of employees in departments 3, 4, 5...

---

### Q37. Departments where EVERY employee earns more than 50000
```sql
-- Method 1: HAVING with MIN
SELECT dept_id FROM employees
GROUP BY dept_id
HAVING MIN(salary) > 50000;

-- Method 2: NOT EXISTS
SELECT DISTINCT dept_id FROM employees e
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE dept_id = e.dept_id AND salary <= 50000
);
```

---

### Q38. Percentage of total salary each department takes
```sql
SELECT dept_id,
       SUM(salary) AS dept_total,
       SUM(salary) * 100.0 / SUM(SUM(salary)) OVER() AS pct_of_total
FROM employees
GROUP BY dept_id;
```

---

### Q39. Orders placed today vs yesterday
```sql
SELECT 
    SUM(CASE WHEN DATE(order_date) = CURDATE() THEN amount ELSE 0 END) AS today_revenue,
    SUM(CASE WHEN DATE(order_date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN amount ELSE 0 END) AS yesterday_revenue
FROM orders;
```

---

### Q40. Rollup — Total + subtotal per department
```sql
SELECT dept_id, job_title, SUM(salary)
FROM employees
GROUP BY dept_id, job_title WITH ROLLUP;
-- Adds subtotal rows for each dept_id, plus grand total row
```

---

## SUBQUERIES & CASE — Q41 to Q60

### Q41. Find the employee(s) with the maximum salary (handle ties)
```sql
SELECT * FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);
```

---

### Q42. Employees in departments with more than 10 employees (IN subquery)
```sql
SELECT * FROM employees
WHERE dept_id IN (
    SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) > 10
);
```

---

### Q43. Employees earning more than ALL employees in dept 5
```sql
SELECT * FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE dept_id = 5);
```
**Trap:** `> ALL` = greater than maximum. `> ANY` = greater than minimum.

---

### Q44. CASE statement — Salary bands
```sql
SELECT name, salary,
    CASE 
        WHEN salary < 30000 THEN 'Low'
        WHEN salary BETWEEN 30000 AND 70000 THEN 'Mid'
        WHEN salary > 70000 THEN 'High'
        ELSE 'Unknown'
    END AS salary_band
FROM employees;
```

---

### Q45. CASE in ORDER BY — Sort by custom priority
```sql
SELECT * FROM orders
ORDER BY 
    CASE status
        WHEN 'URGENT' THEN 1
        WHEN 'PENDING' THEN 2
        WHEN 'SHIPPED' THEN 3
        ELSE 4
    END;
```

---

### Q46. Conditional aggregation — Count orders by status in one row
```sql
SELECT 
    COUNT(CASE WHEN status = 'PENDING' THEN 1 END) AS pending,
    COUNT(CASE WHEN status = 'SHIPPED' THEN 1 END) AS shipped,
    COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END) AS delivered
FROM orders;
-- This is the PIVOT pattern in SQL!
```

---

### Q47. Find Nth highest salary (generic, parameterized)
```sql
-- Nth highest where N = 3
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER(ORDER BY salary DESC) AS rnk
    FROM employees
) t WHERE rnk = 3;
```

---

### Q48. Customers who ordered product A but NOT product B
```sql
SELECT DISTINCT customer_id FROM orders WHERE product_id = 'A'
AND customer_id NOT IN (
    SELECT customer_id FROM orders WHERE product_id = 'B'
);
```

---

### Q49. Correlated subquery — Products priced above average in their category
```sql
SELECT product_name, category, price
FROM products p
WHERE price > (
    SELECT AVG(price) FROM products WHERE category = p.category
);
```

---

### Q50. Derived table (subquery in FROM)
```sql
SELECT dept_name, avg_salary
FROM (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) dept_avg
JOIN departments d ON dept_avg.dept_id = d.dept_id
WHERE avg_salary > 50000;
```

---

### Q51. Find employees hired in the last 30 days
```sql
SELECT * FROM employees
WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
```

---

### Q52. String functions — Format employee display name
```sql
SELECT 
    CONCAT(UPPER(SUBSTRING(name, 1, 1)), LOWER(SUBSTRING(name, 2))) AS formatted_name,
    LENGTH(name) AS name_length,
    TRIM(name) AS trimmed_name
FROM employees;
```

---

### Q53. Date functions — Employee tenure in years
```sql
SELECT name, hire_date,
       TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_of_service
FROM employees;
```

---

### Q54. Find employees whose names start with 'A' and end with 'n'
```sql
SELECT * FROM employees
WHERE name LIKE 'A%n';
-- Trap: LIKE 'A%n' uses index on name (if exists) only for prefix 'A%', not suffix
```

---

### Q55. NULL handling — COALESCE and NULLIF
```sql
-- COALESCE: return first non-NULL
SELECT name, COALESCE(commission, 0) AS commission FROM employees;

-- NULLIF: return NULL if two values are equal (useful to avoid division by zero!)
SELECT total_sales / NULLIF(total_orders, 0) AS avg_order_value FROM sales_summary;

-- IFNULL (MySQL specific):
SELECT IFNULL(manager_id, 'No Manager') FROM employees;
```

---

### Q56. Ranking products by sales volume
```sql
SELECT product_id, SUM(amount) AS total_sales,
       RANK() OVER(ORDER BY SUM(amount) DESC) AS sales_rank
FROM orders
GROUP BY product_id;
```

---

### Q57. Find gaps in sequential order IDs
```sql
SELECT order_id + 1 AS gap_start
FROM orders o
WHERE NOT EXISTS (
    SELECT 1 FROM orders WHERE order_id = o.order_id + 1
)
AND order_id < (SELECT MAX(order_id) FROM orders);
```

---

### Q58. EXCEPT / MINUS — Customers who ordered last year but NOT this year
```sql
SELECT customer_id FROM orders WHERE YEAR(order_date) = YEAR(CURDATE()) - 1
EXCEPT
SELECT customer_id FROM orders WHERE YEAR(order_date) = YEAR(CURDATE());
-- MySQL uses: first_query and customer_id NOT IN (second_query)
```

---

### Q59. INTERSECT — Customers who ordered BOTH this year AND last year
```sql
SELECT customer_id FROM orders WHERE YEAR(order_date) = YEAR(CURDATE()) - 1
INTERSECT
SELECT customer_id FROM orders WHERE YEAR(order_date) = YEAR(CURDATE());
```

---

### Q60. Output Prediction — Tricky GROUP BY
```sql
SELECT dept_id, name, MAX(salary)
FROM employees
GROUP BY dept_id;
-- ❌ ERROR in standard SQL! 'name' is neither aggregated nor in GROUP BY
-- MySQL with ONLY_FULL_GROUP_BY disabled might return arbitrary name
-- Fix: Use subquery or window function
```

---

## TRANSACTIONS, VIEWS, INDEXES — Q61 to Q80

### Q61. Create a view for high-salary employees
```sql
CREATE VIEW high_earners AS
SELECT emp_id, name, salary, dept_id
FROM employees
WHERE salary > 80000;

-- Use it:
SELECT * FROM high_earners WHERE dept_id = 3;
```

---

### Q62. Update through a view (updatable view conditions)
```sql
-- This works (simple single-table view, no aggregation):
UPDATE high_earners SET salary = salary * 1.1 WHERE dept_id = 3;

-- This FAILS (view with aggregation/DISTINCT):
CREATE VIEW dept_avg AS SELECT dept_id, AVG(salary) avg FROM employees GROUP BY dept_id;
UPDATE dept_avg SET avg = 70000;  -- ❌ Not updatable!
```

---

### Q63. Create composite index and explain when it's used
```sql
CREATE INDEX idx_dept_salary ON employees(dept_id, salary);

-- USES index (leftmost prefix):
SELECT * FROM employees WHERE dept_id = 3;
SELECT * FROM employees WHERE dept_id = 3 AND salary > 50000;

-- DOES NOT use index:
SELECT * FROM employees WHERE salary > 50000;  -- No dept_id in WHERE
```

---

### Q64. EXPLAIN a query — Identify full table scan
```sql
EXPLAIN SELECT * FROM employees WHERE YEAR(hire_date) = 2023;
-- Shows Seq Scan / Full Table Scan — bad!

-- FIX: Rewrite to allow index use
EXPLAIN SELECT * FROM employees 
WHERE hire_date BETWEEN '2023-01-01' AND '2023-12-31';
```

---

### Q65. Transaction with error handling
```sql
START TRANSACTION;

UPDATE accounts SET balance = balance - 1000 WHERE account_id = 1;
-- Check if account has enough balance:
SELECT balance INTO @bal FROM accounts WHERE account_id = 1;

IF @bal < 0 THEN
    ROLLBACK;
    SELECT 'Insufficient funds' AS error;
ELSE
    UPDATE accounts SET balance = balance + 1000 WHERE account_id = 2;
    COMMIT;
END IF;
```

---

### Q66. Find indexes on a table (MySQL)
```sql
SHOW INDEXES FROM employees;
-- or
SELECT * FROM information_schema.STATISTICS WHERE TABLE_NAME = 'employees';
```

---

### Q67. Drop and rebuild an index
```sql
DROP INDEX idx_dept_salary ON employees;
CREATE INDEX idx_dept_salary ON employees(dept_id, salary);
-- Rebuilding helps when index is fragmented after many DML operations
```

---

### Q68. Partial index (PostgreSQL) — Index only active orders
```sql
CREATE INDEX idx_pending_orders ON orders(customer_id) 
WHERE status = 'PENDING';
-- Smaller index, faster for queries filtering by status = 'PENDING'
```

---

### Q69. Query optimization — Rewrite without function on indexed column
```sql
-- BAD (no index use):
SELECT * FROM employees WHERE MONTH(hire_date) = 6;

-- GOOD (range scan possible):
SELECT * FROM employees 
WHERE hire_date BETWEEN '2023-06-01' AND '2023-06-30';
```

---

### Q70. Find slow queries using performance schema (MySQL)
```sql
SELECT query, exec_count, avg_latency
FROM sys.statement_analysis
ORDER BY avg_latency DESC
LIMIT 10;
```

---

### Q71. String aggregation — List all employees per department in one row
```sql
-- MySQL:
SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS employees
FROM employees
GROUP BY dept_id;

-- PostgreSQL:
SELECT dept_id, STRING_AGG(name, ', ' ORDER BY name) AS employees
FROM employees
GROUP BY dept_id;
```

---

### Q72. Find the most recent order for each customer
```sql
SELECT customer_id, MAX(order_date) AS last_order_date
FROM orders
GROUP BY customer_id;

-- To get full order details of latest order:
SELECT o.* FROM orders o
JOIN (
    SELECT customer_id, MAX(order_date) AS max_date
    FROM orders GROUP BY customer_id
) latest ON o.customer_id = latest.customer_id AND o.order_date = latest.max_date;
```

---

### Q73. Running total of revenue by date
```sql
SELECT order_date,
       SUM(amount) AS daily_revenue,
       SUM(SUM(amount)) OVER(ORDER BY order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders
GROUP BY order_date
ORDER BY order_date;
```

---

### Q74. Debug: Why is this UPDATE wrong?
```sql
-- WRONG: MySQL doesn't allow subquery referencing same table in UPDATE/DELETE
UPDATE employees 
SET salary = salary * 1.1
WHERE emp_id IN (SELECT emp_id FROM employees WHERE salary < 30000);  -- ❌ MySQL error

-- FIX: Use derived table
UPDATE employees 
SET salary = salary * 1.1
WHERE emp_id IN (SELECT emp_id FROM (SELECT emp_id FROM employees WHERE salary < 30000) AS t);
```

---

### Q75. INSERT with SELECT (copy data)
```sql
-- Insert high earners into archive table
INSERT INTO employees_archive (emp_id, name, salary, dept_id)
SELECT emp_id, name, salary, dept_id
FROM employees
WHERE salary > 100000;
```

---

### Q76. UPSERT — Insert if not exists, update if exists
```sql
-- MySQL:
INSERT INTO products (product_id, product_name, price)
VALUES (1, 'Laptop', 75000)
ON DUPLICATE KEY UPDATE price = VALUES(price);

-- PostgreSQL:
INSERT INTO products (product_id, product_name, price)
VALUES (1, 'Laptop', 75000)
ON CONFLICT (product_id) DO UPDATE SET price = EXCLUDED.price;
```

---

### Q77. Pagination — Efficient vs Inefficient
```sql
-- Inefficient (slow for large offsets — scans and discards rows):
SELECT * FROM orders ORDER BY order_date DESC LIMIT 20 OFFSET 10000;

-- Efficient (keyset/cursor pagination):
SELECT * FROM orders 
WHERE order_id < :last_seen_id  -- Pass last ID from previous page
ORDER BY order_id DESC LIMIT 20;
```

---

### Q78. Find all employees who report (directly or indirectly) to manager ID = 1
```sql
WITH RECURSIVE reports AS (
    SELECT emp_id, name, manager_id
    FROM employees
    WHERE manager_id = 1  -- Direct reports
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id
    FROM employees e
    JOIN reports r ON e.manager_id = r.emp_id  -- Indirect reports
)
SELECT * FROM reports;
```

---

### Q79. Detect and fix N+1 query pattern
```sql
-- N+1 BAD: 1 query for all customers, then N queries for each customer's orders
-- (demonstrated conceptually — this would be done in application code)

-- FIX: Single JOIN query
SELECT c.customer_id, c.name, COUNT(o.order_id) AS order_count, SUM(o.amount) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
```

---

### Q80. Output Prediction — NULL arithmetic
```sql
SELECT 
    NULL + 5,        -- NULL (any arithmetic with NULL = NULL)
    NULL = NULL,     -- NULL (not TRUE! Use IS NULL)
    NULL IS NULL,    -- TRUE (1)
    COALESCE(NULL, NULL, 3),  -- 3 (first non-NULL)
    1 / 0;           -- Error in MySQL; NULL in some DBs
```

---

*Next: [03_SQL_Advanced.md](./03_SQL_Advanced.md) — Window Functions, CTEs, Query Optimization, DB Design*
