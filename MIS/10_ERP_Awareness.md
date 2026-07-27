# ERP System Awareness — 30 Interview Questions

> For MIS Executive interviews — ERP data extraction and system awareness

---

**1. What is ERP (Enterprise Resource Planning)?**

ERP (Enterprise Resource Planning) is an integrated software system that manages and automates core business processes — including finance, procurement, inventory, sales, HR, and manufacturing — within a single platform. Instead of using separate systems for each department, ERP provides a unified database so all teams work from the same data. Examples include SAP, Oracle ERP, Microsoft Dynamics, and Tally. ERP eliminates data silos and enables real-time, organization-wide reporting.

---

**2. Why do companies use ERP systems?**

Companies use ERP to: (1) integrate data across departments into one system, (2) eliminate redundant data entry and manual processes, (3) enable real-time reporting and decision-making, (4) enforce standard business processes and controls, and (5) scale operations efficiently as the company grows. Without ERP, companies rely on disconnected spreadsheets and emails, leading to data inconsistencies and reporting delays. ERP is the backbone of data in most mid-to-large organizations.

---

**3. What are the major ERP systems used in industry?**

Major ERP systems include: SAP (most widely used globally, dominant in large enterprises), Oracle ERP (popular in BFSI and large corporates), Microsoft Dynamics 365 (popular in mid-sized companies), Tally (widely used in India for SME accounting and inventory), Zoho Books (cloud-based, popular with small businesses), and Odoo (open-source, used by growing mid-sized companies). An MIS Executive should know which ERP their company uses and how to extract data from it.

---

**4. What is SAP and what does it stand for?**

SAP stands for Systeme, Anwendungen, und Produkte in der Datenverarbeitung — German for "Systems, Applications, and Products in Data Processing." It is the world's leading ERP software, developed by a German company founded in 1972. SAP is used by thousands of large enterprises globally across manufacturing, retail, banking, telecom, and government sectors. For an MIS Executive, SAP is the most important ERP system to have awareness of, as it is the source of most enterprise reporting data.

---

**5. What are the major modules in SAP?**

Major SAP modules include: FI (Financial Accounting) — general ledger, accounts payable/receivable; CO (Controlling) — cost centers, profit centers, internal reporting; SD (Sales & Distribution) — sales orders, pricing, billing; MM (Materials Management) — procurement, inventory, goods receipts; HR/HCM (Human Capital Management) — payroll, attendance, employee data; PP (Production Planning) — manufacturing orders and scheduling. An MIS Executive typically interacts most with FI, SD, MM, and HR data.

---

**6. What is a Transaction Code (T-code) in SAP?**

A Transaction Code (T-code) is a shortcut command in SAP that directly opens a specific function or report screen. Instead of navigating through menus, users type the T-code in the command bar and press Enter. For example, typing `SE16N` opens the table viewer for data extraction, while `VA05` opens the list of sales orders. T-codes make SAP navigation fast and efficient. MIS Executives who know the right T-codes can extract data quickly without needing SAP expertise.

---

**7. What are common SAP T-codes used by MIS professionals?**

Commonly used SAP T-codes for MIS data extraction: `SE16` / `SE16N` — view and extract data from any SAP database table; `VA05` — list of sales orders by customer or date range; `ME2M` — list of purchase orders by material; `MB51` — material document list (goods movements and inventory transactions); `S_ALR_87012284` — vendor line item report (AP); `FBL5N` — customer line item report (AR). Knowing these T-codes allows MIS executives to pull raw data directly from SAP for reporting.

---

**8. What is SE16N in SAP and how is it used by MIS?**

SE16N is a SAP T-code that provides direct access to any SAP database table — it is essentially SAP's data browser. MIS Executives use SE16N to extract raw transactional data by entering the table name, applying filters (e.g., date range, company code), and exporting results to Excel. For example, `VBAK` is the sales order header table; `MSEG` is the material document table. SE16N is one of the most powerful data extraction tools in SAP for MIS purposes, bypassing the need for custom ABAP reports.

---

**9. What is an SAP Report and how is it generated?**

An SAP Report is a structured output generated from SAP that summarizes transactional or master data — for example, a monthly sales report, an open purchase order list, or an inventory aging report. Reports in SAP are accessed via T-codes or the SAP menu path. Users enter selection criteria (date range, company code, plant, etc.) and SAP generates the report. The output can be exported to Excel, PDF, or text file. Standard SAP reports cover most common MIS needs; custom reports require ABAP programming.

---

**10. What is the difference between ABAP reports and Standard SAP reports?**

Standard SAP reports are built-in reports delivered with SAP — they are ready to use with no customization needed (e.g., VA05 for sales orders, MB51 for material movements). ABAP reports are custom-developed programs written by SAP developers in ABAP (Advanced Business Application Programming) language to meet specific business reporting needs that standard reports cannot fulfill. MIS Executives typically use standard reports and SE16N for data extraction; ABAP reports are requested from the IT/SAP team when standard options are insufficient.

---

**11. How does an MIS Executive typically extract data from SAP?**

An MIS Executive extracts data from SAP through: (1) Running standard SAP reports (T-codes like VA05, MB51) and exporting via List > Save > Local File > Spreadsheet, (2) Using SE16N to query specific database tables and export to Excel, (3) Requesting scheduled SAP report outputs that auto-export to a shared drive, or (4) Accessing SAP-connected BI tools (like SAP Business Objects or Power BI) that pull live SAP data. The exported Excel file is then cleaned, formatted, and used to build MIS reports.

---

**12. What is Oracle ERP and which industries use it?**

Oracle ERP (Oracle Fusion Cloud ERP / Oracle E-Business Suite) is a comprehensive ERP platform developed by Oracle Corporation, competing directly with SAP at the enterprise level. It is widely used in: Banking & Financial Services, Telecommunications, Retail and e-Commerce, Healthcare, and Government. Oracle ERP is known for its strong financial management, project accounting, and supply chain modules. MIS professionals in Oracle environments use Oracle's reporting tools (OTBI, BI Publisher) or export data to Excel for analysis.

---

**13. What is Tally and which companies use it?**

Tally (now Tally Prime) is an Indian accounting and ERP software widely used by SMEs (Small and Medium Enterprises) in India and South Asia for accounting, inventory management, GST compliance, payroll, and banking. It is the most popular accounting software for Indian businesses below the enterprise scale. MIS Executives in companies using Tally extract data via Tally's built-in report exports (Day Book, Ledger, Stock Summary) to Excel. Tally is significantly simpler than SAP but covers core financial and inventory reporting needs for SMEs.

---

**14. What is a General Ledger (GL) in ERP?**

The General Ledger (GL) is the master financial record in ERP that contains all financial transactions of a company — every debit and credit entry from all sub-ledgers (accounts payable, accounts receivable, payroll, etc.) is posted to the GL. It is the foundation of financial statements (Balance Sheet and P&L). In SAP, the GL is managed in the FI module; the T-code `FB03` views GL documents and `S_ALR_87012301` generates GL account balances. MIS finance reports are often sourced from GL data.

---

**15. What is Accounts Payable (AP) vs Accounts Receivable (AR) in ERP?**

Accounts Payable (AP) tracks money owed by the company to its vendors/suppliers — it records purchase invoices and payments made. Accounts Receivable (AR) tracks money owed to the company by its customers — it records sales invoices and payments received. In SAP: AP is managed in the FI module (T-code `FBL1N` for vendor line items); AR is tracked via `FBL5N` for customer line items. MIS reports often include aging analysis of AP and AR to help finance teams manage cash flow.

---

**16. What is a Purchase Order (PO) and how does it flow in ERP?**

A Purchase Order (PO) is a formal document issued by a company to a vendor, confirming the purchase of goods or services at an agreed price and quantity. In ERP (SAP MM module), the PO flow is: Purchase Requisition (PR) → Purchase Order (PO) → Goods Receipt (GRN) → Invoice Verification → Payment. The T-code `ME23N` displays a PO in SAP; `ME2M` lists POs by material. MIS Executives track open POs, pending GRNs, and procurement cycle times for operations reporting.

---

**17. What is a GRN (Goods Receipt Note)?**

A GRN (Goods Receipt Note) is a document generated in ERP when purchased goods are received from a vendor and accepted into inventory. It confirms that the quantity and quality of goods received match the Purchase Order. In SAP, GRNs are posted using T-code `MIGO` and viewed via `MB51`. GRN data is critical for MIS reporting on procurement cycle times (PO to GRN days), inventory updates, and 3-way matching (PO → GRN → Invoice) for payment processing.

---

**18. What is inventory management in ERP?**

Inventory management in ERP tracks the movement, quantity, location, and value of stock across warehouses and plants in real time. In SAP MM, inventory transactions include goods receipts, goods issues, stock transfers, and returns. Key MIS inventory reports include: current stock levels (T-code `MMBE`), material movements (`MB51`), and slow-moving or non-moving stock reports. Accurate inventory data from ERP allows MIS to report on stock turnover, inventory aging, and warehouse fill rates.

---

**19. What is the Order-to-Cash (O2C) process?**

The Order-to-Cash (O2C) process covers the end-to-end cycle from receiving a customer order to collecting payment. Steps: Customer Order → Order Confirmation → Delivery & Shipping → Billing/Invoice → Accounts Receivable → Payment Receipt. In SAP, this process runs through the SD and FI modules. MIS Executives report on O2C metrics like order fulfillment rate, delivery TAT, invoice-to-payment days (DSO — Days Sales Outstanding), and revenue realized per period.

---

**20. What is the Procure-to-Pay (P2P) process?**

The Procure-to-Pay (P2P) process covers the end-to-end procurement cycle from identifying a need to paying the vendor. Steps: Purchase Requisition → Purchase Order → Goods Receipt (GRN) → Invoice Receipt → Invoice Verification → Payment to Vendor. In SAP, this flows through MM and FI modules. MIS metrics for P2P include: PO to GRN cycle time, invoice processing time, vendor payment aging, and PO compliance rate (% of purchases with a valid PO).

---

**21. What is Master Data in ERP?**

Master data is the core, stable reference data in ERP that is used repeatedly across transactions — unlike transactional data which changes with every order. Key master data types include: Customer Master (customer name, address, payment terms, credit limit), Vendor Master (supplier details, bank account, payment terms), and Material Master (product description, unit of measure, price, storage information). Master data quality directly impacts reporting accuracy — incorrect customer or material codes lead to wrong report outputs.

---

**22. What is a Cost Center in SAP?**

A Cost Center in SAP (CO module) is an organizational unit that represents a specific area of the business where costs are incurred and tracked — for example, a department (HR, IT, Sales) or a location (Mumbai Plant, Delhi Office). Every expense is assigned to a cost center so management can see departmental spending. MIS Executives use cost center reports to build department-wise cost tracking dashboards and to support budget vs. actual variance analysis.

---

**23. What is a Profit Center in SAP?**

A Profit Center in SAP (CO module) is an organizational unit used to track both revenues and costs, enabling profit and loss analysis at a sub-company level — for example, by product line, business unit, or region. Unlike a cost center (which only tracks costs), a profit center shows whether a business segment is profitable. MIS finance reports often segment P&L by profit center to help management evaluate the performance of individual business units.

---

**24. What is a Company Code in SAP?**

A Company Code in SAP represents an independent legal entity for which a complete, self-contained set of accounts can be drawn up (balance sheet and P&L). In a group of companies, each subsidiary or legal entity has its own company code. All financial postings in SAP are made under a company code. MIS Executives working in multi-entity organizations must know the relevant company codes to filter data correctly when extracting reports from SAP.

---

**25. What data does MIS typically pull from ERP?**

MIS Executives commonly extract the following data from ERP: Sales data (orders, revenue, invoices — from SD/AR), Procurement data (POs, GRNs, vendor payments — from MM/AP), Inventory data (stock levels, movements — from MM), Financial data (GL balances, cost center expenses — from FI/CO), and HR data (headcount, payroll costs — from HCM). This data is exported to Excel, cleaned, and used to build operational and financial MIS reports for management.

---

**26. How do you export data from SAP to Excel?**

To export data from SAP to Excel: (1) Run the report or SE16N query in SAP, (2) Once the output is displayed, go to the menu: List > Save > Local File, (3) Choose the format "Spreadsheet" (.xlsx) or "Text with Tabs" (.txt), (4) Choose the save location on your computer, and (5) Open the exported file in Excel for further cleaning and analysis. Some SAP versions allow direct export via a toolbar button (the Excel icon). Always verify that all rows exported correctly — SAP sometimes limits default output rows.

---

**27. What is CRM and how does it differ from ERP?**

CRM (Customer Relationship Management) is a system focused specifically on managing interactions with customers — tracking leads, sales pipeline, customer service, and marketing campaigns. ERP is broader — it manages all core business operations including finance, HR, procurement, and production. CRM and ERP are complementary: CRM manages the customer-facing side while ERP handles the back-office operations. Popular CRM tools include Salesforce, Zoho CRM, and HubSpot. In some companies, SAP CRM or SAP SD overlaps with CRM functionality.

---

**28. What is a Data Warehouse and how is it different from ERP?**

A Data Warehouse is a centralized repository that collects and stores historical data from multiple source systems (ERP, CRM, HR systems, etc.) and is optimized for reporting and analytics. ERP is an operational system — designed to process day-to-day transactions in real time. Querying an ERP for large historical reports can slow down operations; a data warehouse solves this by storing pre-aggregated, structured data for fast reporting. Tools like SAP BW, Snowflake, or Amazon Redshift are data warehouses used alongside ERP systems.

---

**29. What should an MIS Executive know about ERP?**

An MIS Executive does not need to be an ERP consultant, but should know: (1) Which ERP system the company uses, (2) Key modules relevant to their reporting domain (Sales, Finance, HR, Inventory), (3) How to extract data — relevant T-codes (SAP) or report exports, (4) What the key data tables or reports are for their metrics, and (5) How to identify and resolve data discrepancies between ERP and Excel reports. The ability to independently extract accurate data from ERP without always relying on the IT team is a significant differentiator for an MIS professional.

---

**30. What are common ERP-related challenges faced by MIS Executives?**

Common challenges include: (1) Access restrictions — not all users have SE16N or full report access, requiring coordination with SAP admins; (2) Data volume — large exports may time out or exceed Excel row limits (1,048,576 rows); (3) Data inconsistencies — master data errors (wrong cost center, missing material codes) causing report mismatches; (4) Format issues — SAP exports may have number formatting issues (commas, special characters) needing cleanup; and (5) Dependency on IT — for custom reports or new data access. Building a good relationship with the SAP/ERP team is essential for MIS effectiveness.

---
