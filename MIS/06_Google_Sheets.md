# Google Sheets — 30 Interview Questions

> For MIS Executive interviews — asked at startups, e-commerce, and tech companies

---

## Q1. What are the key differences between Google Sheets and Microsoft Excel?

**A:** **Google Sheets** is cloud-native, browser-based, and free — it excels at real-time collaboration (multiple users editing simultaneously), automatic saving, and easy sharing via link. **Excel** is a desktop application with more advanced features — greater formula complexity, Power Query, Power Pivot, more chart types, VBA macros, and better performance with large datasets (up to ~1M rows). Sheets has a limit of 10 million cells per spreadsheet. Key Sheets advantages: IMPORTRANGE, QUERY function, ARRAYFORMULA, and built-in Google integrations (Forms, Data Studio). Key Excel advantages: Power BI integration, richer pivot tables, and offline-first reliability.

---

## Q2. What is the IMPORTRANGE function and how do you use it?

**A:** `IMPORTRANGE` pulls data from one Google Sheet into another, enabling cross-spreadsheet data sharing without copy-pasting. Syntax: `=IMPORTRANGE("spreadsheet_url", "Sheet1!A1:D100")`. The first argument is the URL of the source spreadsheet, and the second is the sheet and range to import. On first use, you must click "Allow Access" to grant permission between the two files. It is used in MIS to centralize data from multiple department Sheets into one master report, or to pull live data from operational Sheets into a dashboard Sheet without duplication.

---

## Q3. What is the QUERY function in Google Sheets?

**A:** `QUERY` allows you to run SQL-like queries directly on a range of data within Google Sheets using Google Visualization API Query Language. Syntax: `=QUERY(data_range, "SELECT A, B, C WHERE D = 'North' ORDER BY B DESC LIMIT 10", headers)`. It supports SELECT, WHERE, ORDER BY, GROUP BY, LIMIT, PIVOT, and aggregate functions (SUM, AVG, COUNT, MAX, MIN). It is one of the most powerful functions in Sheets for filtering, summarizing, and reshaping data without building pivot tables. In MIS, it is used to dynamically pull filtered subsets from a master data sheet into summary views.

---

## Q4. What is ARRAYFORMULA and why is it useful?

**A:** `ARRAYFORMULA` allows a single formula to process an entire column or range of cells at once, returning results for multiple rows without dragging the formula down. Example: `=ARRAYFORMULA(A2:A100 * B2:B100)` computes the product for every row simultaneously. It also works with functions that normally only process a single value, like: `=ARRAYFORMULA(IF(A2:A100>0, "Positive", "Negative"))`. In MIS, ARRAYFORMULA is great for applying consistent calculations to entire columns automatically — new rows added to the range are computed instantly without needing to copy formulas down.

---

## Q5. What is the GOOGLEFINANCE function?

**A:** `GOOGLEFINANCE` fetches real-time or historical financial market data directly into a Sheets cell. Syntax: `=GOOGLEFINANCE("GOOG", "price")` returns the current stock price of Google. You can fetch attributes like `"high"`, `"low"`, `"volume"`, `"pe"`, `"marketcap"`, etc. For historical data: `=GOOGLEFINANCE("GOOG", "price", "2024-01-01", "2024-12-31", "DAILY")` returns a table of daily prices. This is useful for finance and investment MIS dashboards that need live or historical market data without manual updates. It is a unique Google Sheets feature with no direct Excel equivalent.

---

## Q6. How does real-time collaboration work in Google Sheets?

**A:** Multiple users can open and edit the same Google Sheet simultaneously — each user's cursor appears in a distinct color with their name, and changes are visible to all in near real-time (within seconds). There is no need to "check out" a file or deal with conflicting saves. You share a Sheet via Share → Add email addresses or generate a shareable link with specific permission levels (Viewer, Commenter, Editor). This makes Google Sheets the preferred tool for teams working on live trackers, attendance records, or shared MIS data entry forms where simultaneous updates are required.

---

## Q7. How does Version History work in Google Sheets?

**A:** Google Sheets automatically saves every change and maintains a full version history at **File → Version History → See Version History**. You can browse all past versions (timestamped with the editor's name), preview what the sheet looked like at any point, and restore any previous version with one click. You can also name important versions (e.g., "EOD Report July 25") for easy reference. Unlike Excel's Track Changes, Sheets version history is automatic, granular, and always available without any setup. This is extremely valuable for audit trails in MIS — you can always answer "who changed this and when."

---

## Q8. How does Conditional Formatting work in Google Sheets?

**A:** Go to **Format → Conditional Formatting** to apply formatting rules based on cell values. You can use preset conditions (greater than, less than, text contains, date before/after, is empty) or write a **Custom Formula** for more complex logic (e.g., `=$C2<0` highlights the entire row where column C is negative). The color scale option applies a gradient from one color to another based on value ranges (useful for heat maps). Unlike Excel, Sheets also supports conditional formatting with ARRAYFORMULA-style custom formulas. Conditional formatting is used heavily in MIS trackers to highlight exceptions — overdue tasks, targets missed, anomalies.

---

## Q9. What are Sparklines in Google Sheets?

**A:** Sparklines are tiny, cell-embedded mini-charts that visualize a trend or data pattern within a single cell without taking up chart canvas space. Syntax: `=SPARKLINE(data_range, {"charttype","line"; "color","blue"})`. Supported chart types: `line`, `bar`, `column`, `winloss`. Example: `=SPARKLINE(B2:M2)` in a summary row shows a small line chart of 12 months of data in that cell. They are used in MIS summary tables to show individual row trends alongside data values — e.g., a row for each sales rep with their 12-month trend sparkline. A unique Google Sheets feature not available as natively in Excel.

---

## Q10. How does the FILTER function work in Google Sheets?

**A:** `FILTER` returns a subset of a range where specified conditions are true. Syntax: `=FILTER(range, condition1, [condition2], ...)`. Example: `=FILTER(A2:D100, C2:C100="North", D2:D100>1000)` returns all rows where Region is "North" AND Sales > 1000. Multiple conditions are AND logic by default; for OR logic, use `+` between conditions: `=FILTER(A2:D, (C2:C="North")+(C2:C="South"))`. Unlike Excel's FILTER (available in Excel 365), Sheets' FILTER has been available longer and is widely used. It is a dynamic array function — results automatically resize as source data changes.

---

## Q11. What does the UNIQUE function do in Google Sheets?

**A:** `UNIQUE` returns all distinct/unique rows from a given range, removing exact duplicates. Syntax: `=UNIQUE(range)`. Example: `=UNIQUE(A2:A100)` returns a list of unique values from column A. `=UNIQUE(A2:C100)` returns unique row combinations across three columns. It is a spill function — it automatically outputs as many rows as needed. In MIS, UNIQUE is used to build dynamic drop-down lists, extract unique region/category/agent lists from raw data, or validate data consistency. Combined with SORT: `=SORT(UNIQUE(A2:A))` gives a sorted unique list.

---

## Q12. How does the SORT function work in Google Sheets?

**A:** `SORT` returns the contents of a range sorted by a specified column. Syntax: `=SORT(range, sort_column_index, is_ascending, [sort_column2], [is_ascending2])`. Example: `=SORT(A2:C100, 3, FALSE)` sorts the range by the 3rd column in descending order. You can sort by multiple columns: `=SORT(A2:C, 2, TRUE, 3, FALSE)`. Unlike Excel's manual sort (which modifies original data), SORT outputs a sorted copy without touching the source. This is extremely useful in MIS dashboards to display always-sorted leaderboards (top performers, highest sales) that automatically update when source data changes.

---

## Q13. Is XLOOKUP available in Google Sheets? How does it compare to VLOOKUP there?

**A:** As of mid-2024, Google Sheets added `XLOOKUP` support, but it is still not as universally available across all Google accounts and regions as it is in Excel 365. In Sheets, `VLOOKUP` remains the most widely used lookup function. The key difference is that `VLOOKUP` requires the lookup column to be the leftmost column and references columns by number index, making it fragile when columns are inserted. Google Sheets' preferred alternative has historically been `INDEX(MATCH())` for flexible two-way lookups, or the `QUERY` function for more complex filtering. When XLOOKUP is available in Sheets, it works with the same syntax as Excel.

---

## Q14. How does Data Validation work in Google Sheets?

**A:** Data Validation is set via **Data → Data Validation** and restricts what users can enter into a cell. You can restrict input to: a list of items (dropdown), a number range, date range, text length, checkbox (TRUE/FALSE), or a custom formula. In MIS, it is used to create controlled dropdowns for Status (Open/Closed/In Progress), Region, or Category — ensuring data consistency in shared trackers. You can show a warning on invalid entry or reject it entirely. Unlike Excel, Sheets allows you to show a dropdown from a range in another sheet using `=SheetName!A1:A10` as the source, or use a named range.

---

## Q15. How do you protect a range or sheet in Google Sheets?

**A:** Go to **Data → Protect Sheets and Ranges**. You can protect either an entire sheet or a specific range of cells. Once protected, you set who has edit permission — you can restrict it to only yourself, or allow specific users. Others will see the protection warning if they try to edit. You can also show a warning (editable but with a caution prompt) instead of fully restricting. In MIS, range protection is used to lock formula cells, header rows, or lookup tables while leaving input cells open for data entry. Sheet protection is used to prevent accidental deletion or modification of report structure.

---

## Q16. What are REGEXMATCH and REGEXEXTRACT functions?

**A:** These functions use regular expressions (regex) for pattern matching in text: **`REGEXMATCH(text, pattern)`** — returns TRUE if the text matches the regex pattern. Example: `=REGEXMATCH(A2, "\d{10}")` checks if A2 contains a 10-digit number (phone validation). **`REGEXEXTRACT(text, pattern)`** — extracts the first matching substring. Example: `=REGEXEXTRACT(A2, "[A-Z]{2}-\d+")` extracts a code like "IN-1234" from a longer string. There is also `REGEXREPLACE` for substituting matched patterns. These are uniquely powerful in Sheets (Excel lacks native regex functions) and are very useful for cleaning and validating unstructured MIS data like email addresses, phone numbers, or product codes.

---

## Q17. How do you create a Pivot Table in Google Sheets?

**A:** Select your data range and go to **Insert → Pivot Table**. Choose to insert in a new or existing sheet. In the Pivot Table Editor (right panel), drag fields to Rows, Columns, Values, and Filters — similar to Excel. Values support aggregation functions (SUM, COUNT, AVERAGE, etc.) and can show "% of Grand Total" or other display options. Google Sheets pivot tables automatically update when you click on the pivot table and the source data has changed (there is a refresh button). They are slightly less feature-rich than Excel pivots (no slicers directly on pivots in older versions), but fully adequate for MIS summary reporting.

---

## Q18. How do you connect Google Sheets to Looker Studio (formerly Google Data Studio)?

**A:** In Looker Studio (lookerstudio.google.com), click **Create → Report → Add Data → Google Sheets** and authorize access. Select the specific spreadsheet and sheet/range. Looker Studio then treats the Sheets data as a live data source — any changes to the Sheet are reflected in the Looker Studio report on the next data refresh (configurable to as frequent as 15 minutes). You can build dashboards with charts, scorecards, date range filters, and share them with stakeholders via a link without them needing Sheets access. This is the Google ecosystem equivalent of Power BI's workflow.

---

## Q19. What is Google Apps Script and how is it used in Sheets?

**A:** Google Apps Script is a JavaScript-based scripting platform for automating tasks across Google Workspace (Sheets, Docs, Gmail, Drive, etc.). In Sheets, it is accessed via **Extensions → Apps Script**. Use cases include: automatically sending email reports when a cell meets a condition, creating custom menu options, building custom functions not available natively, auto-populating data from forms, and scheduling scripts to run on a trigger (daily, hourly, on form submit). For MIS, Apps Script is the equivalent of Excel's VBA — it can automate repetitive reporting tasks. No programming background is required for basic scripts, but JavaScript knowledge is helpful.

---

## Q20. What are IMPORTHTML and IMPORTXML used for?

**A:** **`IMPORTHTML(url, query, index)`** imports data from an HTML table or list on a webpage directly into Sheets. Example: `=IMPORTHTML("https://en.wikipedia.org/wiki/List_of_countries_by_population", "table", 1)` pulls the first table from that Wikipedia page into Sheets. **`IMPORTXML(url, xpath_query)`** imports specific data from XML or HTML using XPath selectors — useful for scraping specific elements from structured web pages. Both functions are live and refresh periodically. These are powerful for MIS professionals who need to pull publicly available web data (exchange rates, competitor prices, government statistics) without building a web scraper or API integration.

---

## Q21. How do Checkboxes work in Google Sheets?

**A:** Insert checkboxes via **Insert → Checkbox** — they insert a cell that toggles between TRUE (checked) and FALSE (unchecked). You can use them in formulas: `=COUNTIF(A2:A20, TRUE)` counts all checked boxes. You can also set custom values via **Data → Data Validation → Checkbox** (e.g., "Yes"/"No" instead of TRUE/FALSE). In MIS, checkboxes are used in task trackers (mark completed tasks), attendance sheets, or to create interactive toggle filters in Sheets dashboards. They add a more professional, app-like feel to shared operational trackers.

---

## Q22. What are Named Ranges in Google Sheets and why are they useful?

**A:** Named Ranges assign a custom name to a cell range (e.g., naming B2:B100 as "SalesData") via **Data → Named Ranges**. You can then use the name in formulas: `=SUM(SalesData)` instead of `=SUM(B2:B100)`. Named ranges make formulas more readable and easier to maintain — if the range changes, you update the named range definition once instead of updating every formula. They are also used as the source for data validation dropdowns across sheets. In MIS, named ranges improve formula auditability and make shared workbooks easier for non-technical team members to understand.

---

## Q23. Explain INT and ROUND functions in Google Sheets.

**A:** **`INT(number)`** truncates a number to the nearest integer toward zero — it does not round, it floors. Example: `=INT(4.9)` = 4, `=INT(-4.1)` = -5. **`ROUND(number, decimal_places)`** rounds a number to the specified number of decimal places using standard rounding rules. Example: `=ROUND(4.567, 2)` = 4.57. Related functions: `ROUNDUP` (always rounds up) and `ROUNDDOWN` (always rounds down). In MIS, ROUND is used when displaying currency or percentages with controlled decimal places, and INT is used when converting decimal quantities (like fractional hours) to whole numbers.

---

## Q24. Are SUMIF and COUNTIF available in Google Sheets?

**A:** Yes, both `SUMIF` and `COUNTIF` work in Google Sheets with the same syntax as Excel. `=SUMIF(range, criteria, sum_range)` adds values where a condition is met. `=COUNTIF(range, criteria)` counts cells meeting a condition. Their multi-criteria versions — `SUMIFS` and `COUNTIFS` — are also fully supported. Example: `=SUMIFS(D2:D100, B2:B100, "North", C2:C100, "Q1")` sums sales for North region in Q1. These are core MIS functions for building summary reports without pivot tables. Google Sheets also supports `AVERAGEIF`, `AVERAGEIFS`, and `MAXIFS`/`MINIFS`.

---

## Q25. What date functions are commonly used in Google Sheets?

**A:** Key date functions: **`TODAY()`** — returns today's date (live). **`NOW()`** — returns current date and time. **`DATEDIF(start, end, unit)`** — calculates the difference between two dates in days ("D"), months ("M"), or years ("Y"). **`DATE(year, month, day)`** — constructs a date from components. **`TEXT(date, "MMM-YYYY")`** — formats a date as text. **`EOMONTH(date, months)`** — returns the last day of a month. **`NETWORKDAYS(start, end)`** — counts working days. **`WEEKDAY(date)`** — returns the day of the week as a number. These are heavily used in MIS for aging analysis, TAT calculations, deadline tracking, and time-based reporting.

---

## Q26. How does Offline Access work in Google Sheets?

**A:** Google Sheets can work offline if you enable offline mode: go to **Settings (gear icon in Google Drive) → Offline → Turn on**. The Google Docs Offline Chrome extension is required. Once enabled, you can open, view, and edit Sheets even without internet — all changes are saved locally and automatically synced to Google Drive when you reconnect. This works only in Chrome browser or the Google Sheets mobile app. It is important to note that functions that require internet (IMPORTRANGE, IMPORTHTML, GOOGLEFINANCE) will not work offline. For MIS, this ensures reports remain accessible during connectivity issues.

---

## Q27. What are key keyboard shortcut differences between Google Sheets and Excel?

**A:** Some important differences: **Format as currency**: Excel uses `Ctrl+Shift+$`; Sheets uses `Ctrl+Shift+4`. **Insert row**: Both use `Ctrl+Shift++`. **Open Name Box**: Excel `Ctrl+G`; Sheets `Ctrl+K` opens hyperlink dialog (Name Box is the same top-left box). **Find & Replace**: Both use `Ctrl+H`. **Add comment**: Excel `Shift+F2`; Sheets `Ctrl+Alt+M`. **Fill Down**: Both use `Ctrl+D`. **Open formula bar**: Sheets uses `F2` like Excel. **Toggle absolute/relative reference**: Both use `F4`. Knowing these differences shows practical experience and prevents slow productivity when switching between tools in an MIS role.

---

## Q28. How do Google Form responses integrate with Google Sheets?

**A:** When you create a Google Form and link it to a Sheet (in Form → Responses → Link to Sheets), every form submission automatically adds a new row to a designated Google Sheet with a timestamp and all answers as columns. This live connection is immediate — no refresh needed. In MIS, this is used for data collection workflows: employee feedback, customer complaints, daily operational reports, expense submissions, or attendance — replacing email-based data collection. You can then build QUERY functions, pivot tables, and charts directly on the response sheet for instant analysis dashboards without any manual data entry.

---

## Q29. What is the IMAGE function in Google Sheets?

**A:** `IMAGE(url, [mode], [height], [width])` inserts an image from a URL directly into a cell. Example: `=IMAGE("https://example.com/logo.png", 1)` inserts the image scaled to fit the cell. Mode options: 1 (stretch to fit), 2 (original size, may overflow), 3 (stretch to exact specified dimensions), 4 (custom height/width in pixels). It is used in MIS dashboards to display product images in inventory reports, team member photos in HR trackers, or company logos in branded reports. Unlike inserting images directly (which float above cells), IMAGE-formula images are anchored to the cell and move with data sorting.

---

## Q30. What are best practices for building collaborative MIS reports in Google Sheets?

**A:** (1) **Use a Master Data sheet** (raw data only, no formulas) and separate Analysis/Report sheets that pull from it using QUERY or IMPORTRANGE — never mix data entry and analysis on the same sheet. (2) **Protect formula cells and headers** — lock all non-input cells so collaborators cannot accidentally break formulas. (3) **Use named ranges** for all key data ranges to make formulas readable and maintainable. (4) **Enable Version History naming** — name key versions (e.g., "Monthly Close July 2025") for easy rollback. (5) **Use data validation** on all input columns to enforce consistent entries. (6) **Color-code sheets** — use tab colors to indicate input (green), calculation (yellow), and output/report (blue) sheets. (7) **Document assumptions** in a dedicated "Notes" sheet or cell comments.

---

*End of File — 30 Questions Covered*
