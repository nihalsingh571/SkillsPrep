# SQL Fundamentals — Q1 to Q80
## Joins, GROUP BY, HAVING, Subqueries, Aggregates, CASE, String/Date Functions

> **Sample data for all queries is in [README.md](./README.md). Refer to it anytime.**

---

## SECTION 1 — JOINS (Q1–Q20)

> **Section Sample Data** — Queries below use `employees` + `departments`.
> Reminder: emp_id 9 (Ivy) has `dept_id = NULL`. dept_id 4 (HR) has no employees.

---

### Q1. Get all employees with their department names

📌 **New Concept — INNER JOIN:** Returns only rows where the condition matches in **both** tables. Rows that don't match on either side are excluded.

```sql
SELECT e.name, e.salary, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;
```

**Output:**
| name  | salary | dept_name   |
|-------|--------|-------------|
| Alice | 90000  | Engineering |
| Bob   | 75000  | Engineering |
| Grace | 75000  | Engineering |
| Carol | 85000  | Marketing   |
| David | 60000  | Marketing   |
| Hank  | 60000  | Marketing   |
| Eve   | 95000  | Sales       |
| Frank | 70000  | Sales       |
| Jack  | 90000  | Sales       |

> ⚠️ **Ivy (dept_id = NULL) is NOT in the output** — INNER JOIN excludes non-matching rows.

---

### Q2. Get ALL employees including those without a department

📌 **New Concept — LEFT JOIN:** Returns **all rows from the left table**, plus matching rows from the right. If no match exists on the right side, columns from the right table appear as `NULL`.

```sql
SELECT e.name, e.salary, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;
```

**Output:**
| name  | salary | dept_name   |
|-------|--------|-------------|
| Alice | 90000  | Engineering |
| Bob   | 75000  | Engineering |
| Carol | 85000  | Marketing   |
| David | 60000  | Marketing   |
| Eve   | 95000  | Sales       |
| Frank | 70000  | Sales       |
| Grace | 75000  | Engineering |
| Hank  | 60000  | Marketing   |
| **Ivy**   | **55000**  | **NULL**        |
| Jack  | 90000  | Sales       |

> Ivy appears with `dept_name = NULL` because she has no department.

---

### Q3. Find employees who have NO department assigned

```sql
SELECT e.name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.dept_id IS NULL;
```

**Output:**
| name |
|------|
| Ivy  |

> ⚠️ **Trap:** Filter on `d.dept_id IS NULL` (right-table column), not `e.dept_id IS NULL`. The first finds unmatched rows; the second finds employees with no dept stored.

---

### Q4. Get departments that have NO employees

```sql
SELECT d.dept_name
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
WHERE e.emp_id IS NULL;
```

**Output:**
| dept_name |
|-----------|
| HR        |

> HR (dept_id = 4) has no employees in our dataset, so it appears with `e.emp_id = NULL`.

---

### Q5. Find each employee and their manager's name

📌 **New Concept — SELF JOIN:** A table joined to **itself**. Use two different aliases (`e` for employee, `m` for manager) to treat the same table as two separate logical tables.

```sql
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.emp_id;
```

**Output:**
| employee | manager |
|----------|---------|
| Alice    | NULL    |
| Bob      | Alice   |
| Carol    | NULL    |
| David    | Carol   |
| Eve      | NULL    |
| Frank    | Eve     |
| Grace    | Alice   |
| Hank     | Carol   |
| Ivy      | NULL    |
| Jack     | Eve     |

> Alice, Carol, Eve, Ivy have no manager — they appear with `manager = NULL`.

---

### Q6. All combinations of employees and departments

📌 **New Concept — CROSS JOIN:** Returns the **Cartesian product** — every row from the left table paired with every row from the right table. 10 employees × 4 departments = **40 rows**.

```sql
SELECT e.name, d.dept_name
FROM employees e
CROSS JOIN departments d;
```

**Output (first 6 of 40 rows shown):**
| name  | dept_name   |
|-------|-------------|
| Alice | Engineering |
| Alice | Marketing   |
| Alice | Sales       |
| Alice | HR          |
| Bob   | Engineering |
| Bob   | Marketing   |
| ...   | ...         |

---

### Q7. Employees who earn more than their manager

```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.emp_id
WHERE e.salary > m.salary;
```

**Output:**
| employee | emp_salary | manager | mgr_salary |
|----------|------------|---------|------------|
| Jack     | 90000      | Eve     | 95000      |

> Jack (90000) does NOT exceed Eve (95000). With our data, **no row meets the condition** — empty result.
> *(If Eve's salary were 80000, Jack would appear.)*

---

### Q8. INNER JOIN with multiple conditions

```sql
SELECT e.name, e.city, d.dept_name
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id AND e.city = d.location;
```

**Output:**
| name  | city      | dept_name   |
|-------|-----------|-------------|
| Alice | Mumbai    | Engineering |
| Bob   | Mumbai    | Engineering |
| Grace | Mumbai    | Engineering |
| Carol | Delhi     | Marketing   |
| David | Delhi     | Marketing   |
| Hank  | Delhi     | Marketing   |
| Eve   | Bangalore | Sales       |
| Frank | Bangalore | Sales       |
| Jack  | Bangalore | Sales       |

---

### Q9. Three-table JOIN: Employee + Department + Orders

```sql
SELECT e.name, d.dept_name, COUNT(o.order_id) AS total_orders
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
JOIN orders o ON o.customer_id = e.emp_id
GROUP BY e.name, d.dept_name;
```

**Output (with our data — customers 1–5 overlap with emp_ids 1–5):**
| name  | dept_name   | total_orders |
|-------|-------------|--------------|
| Alice | Engineering | 3            |
| Carol | Marketing   | 2            |
| David | Marketing   | 1            |
| Eve   | Sales       | 1            |

---

### Q10. Customers who have placed orders (EXISTS vs JOIN)

📌 **New Concept — EXISTS:** A subquery that returns `TRUE` if at least one row matches. It stops scanning as soon as the first match is found — more efficient than `IN` for large datasets.

```sql
-- Using EXISTS
SELECT c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

**Output:**
| name   |
|--------|
| Rahul  |
| Priya  |
| Arun   |
| Sneha  |
| Vikram |

> Nisha (customer_id = 6) has no orders → excluded.

---

### Q11. Customers who have NEVER placed an order

```sql
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);
```

**Output:**
| name  |
|-------|
| Nisha |

---

### Q12. FULL OUTER JOIN — All employees and all departments

📌 **New Concept — FULL OUTER JOIN:** Returns all rows from both tables. Unmatched rows from either side appear with `NULL` for the other table's columns. **MySQL does not support this syntax directly — emulate with UNION.**

```sql
-- PostgreSQL / SQL Server:
SELECT e.name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;

-- MySQL equivalent:
SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.dept_id
UNION
SELECT e.name, d.dept_name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.dept_id;
```

**Output:**
| name  | dept_name   |
|-------|-------------|
| Alice | Engineering |
| Bob   | Engineering |
| Carol | Marketing   |
| ...   | ...         |
| Ivy   | NULL        |
| NULL  | HR          |

> Ivy has no dept → `dept_name = NULL`. HR has no employees → `name = NULL`.

---

### Q13. Find products that were NEVER ordered

```sql
SELECT p.product_name FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
WHERE o.order_id IS NULL;
```

**Output:**
| product_name  |
|---------------|
| Wireless Mouse (*)|

> *(Mouse was ordered in Q102/Q108 in our data, so result may be empty. If stock=200 item had no orders it would appear.)*
> With our dataset — all products were ordered at least once → **empty result**.

---

### Q14. Total sales per department

```sql
SELECT d.dept_name, SUM(o.amount) AS total_sales
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
JOIN orders o ON e.emp_id = o.customer_id
GROUP BY d.dept_name
ORDER BY total_sales DESC;
```

**Output:**
| dept_name   | total_sales |
|-------------|-------------|
| Engineering | 77300       |
| Marketing   | 13500       |
| Sales       | 1200        |

---

### Q15. Non-equi JOIN — Employees in a salary band

📌 **New Concept — Non-equi JOIN:** A JOIN using a condition other than `=`, such as `BETWEEN`, `<`, `>`. Useful for range-based lookups.

```sql
-- Assuming a salary_grades table: (grade, min_salary, max_salary)
-- Grade A: 80001–100000, Grade B: 60001–80000, Grade C: 0–60000
SELECT e.name, e.salary,
       CASE
           WHEN e.salary > 80000 THEN 'Grade A'
           WHEN e.salary > 60000 THEN 'Grade B'
           ELSE 'Grade C'
       END AS grade
FROM employees e;
```

**Output:**
| name  | salary | grade   |
|-------|--------|---------|
| Alice | 90000  | Grade A |
| Bob   | 75000  | Grade B |
| Carol | 85000  | Grade A |
| David | 60000  | Grade C |
| Eve   | 95000  | Grade A |
| Frank | 70000  | Grade B |
| Grace | 75000  | Grade B |
| Hank  | 60000  | Grade C |
| Ivy   | 55000  | Grade C |
| Jack  | 90000  | Grade A |

---

### Q16. Debug: LEFT JOIN behaving like INNER JOIN

```sql
-- ❌ BUGGY: WHERE on right table kills LEFT JOIN
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location = 'Mumbai';

-- ✅ FIX: Move condition to ON clause
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id AND d.location = 'Mumbai';
```

**Buggy Output:** Only employees whose dept is in Mumbai — Ivy disappears.
**Fixed Output:**
| name  | dept_name   |
|-------|-------------|
| Alice | Engineering |
| Bob   | Engineering |
| Grace | Engineering |
| Carol | NULL        |
| David | NULL        |
| Eve   | NULL        |
| Frank | NULL        |
| Hank  | NULL        |
| Ivy   | NULL        |
| Jack  | NULL        |

---

### Q17. Find employees who work in the same department as Alice

```sql
SELECT e.name FROM employees e
WHERE e.dept_id = (SELECT dept_id FROM employees WHERE name = 'Alice')
AND e.name != 'Alice';
```

**Output:**
| name  |
|-------|
| Bob   |
| Grace |

---

### Q18. Employees in departments located in Mumbai or Delhi

```sql
SELECT e.name, d.dept_name, d.location
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
WHERE d.location IN ('Mumbai', 'Delhi');
```

**Output:**
| name  | dept_name   | location |
|-------|-------------|----------|
| Alice | Engineering | Mumbai   |
| Bob   | Engineering | Mumbai   |
| Grace | Engineering | Mumbai   |
| Carol | Marketing   | Delhi    |
| David | Marketing   | Delhi    |
| Hank  | Marketing   | Delhi    |

---

### Q19. Department with the highest average salary

```sql
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_name
ORDER BY avg_salary DESC
LIMIT 1;
```

📌 **New Concept — LIMIT:** Restricts the number of rows returned by the query.

**Output:**
| dept_name | avg_salary |
|-----------|------------|
| Sales     | 85000.00   |

> Sales avg = (95000 + 70000 + 90000) / 3 = 85000.

---

### Q20. List products never ordered (NOT IN alternative)

```sql
SELECT p.product_name FROM products p
WHERE p.product_id NOT IN (SELECT DISTINCT product_id FROM orders);
```

**Output:** *(Empty with our dataset — all products were ordered)*
| product_name |
|---|
| *(no rows)* |

---

## SECTION 2 — GROUP BY, HAVING, AGGREGATES (Q21–Q40)

---

### Q21. Count employees in each department

📌 **New Concept — GROUP BY:** Groups rows that share the same value in a column. Aggregate functions like `COUNT`, `SUM`, `AVG`, `MAX`, `MIN` are then applied per group.

📌 **New Concept — COUNT(*):** Counts **all rows** in a group, including those with NULL values in other columns.

```sql
SELECT dept_id, COUNT(*) AS employee_count
FROM employees
GROUP BY dept_id;
```

**Output:**
| dept_id | employee_count |
|---------|----------------|
| NULL    | 1              |
| 1       | 3              |
| 2       | 3              |
| 3       | 3              |

---

### Q22. Departments with more than 2 employees

📌 **New Concept — HAVING:** Filters **groups** after GROUP BY. Unlike WHERE (which filters rows before grouping), HAVING can use aggregate functions like `COUNT(*)`, `SUM()`, etc.

```sql
SELECT dept_id, COUNT(*) AS emp_count
FROM employees
GROUP BY dept_id
HAVING COUNT(*) > 2;
```

**Output:**
| dept_id | emp_count |
|---------|-----------|
| 1       | 3         |
| 2       | 3         |
| 3       | 3         |

---

### Q23. Average salary per department, only where avg > 75000

```sql
SELECT d.dept_name, AVG(e.salary) AS avg_salary
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
GROUP BY d.dept_name
HAVING AVG(e.salary) > 75000;
```

**Output:**
| dept_name | avg_salary  |
|-----------|-------------|
| Engineering| 80000.00   |
| Sales      | 85000.00   |

> Engineering avg = (90000+75000+75000)/3 = 80000. Marketing = (85000+60000+60000)/3 = 68333 → excluded.

---

### Q24. Max salary per department

```sql
SELECT dept_id, MAX(salary) AS max_salary
FROM employees
GROUP BY dept_id;
```

**Output:**
| dept_id | max_salary |
|---------|------------|
| 1       | 90000      |
| 2       | 85000      |
| 3       | 95000      |
| NULL    | 55000      |

---

### Q25. Total, Average, Min, Max salary across all employees

```sql
SELECT
    COUNT(*)        AS total_employees,
    SUM(salary)     AS total_salary,
    AVG(salary)     AS avg_salary,
    MIN(salary)     AS min_salary,
    MAX(salary)     AS max_salary
FROM employees;
```

**Output:**
| total_employees | total_salary | avg_salary | min_salary | max_salary |
|-----------------|--------------|------------|------------|------------|
| 10              | 760000       | 76000.00   | 55000      | 95000      |

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

**Output:**
| customer_id | yr   | mo | order_count |
|-------------|------|----|-------------|
| 1           | 2024 | 1  | 1           |
| 1           | 2024 | 2  | 1           |
| 1           | 2024 | 5  | 1           |
| 2           | 2024 | 1  | 1           |
| 2           | 2024 | 5  | 1           |
| 3           | 2024 | 3  | 1           |
| 3           | 2024 | 6  | 1           |
| 4           | 2024 | 3  | 1           |
| 4           | 2024 | 4  | 1           |
| 5           | 2024 | 4  | 1           |

---

### Q27. Second highest salary (3 methods)

📌 **New Concept — DISTINCT:** Removes duplicate values from the result. `SELECT DISTINCT salary` returns only unique salary values.

```sql
-- Method 1: LIMIT + OFFSET
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;

-- Method 2: Subquery
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 3: DENSE_RANK (most robust — covered in detail in Chapter 3)
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER(ORDER BY salary DESC) AS rnk
    FROM employees
) t WHERE rnk = 2;
```

**Output (all 3 methods):**
| salary |
|--------|
| 90000  |

> 95000 is highest (Eve). Next distinct value = 90000 (Alice, Jack).

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

**Output:**
| name  | dept_id | salary | rnk |
|-------|---------|--------|-----|
| Alice | 1       | 90000  | 1   |
| Bob   | 1       | 75000  | 2   |
| Grace | 1       | 75000  | 2   |
| Carol | 2       | 85000  | 1   |
| David | 2       | 60000  | 2   |
| Hank  | 2       | 60000  | 2   |
| Eve   | 3       | 95000  | 1   |
| Jack  | 3       | 90000  | 2   |
| Frank | 3       | 70000  | 3   |

---

### Q29. Employees whose salary is above their department average

📌 **New Concept — Correlated Subquery:** A subquery that references a column from the **outer query** (`e.dept_id`). It executes **once per row** of the outer query, using the current row's value.

```sql
SELECT e.name, e.salary, e.dept_id
FROM employees e
WHERE e.salary > (
    SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id
);
```

**Output:**
| name  | salary | dept_id |
|-------|--------|---------|
| Alice | 90000  | 1       |
| Carol | 85000  | 2       |
| Eve   | 95000  | 3       |
| Jack  | 90000  | 3       |

> Dept 1 avg = 80000 → Alice (90000) qualifies. Dept 2 avg ≈ 68333 → Carol (85000) qualifies. Dept 3 avg = 85000 → Eve (95000) and Jack (90000) qualify.

---

### Q30. Count employees with NULL vs NOT NULL salary

```sql
SELECT
    COUNT(salary)          AS with_salary,
    COUNT(*) - COUNT(salary) AS null_salary
FROM employees;
```

📌 **New Concept — COUNT(column):** Unlike `COUNT(*)`, `COUNT(column)` **excludes NULL values** in that column.

**Output:**
| with_salary | null_salary |
|-------------|-------------|
| 10          | 0           |

> All 10 employees have non-NULL salaries in our dataset.

---

### Q31. Find duplicate emails in customers table

```sql
SELECT email, COUNT(*) AS cnt
FROM customers
GROUP BY email
HAVING COUNT(*) > 1;
```

**Output:** *(Empty — no duplicate emails in our dataset)*
| email | cnt |
|---|---|
| *(no rows)* | |

---

### Q32. Delete duplicate rows, keep lowest customer_id

```sql
DELETE FROM customers
WHERE customer_id NOT IN (
    SELECT MIN(customer_id) FROM customers GROUP BY email
);
```

> Deletes all rows except the one with the lowest `customer_id` for each email. With no duplicates in our dataset, no rows are deleted.

---

### Q33. Revenue by product category

```sql
SELECT p.category, SUM(o.amount) AS revenue
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```

**Output:**
| category    | revenue |
|-------------|---------|
| Furniture   | 62000   |
| Electronics | 78000   |
| Books       | 2000    |

> Electronics: 75000+1500+1500 = 78000. Furniture: 12000+25000+25000 = 62000. Books: 800+1200 = 2000.

---

### Q34. Customers who ordered more than 2 times

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 2;
```

**Output:**
| customer_id | order_count |
|-------------|-------------|
| 1           | 3           |

> Rahul (customer_id=1) placed orders 101, 102, 109 → 3 orders.

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

**Output:**
| month   | monthly_revenue | total_orders |
|---------|-----------------|--------------|
| 2024-01 | 87000           | 2            |
| 2024-02 | 1500            | 1            |
| 2024-03 | 75800           | 2            |
| 2024-04 | 26200           | 2            |
| 2024-05 | 2300            | 2            |
| 2024-06 | 25000           | 1            |

---

### Q36. Output Prediction

```sql
SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id HAVING dept_id > 1;
```

**Output:**
| dept_id | COUNT(*) |
|---------|----------|
| 2       | 3        |
| 3       | 3        |

> Groups where `dept_id > 1`. dept_id=1 and NULL are excluded.

---

### Q37. Departments where EVERY employee earns more than 60000

```sql
SELECT dept_id FROM employees
GROUP BY dept_id
HAVING MIN(salary) > 60000;
```

**Output:**
| dept_id |
|---------|
| 1       |
| 3       |

> Dept 1: min = 75000 ✅. Dept 2: min = 60000 ❌ (not strictly greater). Dept 3: min = 70000 ✅.

---

### Q38. Percentage of total salary each department takes

```sql
SELECT dept_id,
       SUM(salary) AS dept_total,
       ROUND(SUM(salary) * 100.0 / SUM(SUM(salary)) OVER(), 2) AS pct_of_total
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id;
```

**Output:**
| dept_id | dept_total | pct_of_total |
|---------|------------|--------------|
| 1       | 240000     | 33.80        |
| 2       | 205000     | 28.87        |
| 3       | 255000     | 35.92        |

---

### Q39. Orders placed today vs yesterday (conditional aggregation)

📌 **New Concept — Conditional Aggregation:** Using `CASE WHEN` inside an aggregate function like `SUM()` or `COUNT()` to calculate multiple metrics in a single query instead of multiple queries.

```sql
SELECT
    SUM(CASE WHEN DATE(order_date) = CURDATE() THEN amount ELSE 0 END) AS today_revenue,
    SUM(CASE WHEN DATE(order_date) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN amount ELSE 0 END) AS yesterday_revenue
FROM orders;
```

**Output (as of 2024-06-11):**
| today_revenue | yesterday_revenue |
|---------------|-------------------|
| 0             | 25000             |

---

### Q40. GROUP BY ROLLUP — Subtotals per department + grand total

📌 **New Concept — ROLLUP:** An extension of GROUP BY that also computes subtotal rows for each grouping level plus a grand total row. NULL in the grouping column marks a subtotal/grand total row.

```sql
SELECT dept_id, COUNT(*) AS emp_count, SUM(salary) AS total_salary
FROM employees
GROUP BY dept_id WITH ROLLUP;
```

**Output:**
| dept_id | emp_count | total_salary |
|---------|-----------|--------------|
| NULL    | 1         | 55000        |
| 1       | 3         | 240000       |
| 2       | 3         | 205000       |
| 3       | 3         | 255000       |
| **NULL**| **10**    | **755000**   |

> Last NULL row = grand total (10 employees, 755000 total).

---

## SECTION 3 — SUBQUERIES & CASE (Q41–Q60)

---

### Q41. Employee(s) with the maximum salary

```sql
SELECT * FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);
```

**Output:**
| emp_id | name | dept_id | salary | manager_id | hire_date  | city      |
|--------|------|---------|--------|------------|------------|-----------|
| 5      | Eve  | 3       | 95000  | NULL       | 2017-06-05 | Bangalore |

---

### Q42. Employees in departments with exactly 3 employees

📌 **New Concept — IN (subquery):** Checks if a value appears in a list returned by a subquery. More readable than multiple OR conditions.

```sql
SELECT * FROM employees
WHERE dept_id IN (
    SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) = 3
);
```

**Output:**
| name  | dept_id | salary |
|-------|---------|--------|
| Alice | 1       | 90000  |
| Bob   | 1       | 75000  |
| Carol | 2       | 85000  |
| David | 2       | 60000  |
| Eve   | 3       | 95000  |
| Frank | 3       | 70000  |
| Grace | 1       | 75000  |
| Hank  | 2       | 60000  |
| Jack  | 3       | 90000  |

---

### Q43. Employees earning more than ALL employees in dept 2

📌 **New Concept — ALL:** The condition must be true for **every** value returned by the subquery. `> ALL(...)` is equivalent to `> MAX(...)`.

```sql
SELECT name, salary FROM employees
WHERE salary > ALL (SELECT salary FROM employees WHERE dept_id = 2);
```

> Dept 2 salaries: 85000, 60000, 60000. `> ALL` means `> 85000`.

**Output:**
| name | salary |
|------|--------|
| Eve  | 95000  |
| Jack | 90000  |
| Alice| 90000  |

---

### Q44. CASE statement — Salary bands

📌 **New Concept — CASE WHEN:** The SQL equivalent of an if-else chain. Evaluates conditions in order and returns the value of the first matching branch.

```sql
SELECT name, salary,
    CASE
        WHEN salary < 65000 THEN 'Low'
        WHEN salary BETWEEN 65000 AND 85000 THEN 'Mid'
        WHEN salary > 85000 THEN 'High'
    END AS salary_band
FROM employees;
```

**Output:**
| name  | salary | salary_band |
|-------|--------|-------------|
| Alice | 90000  | High        |
| Bob   | 75000  | Mid         |
| Carol | 85000  | Mid         |
| David | 60000  | Low         |
| Eve   | 95000  | High        |
| Frank | 70000  | Mid         |
| Grace | 75000  | Mid         |
| Hank  | 60000  | Low         |
| Ivy   | 55000  | Low         |
| Jack  | 90000  | High        |

---

### Q45. CASE in ORDER BY — Custom sort priority

```sql
SELECT order_id, status, amount
FROM orders
ORDER BY
    CASE status
        WHEN 'PENDING'   THEN 1
        WHEN 'SHIPPED'   THEN 2
        WHEN 'DELIVERED' THEN 3
    END;
```

**Output:**
| order_id | status    | amount |
|----------|-----------|--------|
| 105      | PENDING   | 75000  |
| 108      | PENDING   | 1500   |
| 103      | SHIPPED   | 12000  |
| 110      | SHIPPED   | 25000  |
| 101      | DELIVERED | 75000  |
| 102      | DELIVERED | 1500   |
| ...      | ...       | ...    |

---

### Q46. Count orders by status in one row (PIVOT pattern)

```sql
SELECT
    COUNT(CASE WHEN status = 'PENDING'   THEN 1 END) AS pending,
    COUNT(CASE WHEN status = 'SHIPPED'   THEN 1 END) AS shipped,
    COUNT(CASE WHEN status = 'DELIVERED' THEN 1 END) AS delivered
FROM orders;
```

**Output:**
| pending | shipped | delivered |
|---------|---------|-----------|
| 2       | 2       | 6         |

---

### Q47. Nth highest salary (N=3)

```sql
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER(ORDER BY salary DESC) AS rnk
    FROM employees
) t WHERE rnk = 3;
```

> Salaries desc: 95000(rnk1), 90000(rnk2), 85000(rnk3), 75000(rnk4)...

**Output:**
| salary |
|--------|
| 85000  |

---

### Q48. Customers who ordered product 1 but NOT product 2

```sql
SELECT DISTINCT customer_id FROM orders WHERE product_id = 1
AND customer_id NOT IN (
    SELECT customer_id FROM orders WHERE product_id = 2
);
```

> Ordered product 1: customers 1, 4. Ordered product 2: customers 1, 2. So only customer 4 qualifies.

**Output:**
| customer_id |
|-------------|
| 4           |

---

### Q49. Products priced above average in their category

```sql
SELECT product_name, category, price
FROM products p
WHERE price > (
    SELECT AVG(price) FROM products WHERE category = p.category
);
```

> Electronics avg = (75000+1500)/2 = 38250 → Laptop Pro (75000) ✅. Books avg = (800+1200)/2 = 1000 → Python Course (1200) ✅. Furniture avg = (12000+25000)/2 = 18500 → Standing Desk (25000) ✅.

**Output:**
| product_name  | category    | price |
|---------------|-------------|-------|
| Laptop Pro    | Electronics | 75000 |
| Standing Desk | Furniture   | 25000 |
| Python Course | Books       | 1200  |

---

### Q50. Derived table — Departments with avg salary > 75000

📌 **New Concept — Derived Table:** A subquery placed in the `FROM` clause, treated as a temporary virtual table. Must be given an alias.

```sql
SELECT d.dept_name, dept_avg.avg_salary
FROM (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) AS dept_avg
JOIN departments d ON dept_avg.dept_id = d.dept_id
WHERE dept_avg.avg_salary > 75000;
```

**Output:**
| dept_name   | avg_salary |
|-------------|------------|
| Engineering | 80000.00   |
| Sales       | 85000.00   |

---

### Q51. Employees hired in the last 3 years

```sql
SELECT name, hire_date FROM employees
WHERE hire_date >= DATE_SUB(CURDATE(), INTERVAL 3 YEAR);
```

**Output (as of 2024):**
| name  | hire_date  |
|-------|------------|
| David | 2021-01-10 |
| Frank | 2022-04-18 |
| Grace | 2020-09-30 |
| Hank  | 2023-02-14 |
| Ivy   | 2021-08-25 |

---

### Q52. String functions — Format display name

📌 **New Concept — String Functions:** `CONCAT` joins strings. `UPPER`/`LOWER` changes case. `LENGTH` returns character count. `SUBSTRING(str, start, len)` extracts part of a string.

```sql
SELECT
    name,
    UPPER(name) AS upper_name,
    LENGTH(name) AS name_length,
    CONCAT(name, ' (', city, ')') AS display_name
FROM employees;
```

**Output:**
| name  | upper_name | name_length | display_name           |
|-------|------------|-------------|------------------------|
| Alice | ALICE      | 5           | Alice (Mumbai)         |
| Bob   | BOB        | 3           | Bob (Mumbai)           |
| Carol | CAROL      | 5           | Carol (Delhi)          |
| ...   | ...        | ...         | ...                    |

---

### Q53. Employee tenure in years

📌 **New Concept — TIMESTAMPDIFF(unit, date1, date2):** Returns the difference between two dates/times in the specified unit (YEAR, MONTH, DAY, HOUR, etc.).

```sql
SELECT name, hire_date,
       TIMESTAMPDIFF(YEAR, hire_date, CURDATE()) AS years_of_service
FROM employees
ORDER BY years_of_service DESC;
```

**Output (as of 2024):**
| name  | hire_date  | years_of_service |
|-------|------------|------------------|
| Eve   | 2017-06-05 | 7                |
| Carol | 2018-11-20 | 5                |
| Alice | 2019-03-15 | 5                |
| Jack  | 2019-12-01 | 4                |
| Bob   | 2020-07-01 | 3                |
| ...   | ...        | ...              |

---

### Q54. Find employees whose names start with 'A' and contain 'e'

📌 **New Concept — LIKE:** Pattern matching operator. `%` matches any sequence of characters (including empty). `_` matches exactly one character.

```sql
SELECT * FROM employees WHERE name LIKE 'A%' OR name LIKE '%e%';
```

**Output:**
| name  | salary |
|-------|--------|
| Alice | 90000  |
| Eve   | 95000  |
| Grace | 75000  |
| Hank  | 60000  |

---

### Q55. NULL handling — COALESCE and NULLIF

📌 **New Concept — COALESCE(a, b, c...):** Returns the **first non-NULL** value from the list. Commonly used to provide default values for NULLs.

📌 **New Concept — NULLIF(a, b):** Returns NULL if `a = b`, otherwise returns `a`. Commonly used to **avoid division by zero** (`NULLIF(divisor, 0)`).

```sql
SELECT
    name,
    dept_id,
    COALESCE(dept_id, 0)   AS dept_or_zero,
    NULLIF(dept_id, 1)     AS not_dept1
FROM employees;
```

**Output:**
| name  | dept_id | dept_or_zero | not_dept1 |
|-------|---------|--------------|-----------|
| Alice | 1       | 1            | NULL      |
| Bob   | 1       | 1            | NULL      |
| Carol | 2       | 2            | 2         |
| David | 2       | 2            | 2         |
| Ivy   | NULL    | 0            | NULL      |

---

### Q56. Ranking orders by amount

```sql
SELECT order_id, customer_id, amount,
       RANK() OVER(ORDER BY amount DESC) AS amount_rank
FROM orders;
```

**Output:**
| order_id | customer_id | amount | amount_rank |
|----------|-------------|--------|-------------|
| 101      | 1           | 75000  | 1           |
| 105      | 4           | 75000  | 1           |
| 110      | 3           | 25000  | 3           |
| 106      | 4           | 25000  | 3           |
| 103      | 2           | 12000  | 5           |
| 102      | 1           | 1500   | 6           |
| 108      | 2           | 1500   | 6           |
| 107      | 5           | 1200   | 8           |
| 104      | 3           | 800    | 9           |
| 109      | 1           | 800    | 9           |

---

### Q57. Find most recent order per customer

```sql
SELECT customer_id, MAX(order_date) AS last_order_date
FROM orders
GROUP BY customer_id;
```

**Output:**
| customer_id | last_order_date |
|-------------|-----------------|
| 1           | 2024-05-20      |
| 2           | 2024-05-01      |
| 3           | 2024-06-10      |
| 4           | 2024-04-02      |
| 5           | 2024-04-15      |

---

### Q58. UNION — Employees from Mumbai OR from Sales dept

📌 **New Concept — UNION:** Combines results of two SELECT queries, **removing duplicates**. Use `UNION ALL` to keep duplicates — it's faster because no deduplication step.

```sql
SELECT name, city FROM employees WHERE city = 'Mumbai'
UNION
SELECT name, city FROM employees WHERE dept_id = 3;
```

**Output:**
| name  | city      |
|-------|-----------|
| Alice | Mumbai    |
| Bob   | Mumbai    |
| Grace | Mumbai    |
| Eve   | Bangalore |
| Frank | Bangalore |
| Jack  | Bangalore |

---

### Q59. STRING_AGG / GROUP_CONCAT — List employees per department

📌 **New Concept — GROUP_CONCAT (MySQL) / STRING_AGG (PostgreSQL):** Aggregates multiple row values into a single comma-separated string within a GROUP BY.

```sql
-- MySQL:
SELECT dept_id, GROUP_CONCAT(name ORDER BY name SEPARATOR ', ') AS employees
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id;
```

**Output:**
| dept_id | employees              |
|---------|------------------------|
| 1       | Alice, Bob, Grace      |
| 2       | Carol, David, Hank     |
| 3       | Eve, Frank, Jack       |

---

### Q60. Output Prediction — Tricky GROUP BY error

```sql
SELECT dept_id, name, MAX(salary)
FROM employees
GROUP BY dept_id;
```

**Output:** ❌ **ERROR in strict SQL mode!** `name` is neither aggregated nor in GROUP BY.

**Fix:**
```sql
SELECT dept_id, MAX(salary) AS max_salary
FROM employees
GROUP BY dept_id;
```

**Correct Output:**
| dept_id | max_salary |
|---------|------------|
| 1       | 90000      |
| 2       | 85000      |
| 3       | 95000      |
| NULL    | 55000      |

---

## SECTION 4 — TRANSACTIONS, VIEWS, INDEXES (Q61–Q80)

---

### Q61. Create and use a view for high-salary employees

📌 **New Concept — VIEW:** A virtual table defined by a stored query. No data is physically stored. Every time you query the view, the underlying query runs.

```sql
CREATE VIEW high_earners AS
SELECT emp_id, name, salary, dept_id
FROM employees
WHERE salary > 80000;

SELECT * FROM high_earners;
```

**Output:**
| emp_id | name  | salary | dept_id |
|--------|-------|--------|---------|
| 1      | Alice | 90000  | 1       |
| 3      | Carol | 85000  | 2       |
| 5      | Eve   | 95000  | 3       |
| 10     | Jack  | 90000  | 3       |

---

### Q62. Attempt to update through a view

```sql
-- ✅ Works — simple single-table view, no aggregation:
UPDATE high_earners SET salary = 92000 WHERE emp_id = 1;

-- ❌ Fails — view with GROUP BY/aggregation is NOT updatable:
CREATE VIEW dept_avg AS SELECT dept_id, AVG(salary) avg FROM employees GROUP BY dept_id;
UPDATE dept_avg SET avg = 70000;  -- ERROR
```

---

### Q63. Create composite index and understand leftmost prefix rule

📌 **New Concept — Composite Index:** An index on multiple columns. SQL only uses this index when the query filters on the **leftmost column(s)** of the index (leftmost prefix rule).

```sql
CREATE INDEX idx_dept_salary ON employees(dept_id, salary);
```

| Query | Uses Index? |
|---|---|
| `WHERE dept_id = 1` | ✅ Yes |
| `WHERE dept_id = 1 AND salary > 70000` | ✅ Yes |
| `WHERE salary > 70000` | ❌ No (salary is not leftmost) |

---

### Q64. EXPLAIN — Identify full table scan

📌 **New Concept — EXPLAIN:** Shows the query execution plan chosen by the optimizer. Key terms: `type=ALL` = full table scan (bad); `type=ref` or `type=range` = index used (good).

```sql
EXPLAIN SELECT * FROM employees WHERE YEAR(hire_date) = 2020;
-- type: ALL (full table scan — function on column prevents index use)

-- Better query:
EXPLAIN SELECT * FROM employees WHERE hire_date BETWEEN '2020-01-01' AND '2020-12-31';
-- type: range (index scan — if index exists on hire_date)
```

---

### Q65. Basic transaction — Bank transfer

📌 **New Concept — Transaction:** A group of SQL operations treated as a single unit. Either ALL succeed (`COMMIT`) or ALL are undone (`ROLLBACK`).

```sql
START TRANSACTION;
  UPDATE orders SET status = 'SHIPPED' WHERE order_id = 105;
  UPDATE orders SET status = 'SHIPPED' WHERE order_id = 108;
COMMIT;
-- Both updates apply together. If any error occurs, use ROLLBACK to undo both.
```

---

### Q66. UPSERT — Insert if not exists, update if exists

📌 **New Concept — UPSERT:** A single operation that inserts a new row OR updates it if the row already exists (based on a unique/primary key conflict).

```sql
-- MySQL:
INSERT INTO products (product_id, product_name, price)
VALUES (1, 'Laptop Pro', 78000)
ON DUPLICATE KEY UPDATE price = VALUES(price);
```

**Effect:** product_id=1 already exists → updates price from 75000 to 78000.

---

### Q67. Efficient pagination — Keyset vs OFFSET

📌 **New Concept — Keyset Pagination:** Instead of `LIMIT n OFFSET m` (which scans and discards rows), use the last seen primary key as the starting point. Far more efficient for large datasets.

```sql
-- ❌ Slow for large offsets (scans 10000 rows, discards 9980):
SELECT * FROM orders ORDER BY order_id LIMIT 20 OFFSET 10000;

-- ✅ Fast keyset pagination:
SELECT * FROM orders WHERE order_id > 10000 ORDER BY order_id LIMIT 20;
```

---

### Q68. Find all employees who report to manager with emp_id = 5 (recursive CTE)

📌 **New Concept — Recursive CTE:** A CTE that references itself. Has two parts: the **anchor** (base case, non-recursive SELECT) and the **recursive member** (references the CTE itself). Used for hierarchical/tree data.

```sql
WITH RECURSIVE subordinates AS (
    SELECT emp_id, name, manager_id, 0 AS depth
    FROM employees WHERE emp_id = 5           -- Anchor: Eve herself
    UNION ALL
    SELECT e.emp_id, e.name, e.manager_id, s.depth + 1
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.emp_id  -- Recursive: find reports
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

### Q69. PIVOT — Monthly revenue by category in one row

```sql
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    SUM(CASE WHEN p.category = 'Electronics' THEN o.amount ELSE 0 END) AS electronics,
    SUM(CASE WHEN p.category = 'Furniture'   THEN o.amount ELSE 0 END) AS furniture,
    SUM(CASE WHEN p.category = 'Books'       THEN o.amount ELSE 0 END) AS books
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
ORDER BY month;
```

**Output:**
| month   | electronics | furniture | books |
|---------|-------------|-----------|-------|
| 2024-01 | 75000       | 12000     | 0     |
| 2024-02 | 1500        | 0         | 0     |
| 2024-03 | 75000       | 0         | 800   |
| 2024-04 | 0           | 25000     | 1200  |
| 2024-05 | 1500        | 0         | 800   |
| 2024-06 | 0           | 25000     | 0     |

---

### Q70. Find customers and their total spend

```sql
SELECT c.name,
       COUNT(o.order_id) AS total_orders,
       COALESCE(SUM(o.amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```

**Output:**
| name   | total_orders | total_spent |
|--------|--------------|-------------|
| Sneha  | 2            | 100000      |
| Rahul  | 3            | 77300       |
| Arun   | 2            | 25800       |
| Priya  | 2            | 13500       |
| Vikram | 1            | 1200        |
| Nisha  | 0            | 0           |

---

### Q71–Q80: Quick Reference Queries with Outputs

**Q71. String aggregation per department**
```sql
SELECT dept_id, GROUP_CONCAT(name SEPARATOR ', ') AS team
FROM employees WHERE dept_id IS NOT NULL GROUP BY dept_id;
```
| dept_id | team |
|---|---|
| 1 | Alice, Bob, Grace |
| 2 | Carol, David, Hank |
| 3 | Eve, Frank, Jack |

**Q72. Most recent order per customer (with full order details)**
```sql
SELECT o.* FROM orders o
JOIN (SELECT customer_id, MAX(order_date) AS max_dt FROM orders GROUP BY customer_id) latest
ON o.customer_id = latest.customer_id AND o.order_date = latest.max_dt;
```
| order_id | customer_id | amount | order_date |
|---|---|---|---|
| 109 | 1 | 800 | 2024-05-20 |
| 108 | 2 | 1500 | 2024-05-01 |
| 110 | 3 | 25000 | 2024-06-10 |
| 106 | 4 | 25000 | 2024-04-02 |
| 107 | 5 | 1200 | 2024-04-15 |

**Q73. NULL arithmetic trap**
```sql
SELECT NULL + 5, NULL = NULL, NULL IS NULL, COALESCE(NULL, NULL, 3), 1/0;
```
| NULL + 5 | NULL = NULL | NULL IS NULL | COALESCE | 1/0 |
|---|---|---|---|---|
| NULL | NULL | 1 | 3 | NULL (MySQL) |

**Q74. Percentage of each order in total revenue**
```sql
SELECT order_id, amount,
       ROUND(amount * 100.0 / SUM(amount) OVER(), 2) AS pct_of_total
FROM orders ORDER BY pct_of_total DESC;
```
| order_id | amount | pct_of_total |
|---|---|---|
| 101 | 75000 | 42.41 |
| 105 | 75000 | 42.41 |
| 110 | 25000 | 14.14 |
| ... | ... | ... |

**Q75–Q80:** See [03_SQL_Advanced.md](./03_SQL_Advanced.md) for Window Functions, CTEs, and complex queries with outputs.
