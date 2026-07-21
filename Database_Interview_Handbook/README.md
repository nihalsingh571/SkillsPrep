# Database Interview Handbook
## DBMS + SQL + MongoDB — Complete Interview Preparation (FAANG & Product Companies)

> **Philosophy: 20% Theory, 80% Practice. Every topic has interview traps, follow-ups, and real queries.**

---

## 📁 Structure

| File | Contents |
|---|---|
| [01_DBMS_Concepts.md](./01_DBMS_Concepts.md) | Keys, Normalization, ACID, Transactions, Isolation Levels, Indexes, Locking, Deadlocks, CAP Theorem, Sharding, Replication — 50 Interview Q&A |
| [02_SQL_Fundamentals.md](./02_SQL_Fundamentals.md) | Joins, GROUP BY, HAVING, Subqueries, Aggregates, CASE, String/Date Functions — Q1–Q80 |
| [03_SQL_Advanced.md](./03_SQL_Advanced.md) | Window Functions, CTEs, Query Optimization, Debug-the-Query, Output Prediction, Database Design — Q81–Q200+ |
| [04_MongoDB_Complete.md](./04_MongoDB_Complete.md) | CRUD, Aggregation Pipeline, Lookup, Indexes, Schema Design, Transactions, Sharding — 80 Queries |
| [05_Rapid_Revision_Guide.md](./05_Rapid_Revision_Guide.md) | 4-page cheat sheet: syntax, traps, most-asked questions, formulas |

---

## 🎯 Company-Wise Focus

| Company | Primary Focus |
|---|---|
| **Google, Meta** | Query optimization, Window functions, DB design at scale |
| **Amazon** | Complex joins, Aggregations, DynamoDB concepts |
| **Microsoft** | Stored procedures, Transactions, ACID, SQL Server specifics |
| **Infosys, TCS, Wipro** | Basic joins, GROUP BY, HAVING, Normalization, Keys |
| **Flipkart, Swiggy, Zomato** | MongoDB, Aggregation pipelines, Sharding |
| **Atlassian, Adobe** | CTEs, Window functions, Schema design |
| **Startups** | MongoDB CRUD, SQL JOINs, REST + DB interaction |

---

## 📊 Schemas Used Throughout This Handbook

```sql
-- EMPLOYEES TABLE
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100),
    dept_id INT,
    salary DECIMAL(10,2),
    manager_id INT,
    hire_date DATE,
    city VARCHAR(50)
);

-- DEPARTMENTS TABLE
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100),
    location VARCHAR(100)
);

-- ORDERS TABLE (E-commerce)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    amount DECIMAL(10,2),
    order_date DATE,
    status VARCHAR(20)
);

-- PRODUCTS TABLE
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    stock INT
);

-- CUSTOMERS TABLE
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(50),
    joined_date DATE
);
```
