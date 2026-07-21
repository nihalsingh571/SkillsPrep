# Database Interview Handbook
## DBMS + SQL + MongoDB — Complete Interview Preparation (FAANG & Product Companies)

> **Philosophy: 20% Theory, 80% Practice. Every query has sample data + expected output.**
> **📌 New Concept callouts explain each term exactly once — when it first appears.**

---

## 📁 Files

| File | Contents |
|---|---|
| [01_DBMS_Concepts.md](./01_DBMS_Concepts.md) | Keys, Normalization, ACID, Transactions, Isolation, Indexes, Locking, CAP, Sharding — 50 Interview Q&A |
| [02_SQL_Fundamentals.md](./02_SQL_Fundamentals.md) | Joins, GROUP BY, HAVING, Subqueries, Aggregates, CASE — Q1–Q80 (with sample data + outputs) |
| [03_SQL_Advanced.md](./03_SQL_Advanced.md) | Window Functions, CTEs, Query Optimization, Debug Queries, DB Design — Q81–Q200+ |
| [04_MongoDB_Complete.md](./04_MongoDB_Complete.md) | CRUD, Aggregation Pipeline, Lookup, Indexes, Schema Design — 80 Queries (with outputs) |
| [05_Rapid_Revision_Guide.md](./05_Rapid_Revision_Guide.md) | 4-page cheat sheet: syntax, traps, most-asked questions |

---

## 🗃️ Master Sample Dataset (Used Across All SQL Chapters)

All SQL queries in this handbook run against this exact dataset. Refer back here anytime.

### `employees` table
```sql
CREATE TABLE employees (
    emp_id INT PRIMARY KEY, name VARCHAR(100), dept_id INT,
    salary DECIMAL(10,2), manager_id INT, hire_date DATE, city VARCHAR(50)
);

INSERT INTO employees VALUES
(1,  'Alice',   1, 90000, NULL, '2019-03-15', 'Mumbai'),
(2,  'Bob',     1, 75000, 1,    '2020-07-01', 'Mumbai'),
(3,  'Carol',   2, 85000, NULL, '2018-11-20', 'Delhi'),
(4,  'David',   2, 60000, 3,    '2021-01-10', 'Delhi'),
(5,  'Eve',     3, 95000, NULL, '2017-06-05', 'Bangalore'),
(6,  'Frank',   3, 70000, 5,    '2022-04-18', 'Bangalore'),
(7,  'Grace',   1, 75000, 1,    '2020-09-30', 'Mumbai'),
(8,  'Hank',    2, 60000, 3,    '2023-02-14', 'Delhi'),
(9,  'Ivy',     NULL, 55000, NULL, '2021-08-25', 'Pune'),
(10, 'Jack',    3, 90000, 5,    '2019-12-01', 'Bangalore');
```

| emp_id | name  | dept_id | salary | manager_id | hire_date  | city       |
|--------|-------|---------|--------|------------|------------|------------|
| 1      | Alice | 1       | 90000  | NULL       | 2019-03-15 | Mumbai     |
| 2      | Bob   | 1       | 75000  | 1          | 2020-07-01 | Mumbai     |
| 3      | Carol | 2       | 85000  | NULL       | 2018-11-20 | Delhi      |
| 4      | David | 2       | 60000  | 3          | 2021-01-10 | Delhi      |
| 5      | Eve   | 3       | 95000  | NULL       | 2017-06-05 | Bangalore  |
| 6      | Frank | 3       | 70000  | 5          | 2022-04-18 | Bangalore  |
| 7      | Grace | 1       | 75000  | 1          | 2020-09-30 | Mumbai     |
| 8      | Hank  | 2       | 60000  | 3          | 2023-02-14 | Delhi      |
| 9      | Ivy   | NULL    | 55000  | NULL       | 2021-08-25 | Pune       |
| 10     | Jack  | 3       | 90000  | 5          | 2019-12-01 | Bangalore  |

---

### `departments` table
```sql
CREATE TABLE departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(100), location VARCHAR(100));

INSERT INTO departments VALUES
(1, 'Engineering', 'Mumbai'),
(2, 'Marketing',   'Delhi'),
(3, 'Sales',       'Bangalore'),
(4, 'HR',          'Pune');
```

| dept_id | dept_name   | location  |
|---------|-------------|-----------|
| 1       | Engineering | Mumbai    |
| 2       | Marketing   | Delhi     |
| 3       | Sales       | Bangalore |
| 4       | HR          | Pune      |

---

### `customers` table
```sql
CREATE TABLE customers (customer_id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), city VARCHAR(50), joined_date DATE);

INSERT INTO customers VALUES
(1, 'Rahul',   'rahul@mail.com',   'Mumbai',    '2022-01-15'),
(2, 'Priya',   'priya@mail.com',   'Delhi',     '2021-06-20'),
(3, 'Arun',    'arun@mail.com',    'Bangalore', '2023-03-10'),
(4, 'Sneha',   'sneha@mail.com',   'Mumbai',    '2022-09-05'),
(5, 'Vikram',  'vikram@mail.com',  'Pune',      '2020-11-30'),
(6, 'Nisha',   'nisha@mail.com',   'Delhi',     '2023-07-22');
```

| customer_id | name   | email             | city      | joined_date |
|-------------|--------|-------------------|-----------|-------------|
| 1           | Rahul  | rahul@mail.com    | Mumbai    | 2022-01-15  |
| 2           | Priya  | priya@mail.com    | Delhi     | 2021-06-20  |
| 3           | Arun   | arun@mail.com     | Bangalore | 2023-03-10  |
| 4           | Sneha  | sneha@mail.com    | Mumbai    | 2022-09-05  |
| 5           | Vikram | vikram@mail.com   | Pune      | 2020-11-30  |
| 6           | Nisha  | nisha@mail.com    | Delhi     | 2023-07-22  |

---

### `products` table
```sql
CREATE TABLE products (product_id INT PRIMARY KEY, product_name VARCHAR(100), category VARCHAR(50), price DECIMAL(10,2), stock INT);

INSERT INTO products VALUES
(1, 'Laptop Pro',      'Electronics', 75000, 50),
(2, 'Wireless Mouse',  'Electronics',  1500, 200),
(3, 'Office Chair',    'Furniture',   12000, 30),
(4, 'Java Book',       'Books',         800,  100),
(5, 'Standing Desk',   'Furniture',   25000, 15),
(6, 'Python Course',   'Books',        1200, 500);
```

| product_id | product_name   | category    | price  | stock |
|------------|----------------|-------------|--------|-------|
| 1          | Laptop Pro     | Electronics | 75000  | 50    |
| 2          | Wireless Mouse | Electronics | 1500   | 200   |
| 3          | Office Chair   | Furniture   | 12000  | 30    |
| 4          | Java Book      | Books       | 800    | 100   |
| 5          | Standing Desk  | Furniture   | 25000  | 15    |
| 6          | Python Course  | Books       | 1200   | 500   |

---

### `orders` table
```sql
CREATE TABLE orders (order_id INT PRIMARY KEY, customer_id INT, product_id INT, amount DECIMAL(10,2), order_date DATE, status VARCHAR(20));

INSERT INTO orders VALUES
(101, 1, 1, 75000, '2024-01-10', 'DELIVERED'),
(102, 1, 2,  1500, '2024-02-14', 'DELIVERED'),
(103, 2, 3, 12000, '2024-01-20', 'SHIPPED'),
(104, 3, 4,   800, '2024-03-05', 'DELIVERED'),
(105, 4, 1, 75000, '2024-03-18', 'PENDING'),
(106, 4, 5, 25000, '2024-04-02', 'DELIVERED'),
(107, 5, 6,  1200, '2024-04-15', 'DELIVERED'),
(108, 2, 2,  1500, '2024-05-01', 'PENDING'),
(109, 1, 4,   800, '2024-05-20', 'DELIVERED'),
(110, 3, 5, 25000, '2024-06-10', 'SHIPPED');
```

| order_id | customer_id | product_id | amount | order_date | status    |
|----------|-------------|------------|--------|------------|-----------|
| 101      | 1           | 1          | 75000  | 2024-01-10 | DELIVERED |
| 102      | 1           | 2          | 1500   | 2024-02-14 | DELIVERED |
| 103      | 2           | 3          | 12000  | 2024-01-20 | SHIPPED   |
| 104      | 3           | 4          | 800    | 2024-03-05 | DELIVERED |
| 105      | 4           | 1          | 75000  | 2024-03-18 | PENDING   |
| 106      | 4           | 5          | 25000  | 2024-04-02 | DELIVERED |
| 107      | 5           | 6          | 1200   | 2024-04-15 | DELIVERED |
| 108      | 2           | 2          | 1500   | 2024-05-01 | PENDING   |
| 109      | 1           | 4          | 800    | 2024-05-20 | DELIVERED |
| 110      | 3           | 5          | 25000  | 2024-06-10 | SHIPPED   |

---

## 🗃️ Master Sample Dataset (MongoDB Collections)

```javascript
// employees collection
[
  { _id: 1, name: "Alice",  dept: "Engineering", salary: 90000, city: "Mumbai",    skills: ["Java","React","MongoDB"],  isActive: true,  joined: ISODate("2019-03-15") },
  { _id: 2, name: "Bob",    dept: "Engineering", salary: 75000, city: "Mumbai",    skills: ["Java","Spring"],           isActive: true,  joined: ISODate("2020-07-01") },
  { _id: 3, name: "Carol",  dept: "Marketing",   salary: 85000, city: "Delhi",     skills: ["SEO","Analytics"],         isActive: true,  joined: ISODate("2018-11-20") },
  { _id: 4, name: "David",  dept: "Marketing",   salary: 60000, city: "Delhi",     skills: ["Content","SEO"],           isActive: false, joined: ISODate("2021-01-10") },
  { _id: 5, name: "Eve",    dept: "Sales",       salary: 95000, city: "Bangalore", skills: ["CRM","Negotiation","Java"], isActive: true,  joined: ISODate("2017-06-05") }
]

// orders collection
[
  { _id: 101, customer_id: 1, product_id: 1, amount: 75000, status: "DELIVERED", order_date: ISODate("2024-01-10") },
  { _id: 102, customer_id: 1, product_id: 2, amount:  1500, status: "DELIVERED", order_date: ISODate("2024-02-14") },
  { _id: 103, customer_id: 2, product_id: 3, amount: 12000, status: "SHIPPED",   order_date: ISODate("2024-01-20") },
  { _id: 104, customer_id: 3, product_id: 4, amount:   800, status: "DELIVERED", order_date: ISODate("2024-03-05") },
  { _id: 105, customer_id: 4, product_id: 1, amount: 75000, status: "PENDING",   order_date: ISODate("2024-03-18") }
]

// products collection
[
  { _id: 1, name: "Laptop Pro",     category: "Electronics", price: 75000, stock: 50  },
  { _id: 2, name: "Wireless Mouse", category: "Electronics", price:  1500, stock: 200 },
  { _id: 3, name: "Office Chair",   category: "Furniture",   price: 12000, stock: 30  },
  { _id: 4, name: "Java Book",      category: "Books",       price:   800, stock: 100 },
  { _id: 5, name: "Standing Desk",  category: "Furniture",   price: 25000, stock: 15  }
]
```
