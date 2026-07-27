# Power Query & Data Cleaning — 30 Interview Questions

> For MIS Executive interviews — asked at EXL, Genpact, Accenture, TCS

---

## Q1. What is Power Query and why is it used?

**A:** Power Query is a data connection and transformation tool built into Excel (and Power BI) that lets you import, clean, and reshape data before loading it into a worksheet or data model. It records every transformation step you apply, so the entire process is repeatable with a single click on "Refresh." It eliminates the need for manual copy-paste or complex VBA macros for data preparation tasks. In MIS roles, it is used to automate the monthly/weekly data consolidation and cleaning process.

---

## Q2. From which sources can Power Query load data?

**A:** Power Query can connect to a wide variety of sources including Excel workbooks, CSV/text files, SQL Server databases, SharePoint folders, web URLs, OData feeds, PDFs, JSON files, and cloud services like Azure or Salesforce. In the "Get Data" menu you will find over 100 built-in connectors. For MIS work, the most common sources are Excel files, CSV exports from ERP/CRM systems, and SharePoint/OneDrive folders. You can also combine data from multiple different source types in one query.

---

## Q3. What is the difference between Merge Queries and Append Queries?

**A:** **Merge Queries** is like a JOIN in SQL — it combines two tables horizontally based on a matching key column, bringing in columns from the second table into the first. **Append Queries** stacks two or more tables vertically (like UNION in SQL), adding rows from one table below another. Use Merge when you want to enrich data with additional columns (e.g., adding product names from a lookup table). Use Append when you want to combine multiple identical-structured files into one consolidated dataset (e.g., monthly sales files).

---

## Q4. What are the join types available in Merge Queries?

**A:** Power Query offers six join types mirroring SQL joins: **Left Outer** (all rows from the first/left table, matching rows from right), **Right Outer** (all rows from right, matching from left), **Full Outer** (all rows from both tables), **Inner** (only matching rows from both), **Left Anti** (rows in left that have NO match in right), and **Right Anti** (rows in right with no match in left). In MIS work, Left Outer and Inner joins are the most frequently used. Left Anti is useful for finding unmatched or missing records between two datasets.

---

## Q5. How do you remove duplicate rows in Power Query?

**A:** Select the column(s) that should be unique, then go to **Home → Remove Rows → Remove Duplicates**. If you right-click on a column header, you also get the "Remove Duplicates" option directly. Power Query keeps the first occurrence and removes subsequent duplicates. If you need to deduplicate based on multiple columns, select all relevant columns before applying Remove Duplicates. This is more reliable than Excel's "Remove Duplicates" feature because it is embedded as a repeatable step in your query.

---

## Q6. What is Unpivot Columns and when would you use it?

**A:** Unpivot Columns transforms a wide table (many columns) into a tall/narrow table by converting column headers into row values. For example, if you have monthly sales data spread across 12 month columns (Jan, Feb, Mar…), Unpivot will turn it into two columns — "Month" and "Sales Value." This normalized format is required for pivot tables, Power BI data models, and proper data analysis. You can unpivot selected columns, or use "Unpivot Other Columns" to keep certain identifier columns and unpivot everything else.

---

## Q7. How do you split a column by a delimiter in Power Query?

**A:** Select the column you want to split, then go to **Transform → Split Column → By Delimiter**. You choose the delimiter character (comma, space, semicolon, etc.) and whether to split at each occurrence, the leftmost, or rightmost occurrence. Power Query will create new columns (e.g., Column1.1, Column1.2) for each split part. This is commonly used to separate "First Name Last Name" into two columns, or to extract parts from a product code like "CAT-SUB-SKU."

---

## Q8. What is the "Fill Down" feature in Power Query?

**A:** Fill Down replaces null values in a column by copying the last non-null value above them downward. It is accessed via **Transform → Fill → Down**. This is extremely useful when data is exported from systems where a value appears only once per group (e.g., a region or department name appears only in the first row of its group, leaving blanks below). Similarly, "Fill Up" propagates values upward. This is a very common data cleaning step in MIS reporting workflows.

---

## Q9. How do you replace values in Power Query?

**A:** Select the column, then go to **Transform → Replace Values** (or right-click → Replace Values). Enter the value to find and the value to replace it with. This is useful for fixing inconsistent data like replacing "N/A", "na", "NA", "#N/A" all with a blank or null. You can also replace values in error cells using **Replace Errors**. Unlike Find & Replace in Excel, this is recorded as a step and applied automatically on every refresh.

---

## Q10. How do you change data types in Power Query?

**A:** Select a column and click the data type icon on the left of the column header (or go to **Transform → Data Type**) and choose the correct type — Text, Whole Number, Decimal, Date, Date/Time, True/False, etc. Correct data types are critical: if a date column is loaded as Text, you cannot do date arithmetic. Power Query sometimes auto-detects types incorrectly (especially for numbers stored as text), so always verify types in the "Changed Type" step. Setting types correctly also improves performance in Power BI data models.

---

## Q11. What is the M language in Power Query?

**A:** M (also called the Power Query Formula Language) is the underlying functional programming language that powers all transformations in Power Query. Every action you perform in the GUI (filter, merge, unpivot, etc.) generates M code behind the scenes, visible in the **Advanced Editor**. M is case-sensitive and expression-based. While most MIS work does not require writing M from scratch, knowing how to read and modify M code — like adding a dynamic date parameter or a conditional expression — is a strong differentiator in interviews.

---

## Q12. What happens when you click "Refresh" on a Power Query?

**A:** When you refresh, Power Query re-executes all the recorded steps from scratch — it reconnects to the source, pulls fresh data, applies every transformation step in sequence, and loads the result into the destination (Excel worksheet or data model). If the source file has moved or the connection has changed, the refresh will fail. In Excel, you can refresh via **Data → Refresh All** or right-clicking the query. Scheduled refresh in Power BI Service automates this without manual intervention.

---

## Q13. What is the Applied Steps panel in Power Query?

**A:** The Applied Steps panel (on the right side of the Power Query Editor) shows a sequential list of every transformation step recorded in your query. Each step has a name (e.g., "Source," "Promoted Headers," "Changed Type," "Filtered Rows"). You can click any step to preview the data at that point, rename steps for clarity, delete unwanted steps, or reorder them. It functions like an undo/redo history that persists permanently. Understanding the Applied Steps panel is essential for debugging and auditing queries.

---

## Q14. What is the difference between connecting to an Excel Table vs a Named Range?

**A:** When connecting to an **Excel Table** (Insert → Table), Power Query can directly reference it by name and automatically picks up new rows added to the table — making it fully dynamic. A **Named Range** is a fixed cell reference given a name; Power Query can connect to it too, but it does not auto-expand when new rows are added unless the range definition is updated. For MIS automation, Excel Tables are strongly preferred as data sources because they grow automatically and keep queries stable.

---

## Q15. How do you add a Conditional Column in Power Query?

**A:** Go to **Add Column → Conditional Column**. A dialog lets you define IF-THEN-ELSE logic: if Column X equals/contains/starts with a value, then output a specific result, else another result. Multiple conditions can be added (like nested IFs). This is the GUI equivalent of writing an IF statement and is useful for creating category buckets, flags (Yes/No), or status labels from raw data. For more complex logic, you can edit the generated M code in the formula bar.

---

## Q16. How does Group By work in Power Query?

**A:** **Group By** (Home → Group By or Transform → Group By) aggregates data similarly to a Pivot Table or SQL GROUP BY. You select one or more columns to group on, and then define aggregation operations (Sum, Count, Average, Min, Max, etc.) on other columns. For example, grouping by Region and summing Sales gives you total sales per region. It collapses the table into summary rows. This is useful for building summary tables that feed dashboards or reports, all refreshable automatically.

---

## Q17. How do you remove blank or null rows in Power Query?

**A:** The quickest method is to click the dropdown arrow on a key column, uncheck "null" and blank entries, and click OK — this adds a "Filtered Rows" step. Alternatively, go to **Home → Remove Rows → Remove Blank Rows** to remove rows where every cell is blank. For null values in specific columns, use **Filter → Does not equal → null**. Removing blanks early in the query prevents errors in downstream calculations and aggregations.

---

## Q18. How do you trim whitespace from text columns in Power Query?

**A:** Select the text column, then go to **Transform → Format → Trim**. This removes leading and trailing spaces from all values in the column. There is also **Clean** (removes non-printable characters) and **Trim** can be combined with it. Whitespace issues are a very common data quality problem — they cause VLOOKUP/MATCH failures because " Sales" ≠ "Sales." In M, the equivalent function is `Text.Trim([ColumnName])`. Always trim text columns when standardizing master data or joining two datasets.

---

## Q19. How do you extract parts of a date column in Power Query?

**A:** Select a date column, then go to **Add Column → Date → Year / Month / Month Name / Quarter / Week of Year / Day / Day Name**, etc. Each option adds a new column with the extracted component. You can also use **Transform → Date** to replace the original column. This is very useful for creating Time Intelligence groupings — extracting Month and Year from transaction dates for monthly MIS summaries. In M, the functions are `Date.Year([Date])`, `Date.Month([Date])`, `Date.MonthName([Date])`, etc.

---

## Q20. How do you combine multiple files from a folder using Power Query?

**A:** Go to **Get Data → From Folder**, select the folder path, and Power Query will list all files in that folder. Click "Combine" or "Combine & Transform" — Power Query will automatically open the first file as a sample, let you pick which sheet/table to extract, and then apply the same transformation to all files, stacking them into one table. It also adds a "Source.Name" column showing which file each row came from. This is the best practice for consolidating monthly reports that are saved as separate files in one folder.

---

## Q21. What are Query Dependencies in Power Query?

**A:** When one query references another query (e.g., a final output query that builds on a staging/cleaning query), a dependency is created. You can visualize these using **View → Query Dependencies** in the Power Query Editor, which shows a diagram of how queries feed into each other. Understanding dependencies is important because refreshing a parent query triggers all dependent queries. Circular dependencies (Query A → Query B → Query A) are not allowed and will cause errors.

---

## Q22. How is Power Query different from a Pivot Table?

**A:** Power Query is a **data transformation and loading tool** — it cleans, reshapes, and loads data. A **Pivot Table** is a **data analysis and summarization tool** — it aggregates and cross-tabulates data that has already been loaded. You typically use Power Query first to clean and structure the data, then use a Pivot Table on top of that clean data for analysis. Power Query does not display results interactively like a Pivot Table; it outputs a static table. Together they form a powerful workflow: clean with Power Query, analyze with Pivot.

---

## Q23. When should you use Power Query vs writing Excel formulas?

**A:** Use Power Query when: (1) you have large datasets (10,000+ rows) where formulas slow down Excel, (2) you need to repeat the same cleaning process on fresh data regularly, (3) you need to combine data from multiple files or sources, or (4) the transformation is complex (merges, unpivots, group by). Use formulas when the data is small, mostly static, and the transformation is simple. Power Query transformations are faster, more reliable, and auditable compared to formula-heavy sheets that are fragile and hard to maintain.

---

## Q24. What are some performance tips for Power Query?

**A:** (1) **Filter early** — remove unnecessary rows and columns as close to the source step as possible to reduce data volume processed downstream. (2) **Avoid unnecessary steps** — each step adds processing overhead. (3) Disable "Background Refresh" if it causes slowness. (4) Use **native database queries** (SQL passthrough) when connecting to databases to push filtering to the server. (5) Turn off column profiling in the Editor when not needed. (6) Load only to the data model (not to the worksheet) if the data is only used for Pivot Tables or Power BI.

---

## Q25. How does Power Query handle errors, and how do you fix them?

**A:** Errors in Power Query appear as "Error" cells in the preview. You can handle them using **Transform → Replace Errors** to substitute a default value (like 0 or "Unknown") for any error in a column. You can also use **Remove Rows → Remove Errors** to delete rows that contain errors. In M language, you can use `try ... otherwise` syntax for fine-grained error handling. Common error causes include: data type mismatches, missing files, changed column names in the source, and division by zero.

---

## Q26. What does "Load to Data Model" mean in Power Query?

**A:** When you choose "Load to Data Model" (via Close & Load To → Only Create Connection + Add to Data Model), the query data is loaded into Excel's internal Power Pivot engine (xVelocity in-memory columnar storage) instead of a worksheet. This allows you to: handle millions of rows beyond Excel's 1M row limit, create relationships between multiple tables, and use DAX measures in Pivot Tables. It is the foundation for building multi-table data models in Excel. In Power BI, all queries load to the data model by default.

---

## Q27. What is ETL and how does Power Query implement it?

**A:** ETL stands for **Extract, Transform, Load** — the three stages of data integration. **Extract**: pulling data from source systems (databases, files, APIs). **Transform**: cleaning, reshaping, and enriching the data (removing duplicates, changing types, merging tables, etc.). **Load**: writing the final clean data to a destination (Excel table, data model, database). Power Query implements the full ETL pipeline in a visual, no-code/low-code environment. Each Applied Step corresponds to a transformation, and "Close & Load" is the load phase.

---

## Q28. What is a data cleaning checklist you follow before analysis?

**A:** A standard data cleaning checklist includes: (1) Remove duplicate rows, (2) Handle missing/null values (fill, remove, or flag), (3) Correct data types (dates as dates, numbers as numbers), (4) Trim whitespace from text columns, (5) Standardize inconsistent values (e.g., "Male"/"male"/"M" → "Male"), (6) Remove irrelevant columns, (7) Fix structural errors (extra headers, merged cells), (8) Validate value ranges (no negative ages, no future dates for historical data), (9) Rename columns for clarity, and (10) Validate row counts before and after cleaning.

---

## Q29. What are common data quality issues in MIS reporting?

**A:** The most common issues are: (1) **Duplicates** — same transaction recorded twice, (2) **Blanks/Nulls** — missing values in key fields like Employee ID or Date, (3) **Inconsistent formats** — dates in DD/MM/YYYY in some rows and MM-DD-YYYY in others, (4) **Whitespace** — "Mumbai " vs "Mumbai" causing mismatches, (5) **Wrong data types** — numbers stored as text, (6) **Outliers** — extreme values due to data entry errors, (7) **Stale data** — report refreshed with old source file, and (8) **Structural issues** — merged cells, multiple headers, or total rows embedded in data.

---

## Q30. What are best practices for organizing Power Query in a workbook?

**A:** (1) **Name queries clearly** — use descriptive names like "Raw_Sales," "Clean_Sales," "Final_Summary" instead of "Query1." (2) **Group related queries** — use query groups (right-click → Move to Group) to organize staging, transformation, and output queries. (3) **Use staging queries** — separate raw load from transformation from final output for easier debugging. (4) **Document steps** — rename Applied Steps to describe what each step does. (5) **Avoid hardcoding paths** — use parameters for file paths to make workbooks portable. (6) **Test after every structural source change** — renamed columns in the source break queries immediately.

---

*End of File — 30 Questions Covered*
