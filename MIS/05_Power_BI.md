# Power BI — 30 Interview Questions

> For MIS Executive interviews — asked at Deloitte, EY, Accenture, Amazon, Flipkart

---

## Q1. What is Power BI and what is it used for?

**A:** Power BI is a business intelligence and data visualization tool developed by Microsoft that allows users to connect to multiple data sources, transform raw data, build data models, create interactive reports, and share dashboards with stakeholders. It is used for making data-driven decisions by converting complex data into visually intuitive charts, graphs, and KPI cards. In MIS roles, Power BI is used to automate reporting, replace static Excel dashboards, and provide real-time or scheduled data refreshes to management. It is available as a free Desktop version and a cloud-based Service (Power BI Pro/Premium).

---

## Q2. What is the difference between Power BI Desktop, Power BI Service, and Power BI Mobile?

**A:** **Power BI Desktop** is a free Windows application where you build reports — connect to data, model it, write DAX, and design visualizations. **Power BI Service** (app.powerbi.com) is the cloud platform where you publish, share, schedule refreshes, and collaborate on reports and dashboards; it requires a Pro or Premium license for sharing. **Power BI Mobile** is the iOS/Android app that allows end-users to view and interact with published reports and dashboards on smartphones and tablets. The typical workflow is: build in Desktop → publish to Service → consume on Mobile.

---

## Q3. What are the main components of Power BI?

**A:** The key components are: (1) **Power Query Editor** — for connecting to data sources and transforming/cleaning data (ETL layer), (2) **Data Model** — the in-memory columnar database where tables, relationships, and calculated columns/measures live, (3) **DAX** — the formula language for creating measures and calculated columns, (4) **Report Canvas** — the drag-and-drop visual design surface where you build charts and visuals, (5) **Power BI Service** — the cloud platform for publishing and sharing, and (6) **Dashboards** — curated single-page views pinned from multiple reports in the Service.

---

## Q4. What is a Data Model in Power BI?

**A:** A data model in Power BI is the structured set of tables along with the relationships defined between them, stored in the in-memory VertiPaq engine. Instead of working with a single flat table, you connect multiple related tables (e.g., Sales, Product, Customer, Date) and define how they relate to each other via key columns. The data model enables cross-table calculations using DAX and allows Pivot/visual filters to work across related tables automatically. A well-designed data model (star schema) is the foundation of a fast and accurate Power BI report.

---

## Q5. What are the types of relationships in Power BI and how do they differ?

**A:** Power BI supports three relationship cardinalities: **One-to-Many (1:*)** — the most common, where one row in the dimension/lookup table corresponds to many rows in the fact table (e.g., one Product to many Sales). **One-to-One (1:1)** — each row in Table A matches exactly one row in Table B; often indicates tables that should be merged. **Many-to-Many (*:*)** — multiple rows in both tables can match; requires careful handling (a bridge table is preferred). Relationships also have a direction (single or bidirectional) that controls how filter context flows between tables.

---

## Q6. What is the difference between a Star Schema and a Snowflake Schema?

**A:** In a **Star Schema**, a central fact table is directly connected to all dimension tables in a single level — simple and efficient for Power BI. In a **Snowflake Schema**, dimension tables are further normalized into sub-dimension tables (e.g., Product → Category → Department), creating multiple levels of joins. Star schema is strongly preferred in Power BI because it minimizes the number of relationships, reduces model complexity, and allows the VertiPaq engine to compress and query data most efficiently. Snowflake schemas can slow down query performance and complicate DAX.

---

## Q7. What is DAX and what is it used for in Power BI?

**A:** DAX (Data Analysis Expressions) is a formula language used in Power BI, Power Pivot, and Analysis Services to create **measures** (dynamic calculations) and **calculated columns** (row-level computed columns). It has functions similar to Excel but designed to work on entire columns and tables rather than individual cells, and it is context-aware (responds to filters applied by slicers, visuals, and report filters). DAX is what makes Power BI reports dynamic — the same measure can show total sales for the whole company or just for one region depending on the filter context. Examples: `SUM`, `CALCULATE`, `FILTER`, `SUMX`, `RANKX`.

---

## Q8. What is the difference between a Measure and a Calculated Column in Power BI?

**A:** A **Measure** is a dynamic DAX calculation evaluated at query time based on the current filter context — it does not exist as a stored column in the table and recalculates every time a visual changes. Example: `Total Sales = SUM(Sales[Amount])`. A **Calculated Column** is computed row-by-row at data refresh time and stored in the table, consuming memory. Example: `Full Name = [First Name] & " " & [Last Name]`. Best practice: use measures for aggregations and KPIs; use calculated columns only when you need the computed value available as a row attribute (e.g., for slicing/filtering).

---

## Q9. Explain some common DAX functions used in MIS reporting.

**A:** Key DAX functions include: **SUM/AVERAGE/COUNT/MIN/MAX** — basic aggregations. **CALCULATE** — modifies filter context for a calculation. **FILTER** — returns a subset of a table meeting a condition. **ALL** — removes all filters from a table or column (used in % of total). **RELATED** — fetches a value from a related table (like VLOOKUP). **DIVIDE** — safe division that handles divide-by-zero. **IF / SWITCH** — conditional logic. **SUMX / AVERAGEX** — row-by-row iteration over a table before aggregating. **RANKX** — ranks rows by a measure. **DISTINCTCOUNT** — counts unique values. **PREVIOUSMONTH / SAMEPERIODLASTYEAR** — time intelligence for MoM/YoY comparisons.

---

## Q10. What is Filter Context in Power BI DAX?

**A:** Filter context is the set of filters currently active when a DAX measure is evaluated — it is defined by slicers, visual filters, report-level filters, row/column headers of a matrix, and the `CALCULATE` function. For example, if a slicer is set to "North Region," every measure on the report page evaluates only for that region's data. Understanding filter context is the most fundamental concept in DAX — it explains why the same measure `SUM(Sales[Amount])` shows different values in different cells of a matrix visual. CALCULATE is the primary tool for modifying filter context.

---

## Q11. What is Row Context in DAX?

**A:** Row context is the context in which a DAX expression is evaluated one row at a time — it occurs in calculated columns and iterator functions (SUMX, AVERAGEX, RANKX, etc.). In a calculated column, DAX automatically knows which row it is evaluating, so `[Revenue] = [Quantity] * [Unit Price]` computes correctly for each row. In measures, row context does not exist by default — you need iterator functions to create it. A common interview question is the difference between filter context and row context, which is fundamental to writing correct DAX.

---

## Q12. Explain the CALCULATE function with an example.

**A:** `CALCULATE` is the most powerful DAX function — it evaluates an expression in a modified filter context. Syntax: `CALCULATE(expression, filter1, filter2, ...)`. Example: `Sales_North = CALCULATE(SUM(Sales[Amount]), Region[Region] = "North")` — this returns total sales for the North region regardless of what slicer is selected. Another example: `Sales_AllRegions = CALCULATE(SUM(Sales[Amount]), ALL(Region))` — removes region filter to get grand total (used for % of total calculations). Without CALCULATE, you cannot override or add to the existing filter context from within a measure.

---

## Q13. What is the difference between Slicers and Filters in Power BI?

**A:** **Slicers** are visual elements placed on the report canvas that users interact with directly — they are visible, intuitive, and user-friendly (dropdowns, buttons, date ranges). **Filters** are set in the Filters pane (on the right) and can be applied at three levels: Visual-level (only affects one chart), Page-level (affects all visuals on one page), and Report-level (affects all pages). Slicers are report-level by default but can be synced across pages. Use slicers for frequently changed, end-user-facing filters and use the Filters pane for fixed or hidden filters.

---

## Q14. What types of visuals are available in Power BI and when do you use them?

**A:** Common visuals and their use cases: **Bar/Column Chart** — compare categories. **Line Chart** — show trends over time. **Matrix** — multi-dimensional crosstab (like a Pivot Table). **Card** — display a single KPI value. **Gauge** — show progress toward a target. **Map/Filled Map** — geographic data. **Treemap** — part-to-whole with hierarchical data. **Funnel** — stages in a process (sales pipeline). **Scatter Plot** — correlation between two measures. **Table** — row-level detail data. **Donut/Pie** — part-to-whole (for small number of categories). Custom visuals from the AppSource marketplace can be imported for specialized needs.

---

## Q15. What is the difference between a Matrix visual and a Table visual?

**A:** A **Table** visual displays data in a flat row-column format — each row corresponds to one record or aggregated group, with no hierarchical structure. A **Matrix** visual supports row and column hierarchies — you can place dimensions on both the row and column axes (like a Pivot Table), and it supports drill-down, subtotals, and grand totals. In MIS reporting, a Matrix is preferred for cross-tab reports (e.g., Region × Month × Sales), while a Table is better for raw detail listings or simple summaries. Both support conditional formatting and totals.

---

## Q16. What is the difference between Cross-Filtering and Cross-Highlighting in Power BI?

**A:** **Cross-highlighting** is the default behavior — when you click a bar in one chart, other charts on the page dim the unrelated portions while keeping all data visible (related data is highlighted, unrelated data is grayed out). **Cross-filtering** actually filters out unrelated data entirely, showing only the filtered subset in other visuals — selected via Edit Interactions. You can control the interaction type between any two visuals (highlight, filter, or none) in the Format → Edit Interactions mode. Cross-filtering gives a cleaner view; cross-highlighting preserves context of the full dataset.

---

## Q17. What is the difference between a Report and a Dashboard in Power BI Service?

**A:** A **Report** is a multi-page document created in Power BI Desktop, containing interactive visuals with full cross-filtering, slicers, drill-through, and detailed analysis capabilities — it is tied to a single dataset. A **Dashboard** is a single-page canvas in Power BI Service where you can pin tiles (individual visuals) from multiple different reports and datasets — it provides a high-level overview but has limited interactivity (no slicers, no cross-filtering). Dashboards can trigger data alerts (notify when a KPI crosses a threshold). Typically: analysts build Reports; executives use Dashboards.

---

## Q18. What is a Workspace in Power BI Service?

**A:** A Workspace is a collaborative container in Power BI Service where reports, datasets, dashboards, and dataflows are stored and managed by a team. There are two types: **My Workspace** (personal, not shareable) and **Shared Workspaces** (collaborative, supports multiple roles). Within a workspace, you can assign roles — Admin, Member, Contributor, or Viewer — to control what each user can do. Reports published from Power BI Desktop go to a specified workspace. Apps are created from workspaces to distribute content to a broader audience in a controlled, read-only format.

---

## Q19. How do you publish a report from Power BI Desktop to Power BI Service?

**A:** In Power BI Desktop, click **File → Publish → Publish to Power BI** (or use the Home → Publish button). You will be prompted to sign in with your Microsoft/organizational account and then select the destination workspace. Once published, the report and its dataset appear in the chosen workspace on app.powerbi.com. After publishing, you can configure a scheduled refresh for the dataset, set up Row-Level Security, or share the report with others. Any edits in Desktop require re-publishing to update the Service version.

---

## Q20. What is Row-Level Security (RLS) in Power BI?

**A:** Row-Level Security (RLS) restricts the data visible to specific users within the same report. You define RLS roles in Power BI Desktop using DAX filter rules (e.g., `[Region] = USERNAME()` or a static filter like `[Region] = "North"`). After publishing, you assign users or security groups to these roles in Power BI Service under **Dataset → Security**. This way, a North Region manager logs into the same report but only sees North data, while a South manager sees South data — all from one shared report and dataset. RLS is a critical security and governance feature.

---

## Q21. What is Power BI Gateway and why is it needed?

**A:** Power BI Gateway is a software agent installed on a local machine (or server) that acts as a bridge between Power BI Service (cloud) and on-premises data sources like local SQL Server, Oracle databases, or network file shares. Since Power BI Service runs in the cloud, it cannot directly access data sitting behind a corporate firewall. The Gateway securely transfers data between on-premises sources and the cloud for scheduled refreshes. There are two types: **On-premises data gateway** (shared, for multiple users) and **Personal mode gateway** (for a single user's use only).

---

## Q22. How do you set up a scheduled refresh in Power BI Service?

**A:** After publishing a report, go to the dataset in Power BI Service → **Settings → Scheduled Refresh**. Toggle it on, select the refresh frequency (daily, weekly, specific times — up to 8 times/day for Pro, 48 times/day for Premium), and set the time zone. The dataset must have a configured data source connection with saved credentials. If the data is on-premises, a Gateway must be configured and running. You can also trigger a manual refresh anytime. Refresh failures send email notifications to the dataset owner, enabling proactive monitoring.

---

## Q23. What are Bookmarks and how are they used for navigation in Power BI?

**A:** Bookmarks capture the current state of a report page — including which filters are applied, which visuals are visible, and scroll position — and save it as a named snapshot. They are created via **View → Bookmarks**. When combined with **Buttons** (Insert → Buttons → Blank), bookmarks enable interactive navigation: clicking a button applies a bookmark to switch views, show/hide visuals, or simulate a page navigation experience. This is how you build "tabs," "show/hide filter panels," or multi-scenario dashboards in Power BI. Bookmarks make reports feel like polished, app-like experiences.

---

## Q24. What is Drill-Through in Power BI?

**A:** Drill-through allows a user to right-click a data point in a visual and navigate to a dedicated detail page filtered to that specific item. For example, right-clicking "North" in a region chart could drill through to a "Region Detail" page showing all transactions for North. To set it up: create a separate report page, drag the drill-through field (e.g., Region) into the Drill-Through section of that page's Filters pane. Power BI automatically adds a back button on the detail page. Drill-through is used to avoid cluttering summary reports with detail tables while still providing access to granular data.

---

## Q25. What are Tooltip Pages in Power BI?

**A:** Tooltip Pages are special report pages in Power BI that appear as rich, custom tooltips when a user hovers over a data point in a visual — replacing the default simple tooltip. To create one: add a new page, go to Page Properties → set "Tooltip" to On and "Page Size" to Tooltip. Add the visuals you want to appear on hover. Then, in the target visual's Format pane → Tooltip, enable "Report Page" and select your tooltip page. This is a very impressive feature for interviews — it shows you can build reports that provide contextual deep-dives without cluttering the main canvas.

---

## Q26. What is a Mobile Layout in Power BI?

**A:** Mobile Layout allows you to design an optimized view of your report page specifically for smartphone screens. In Power BI Desktop, go to **View → Mobile Layout**. A phone canvas appears where you can drag, resize, and rearrange the visuals from the current page into a portrait-oriented layout. When a mobile user views the report in the Power BI Mobile app, they automatically see this optimized layout instead of the full desktop layout. Not all visuals need to be included — you can choose to show only the most important KPIs and charts for mobile users.

---

## Q27. What is the SAMEPERIODLASTYEAR function and how is it used?

**A:** `SAMEPERIODLASTYEAR` is a time intelligence DAX function that returns a table of dates shifted back exactly one year, used to calculate the same period's value from the prior year. Example: `Sales_LY = CALCULATE(SUM(Sales[Amount]), SAMEPERIODLASTYEAR(Date[Date]))`. This requires a proper Date table with a continuous date range marked as "Date Table." With this measure, you can easily calculate Year-over-Year growth: `YoY% = DIVIDE([Total Sales] - [Sales_LY], [Sales_LY])`. Other similar functions: `PREVIOUSMONTH`, `PREVIOUSYEAR`, `DATEADD`, `PARALLELPERIOD`.

---

## Q28. What are some performance optimization tips for Power BI reports?

**A:** Key performance tips: (1) **Reduce model size** — import only needed columns, avoid high-cardinality text columns in fact tables. (2) **Use star schema** — minimize the number of relationships and avoid many-to-many. (3) **Write efficient DAX** — avoid row-by-row iterator functions on large tables when a simpler aggregation works; prefer `SUMX` with small tables. (4) **Limit visuals per page** — each visual runs a separate query; fewer visuals = faster load. (5) **Use aggregations** for large datasets. (6) **Avoid calculated columns** where measures suffice — columns consume RAM. (7) Use **Analyze in Excel** or **Performance Analyzer** (View → Performance Analyzer) to identify slow visuals.

---

## Q29. What is DISTINCTCOUNT and when would you use it in MIS?

**A:** `DISTINCTCOUNT(column)` counts the number of unique values in a column, ignoring duplicates. In MIS reporting, it is used for metrics like: number of unique customers who made a purchase, number of distinct SKUs sold, unique agents handling tickets, or number of active employees in a month. Example: `Unique_Customers = DISTINCTCOUNT(Sales[Customer_ID])`. Unlike `COUNT` (which counts all non-blank rows) or `COUNTA`, DISTINCTCOUNT gives the count of unique/individual entities — essential for customer acquisition and engagement metrics commonly asked about in interviews.

---

## Q30. Explain the RANKX function with a practical example.

**A:** `RANKX` ranks values in a table based on a measure. Syntax: `RANKX(table, expression, [value], [order], [ties])`. Example: `Region_Rank = RANKX(ALL(Region[Region]), [Total Sales])` — this ranks each region from highest to lowest total sales, regardless of the current filter context (`ALL` removes filters so all regions are ranked together). It is used in MIS to build top-N leaderboards, agent performance rankings, or product sales rankings. The `order` argument is `DESC` (1 = highest) by default; set to `ASC` for lowest-first ranking.

---

*End of File — 30 Questions Covered*
