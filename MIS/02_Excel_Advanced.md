# Excel Advanced — Complete Notes
## VLOOKUP, INDEX/MATCH, Array Formulas, Dynamic Arrays, Power Formulas

---

## 1. ADVANCED VLOOKUP TECHNIQUES

### Two-Table VLOOKUP (Chain Lookup)
```excel
-- Employee data across 3 sheets: need dept name from emp ID
-- Sheet1: EmpID → DeptCode
-- Sheet2: DeptCode → DeptName

=VLOOKUP(VLOOKUP(A2, Sheet1!A:B, 2, 0), Sheet2!A:B, 2, 0)
-- First VLOOKUP gets DeptCode, second gets DeptName from that code
```

### VLOOKUP with Wildcard
```excel
=VLOOKUP("*"&A2&"*", B:C, 2, 0)
-- Finds partial match — useful when names have extra characters
-- "Nihal*" finds "Nihal Kumar", "Nihal Singh", etc.
```

### VLOOKUP Across Multiple Sheets
```excel
=IFERROR(VLOOKUP(A2, Sheet1!A:D, 2, 0),
    IFERROR(VLOOKUP(A2, Sheet2!A:D, 2, 0),
        IFERROR(VLOOKUP(A2, Sheet3!A:D, 2, 0), "Not Found")))
-- Tries Sheet1, then Sheet2, then Sheet3, then "Not Found"
```

### VLOOKUP Returning Multiple Columns (Old Method)
```excel
-- Instead of writing 3 separate VLOOKUPs:
=VLOOKUP($A2, Master!$A:$F, COLUMN(B1), 0)
-- COLUMN(B1) = 2, COLUMN(C1) = 3, etc.
-- Drag right and col_index automatically increments!
```

---

## 2. INDEX + MATCH — MASTERY

### 2D Lookup (Row and Column)
```excel
-- Find Sales for Region "North" in Month "March"
-- Data: Rows = Regions, Columns = Months

=INDEX(B2:M10,
       MATCH("North", A2:A10, 0),    ← Find row for "North"
       MATCH("March", B1:M1, 0))     ← Find column for "March"
```

### INDEX/MATCH for Left Lookup (VLOOKUP Can't!)
```excel
-- Find Employee ID from Employee Name (name in col B, ID in col A)
=INDEX(A:A, MATCH("Alice", B:B, 0))
-- VLOOKUP would fail here because ID is LEFT of Name
```

### Multiple Criteria Match (Array Version)
```excel
-- Match on both Region AND Product:
=INDEX(C:C, MATCH(1, (A:A="North")*(B:B="Laptop"), 0))
-- Enter with Ctrl+Shift+Enter in older Excel
-- In Excel 365: just Enter
```

### Dynamic Column Selection with INDEX/MATCH
```excel
=INDEX(A:Z,
       MATCH(lookup_row, A:A, 0),
       MATCH(lookup_col, 1:1, 0))
-- Find the row with MATCH for rows
-- Find the column with MATCH for columns
-- Dynamic — works even if columns are rearranged
```

---

## 3. XLOOKUP — COMPLETE GUIDE (Excel 365/2021)

```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [not_found], [match_mode], [search_mode])
```

### Basic Usage
```excel
=XLOOKUP(A2, Master!A:A, Master!B:B)
-- Equivalent to: =IFERROR(VLOOKUP(A2, Master!A:B, 2, 0), #N/A)
```

### With Not Found Handler
```excel
=XLOOKUP(A2, Master!A:A, Master!B:B, "Not Found")
-- No IFERROR needed!
```

### Return Multiple Columns at Once
```excel
=XLOOKUP(A2, Master!A:A, Master!B:D)
-- Returns Name, Department, AND Salary in 3 adjacent cells with one formula!
```

### Search Last Match (Useful for Latest Transaction)
```excel
=XLOOKUP(A2, Master!A:A, Master!B:B, "Not Found", 0, -1)
-- search_mode = -1 means search from the BOTTOM (returns last occurrence)
```

### Wildcard Match
```excel
=XLOOKUP("*"&A2&"*", Master!A:A, Master!B:B, "Not Found", 2)
-- match_mode = 2 enables wildcard matching
```

### Two-Way Lookup
```excel
=XLOOKUP(row_value, row_range, XLOOKUP(col_value, col_range, data_range))
-- Nested XLOOKUP replaces Index/Match 2D lookup
```

---

## 4. ARRAY FORMULAS — POWERFUL MULTI-CELL CALCULATIONS

### What Is an Array Formula?
An array formula performs calculations on multiple values simultaneously. In older Excel, entered with `Ctrl+Shift+Enter`. In Excel 365, just press `Enter`.

### SUMPRODUCT — The Array King (Works in All Excel Versions!)

**Basic: Multiply arrays then sum**
```excel
=SUMPRODUCT(B2:B100, C2:C100)
-- Multiplies each B×C pair, then sums all results
-- Real use: =SUMPRODUCT(Units, Price) → Total Revenue
```

**With conditions (replaces SUMIFS):**
```excel
=SUMPRODUCT((A2:A100="Delhi")*(B2:B100="Sales"), C2:C100)
-- Sum C where A="Delhi" AND B="Sales"
-- Each condition creates 1s and 0s, multiplied = AND logic

=SUMPRODUCT((A2:A100="Delhi")+(A2:A100="Mumbai"), C2:C100)
-- This is OR logic (+ instead of *)
```

**Conditional count:**
```excel
=SUMPRODUCT((A2:A100="Delhi")*1)
-- Count rows where A = "Delhi" (1 for true, 0 for false, then sum)
```

**Weighted average:**
```excel
=SUMPRODUCT(B2:B100, C2:C100) / SUM(C2:C100)
-- Revenue-weighted average price
```

### UNIQUE — Get Unique Values (Excel 365)
```excel
=UNIQUE(A2:A100)               → Unique values from column A
=UNIQUE(A2:A100, FALSE, TRUE)  → Unique values appearing exactly once
```

### SORT — Dynamic Sorted List (Excel 365)
```excel
=SORT(A2:A100)                   → Sort ascending
=SORT(A2:B100, 2, -1)            → Sort by column 2, descending
=SORT(UNIQUE(A2:A100))           → Sorted unique values
```

### FILTER — Extract Matching Rows (Excel 365)
```excel
=FILTER(A2:D100, B2:B100="Delhi")
-- Returns all rows where B = "Delhi" — like AutoFilter but dynamic!

=FILTER(A2:D100, (B2:B100="Delhi")*(C2:C100>5000), "No Results")
-- Multiple conditions: Delhi AND Sales > 5000

=FILTER(A2:D100, C2:C100=MAX(C2:C100))
-- Extract the row with maximum sales
```

### SEQUENCE — Generate Number Sequences
```excel
=SEQUENCE(10)           → 1 to 10 (vertically)
=SEQUENCE(1, 12)        → 1 to 12 (horizontally) — for month numbers
=SEQUENCE(5, 4, 1, 1)   → 5×4 matrix starting at 1, step 1
```

### COUNTIF/SUMIF with Dynamic Arrays
```excel
-- Count each unique department's employees dynamically:
=COUNTIF(B:B, UNIQUE(B2:B100))
-- Returns a count for each unique dept — spills automatically
```

---

## 5. NESTED IF AND ALTERNATIVES

### Complex Nested IF
```excel
=IF(A2>100%, "Exceeds",
    IF(A2>=90%, "Meets",
        IF(A2>=75%, "Near",
            IF(A2>=50%, "Developing", "Critical"))))
```

### IFS — Cleaner Alternative (Excel 2016+)
```excel
=IFS(A2>100%, "Exceeds",
     A2>=90%, "Meets",
     A2>=75%, "Near",
     A2>=50%, "Developing",
     TRUE, "Critical")      ← TRUE as last condition = default/else
```

### CHOOSE — Select from List by Number
```excel
=CHOOSE(MONTH(A2), "Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
-- Converts month number to name

=CHOOSE(WEEKDAY(A2,2), "Mon","Tue","Wed","Thu","Fri","Sat","Sun")
-- Converts weekday number to name
```

### SWITCH — Modern CHOOSE (Excel 2019+)
```excel
=SWITCH(A2,
    "N", "North",
    "S", "South",
    "E", "East",
    "W", "West",
    "Unknown")   ← Default value
-- Replaces complex nested IFs for exact value matching
```

---

## 6. TEXT-TO-COLUMNS AND FLASH FILL

### Text to Columns
`Data → Text to Columns`
- **Delimited:** Split by comma, space, tab, custom character
- **Fixed Width:** Split at fixed character positions
- Use case: Split "First Last" → two columns; Split "CITY-CODE-DATE" into parts

### Flash Fill (Excel 2013+)
`Ctrl + E`

Excel automatically detects the pattern from your example:
```
Column A          Column B (type first example, then Ctrl+E)
"Nihal Kumar"  →  "Kumar, Nihal"    ← Flash Fill sees the pattern!
"Priya Sharma" →  "Sharma, Priya"   ← Auto-fills the rest
"Arun Singh"   →  "Singh, Arun"
```

Use cases:
- Extract first/last name
- Reformat phone numbers: "9876543210" → "98765-43210"
- Add email prefix: "nihal" → "nihal@company.com"
- Extract year from date string

---

## 7. WHAT-IF ANALYSIS TOOLS

### Goal Seek
`Data → What-If Analysis → Goal Seek`

**Scenario:** If target profit is ₹5,00,000 and formula is =Revenue-Cost, what should Revenue be?
- Set cell: Profit cell
- To value: 500000
- By changing cell: Revenue cell
- Excel works backwards to find the answer

**Interview use case:** "What sales target achieves 20% margin?"

### Scenario Manager
`Data → What-If Analysis → Scenario Manager`

Create named scenarios (Best Case, Worst Case, Most Likely) with different input values. Excel switches between them to show impact on outputs.

### Data Table (Sensitivity Analysis)
`Data → What-If Analysis → Data Table`

- **One-variable table:** How profit changes as price varies from ₹1000 to ₹2000
- **Two-variable table:** Profit matrix for different price AND quantity combinations

---

## 8. ADVANCED FORMATTING TECHNIQUES

### Custom Number Formats
`Ctrl + 1 → Number → Custom`

```
Format Code          Result for 45000
#,##0                45,000
#,##0.00             45,000.00
₹#,##0               ₹45,000
₹#,##0;[Red](₹#,##0) → Positive in black, Negative in red with ()
0.0%                 18.0% (for 0.18)
"▲ "#,##0;"▼ "#,##0  → ▲ 45,000 for positive, ▼ 5,000 for negative
[>=1000]#,##0"K";#,##0  → Shows as 45K for large numbers

-- Dates:
DD-MMM-YYYY          27-Jul-2024
DDDD, DD MMMM YYYY   Sunday, 27 July 2024
MMM-YY               Jul-24
```

### Format Cells Shortcuts
```
Ctrl + 1          Open Format Cells dialog
Ctrl + Shift + $  Currency
Ctrl + Shift + %  Percentage
Ctrl + Shift + #  Date
Ctrl + Shift + @  Time
Ctrl + Shift + !  Number with comma separator
```

---

## 9. ADVANCED CONDITIONAL FORMATTING

### Using Formulas for Row Highlighting
```excel
-- Highlight entire row where Value > 10000:
Formula: =$C2>10000    ($ locks column C, row 2 adjusts)
Applied to: $A$2:$Z$1000

-- Highlight alternate rows (zebra striping):
Formula: =MOD(ROW(),2)=0
Applied to: $A$2:$Z$1000

-- Highlight row if date is overdue:
Formula: =$D2<TODAY()
Applied to: $A$2:$D$1000

-- Highlight if value appears more than once (duplicates):
Formula: =COUNTIF($A$2:$A2,A2)>1
Applied to: $A$2:$A$1000
```

### Traffic Light System
```excel
-- Create three rules for same range:
Rule 1: =A2>=90   → Green background   (Priority: 1)
Rule 2: =A2>=70   → Yellow background  (Priority: 2)
Rule 3: =A2<70    → Red background     (Priority: 3)

-- In Manage Rules, check "Stop If True" on Rule 1 and 2
-- So if green, don't check yellow/red
```

---

## 10. EXCEL TABLES — STRUCTURED REFERENCES

### Create a Table
`Ctrl + T` → Table has auto-expand, filtering, and structured references

### Structured References (Formulas Using Table Names)
```excel
-- After creating table named "SalesData":
=SUM(SalesData[Amount])              → Sum the Amount column
=COUNTIF(SalesData[Region], "North") → Count North in Region column
=AVERAGE(SalesData[Score])           → Average of Score column

-- In a table formula (Total Row):
=SUM([Amount])     → Sum of Amount column in same table
=[@Amount]*1.18    → This row's Amount × 1.18 (@ = current row)
```

**Advantages of Tables:**
- Formulas auto-expand when new rows are added
- Filtering built-in
- No need to update ranges in formulas
- Structured references are more readable

---

## 11. POWER FORMULAS FOR MIS REPORTS

### Running Total (Cumulative Sum)
```excel
=SUM($C$2:C2)
-- Anchor the start ($C$2), let end row adjust (C2→C3→C4)
-- Gives running/cumulative total as you drag down
```

### Month-over-Month Change
```excel
=IF(ROW()=2, "", (C2-C1)/C1)
-- Percentage change from previous month
-- IF check prevents error on first row
```

### Rank Without Ties Affecting Order
```excel
=RANK(C2, $C$2:$C$100, 0)   → Rank from highest (1=best)
=RANK(C2, $C$2:$C$100, 1)   → Rank from lowest (1=worst)

-- Unique rank (no duplicate ranks):
=SUMPRODUCT((C$2:C$100>C2)*1)+1   → Dense rank without ties
```

### Percentile and Quartile
```excel
=PERCENTILE(C2:C100, 0.9)     → 90th percentile value
=QUARTILE(C2:C100, 1)         → 25th percentile (Q1)
=QUARTILE(C2:C100, 3)         → 75th percentile (Q3)
```

### Dynamic Report Period Calculation
```excel
-- Current month's data:
=SUMIFS(Sales, Date, ">="&DATE(YEAR(TODAY()), MONTH(TODAY()), 1),
               Date, "<="&EOMONTH(TODAY(), 0))

-- Last month:
=SUMIFS(Sales, Date, ">="&DATE(YEAR(TODAY()), MONTH(TODAY())-1, 1),
               Date, "<="&EOMONTH(TODAY(), -1))

-- Year to date (YTD):
=SUMIFS(Sales, Date, ">="&DATE(YEAR(TODAY()), 1, 1),
               Date, "<="&TODAY())
```

### OFFSET — Dynamic Range Reference
```excel
=OFFSET(A1, 0, 0, COUNTA(A:A), 1)
-- Creates a range starting at A1, sized to fit actual data
-- Use in dynamic named ranges and chart source data

=SUM(OFFSET(C2, 0, 0, MATCH(TODAY(), A:A, 1), 1))
-- Sum sales up to today's date dynamically
```

### INDIRECT — Reference from Text String
```excel
=INDIRECT("Sheet1!A1")    → References cell A1 on Sheet1 dynamically
=INDIRECT(A2&"!A1")       → References cell A1 on the sheet named in A2

-- Real use: Pull data from monthly sheets (Sheet names = "Jan", "Feb"...)
=SUM(INDIRECT(A2&"!B2:B100"))
-- Where A2 contains "Jan" → Sums Jan!B2:B100
-- Change A2 to "Feb" → Automatically sums Feb!B2:B100
```

---

## 12. PROTECTING WORKBOOKS AND SHEETS

### Sheet Protection
`Review → Protect Sheet`
- Lock editing of formulas while allowing data entry in unlocked cells
- Steps: 
  1. Select cells users SHOULD edit → Format Cells → Protection → Uncheck "Locked"
  2. Then Protect Sheet (all other cells become locked)
- Use case: Protect formula cells, allow only data entry cells to be edited

### Workbook Structure Protection
`Review → Protect Workbook`
- Prevents adding/deleting/renaming sheets
- Good for final report templates

### Hide Formulas
`Format Cells → Protection → Hidden → Protect Sheet`
- Formula won't show in formula bar even though cell is locked

---

## 13. ADVANCED CHART TECHNIQUES

### Combination Charts (Dual Axis)
- Bar chart for absolute values + Line chart for % on secondary axis
- Use case: Monthly revenue (bars) + Growth % (line)
- Right-click a series → Format Data Series → Secondary Axis

### Dynamic Charts with Named Ranges + OFFSET
```excel
-- Create named range that updates as data grows:
Name: "DynamicSales"
Refers to: =OFFSET(Sheet1!$C$2, 0, 0, COUNTA(Sheet1!$C:$C)-1, 1)
-- Use this named range as chart data source
-- Chart updates automatically as new data is added
```

### Sparklines — Mini Charts in Cells
`Insert → Sparklines → Line/Column/Win-Loss`
- Tiny charts within a single cell
- Great for showing trends in a compact report row
- Show win/loss for positive/negative values

### Chart Formatting Tips
- Remove gridlines for cleaner look
- Use data labels instead of legend when possible
- Use consistent colors aligned with company brand
- Limit colors to 2-3 per chart
- Always add a chart title and axis labels

---

## 14. ADVANCED FILTERING AND DATA EXTRACTION

### Advanced Filter for Complex Criteria
`Data → Advanced Filter`

```
Criteria Range: A separate range with headers and condition rows
Action: Filter in-place OR Copy to another location

Example criteria range for "Delhi Sales > 5000":
Region    Sales
Delhi     >5000
```

### UNIQUE + FILTER Combination (Excel 365)
```excel
-- Unique list of Delhi employees earning >50000:
=UNIQUE(FILTER(A2:A100, (B2:B100="Delhi")*(C2:C100>50000)))

-- Top 5 salespeople by amount:
=INDEX(SORT(A2:B100, 2, -1), SEQUENCE(5), {1,2})
```

### Extract Unique Values for Dropdown
```excel
-- Dynamic dropdown list that updates automatically:
=SORT(UNIQUE(FILTER(Region, Region<>"")))
-- Use this as Data Validation list source
```

---

## 15. PERFORMANCE OPTIMIZATION FOR LARGE FILES

### Make Excel Faster
1. **Avoid entire column references** in VLOOKUP (`A:A` → use `A2:A10000` instead)
2. **Convert formulas to values** for static historical data
3. **Use Tables** instead of named ranges for auto-expanding
4. **Avoid volatile functions** in large sheets (TODAY(), NOW(), INDIRECT(), OFFSET() recalculate every change)
5. **Limit conditional formatting** — apply to exact used range, not entire columns
6. **Use Manual Calculation** during data entry: `Formulas → Calculation Options → Manual` (press F9 to calculate)
7. **Avoid merged cells** — they break sorting, filtering, and copy-paste

---

## 16. INTERVIEW QUESTIONS — EXCEL ADVANCED

**Q1. What is the difference between VLOOKUP and INDEX/MATCH?**
A: VLOOKUP can only look right (lookup column must be leftmost), breaks if columns are inserted, uses a fixed column number. INDEX/MATCH can look in any direction, is more flexible, and won't break with column insertions. INDEX/MATCH is also faster on large datasets.

**Q2. What is the limitation of VLOOKUP?**
A: Five key limitations: (1) Can only return data to the RIGHT of the lookup column, (2) Breaks if columns are inserted between lookup and return columns, (3) Returns only the first match — duplicates cause issues, (4) Column index is a hardcoded number — error-prone, (5) Slightly slower than INDEX/MATCH on large data.

**Q3. How do you do a two-way lookup in Excel?**
A: Using `=INDEX(data_range, MATCH(row_value, row_headers, 0), MATCH(col_value, col_headers, 0))` — the first MATCH finds the row, the second MATCH finds the column, and INDEX returns the value at their intersection.

**Q4. What is SUMPRODUCT and how does it work?**
A: SUMPRODUCT multiplies corresponding elements of arrays and returns their sum. It can also be used as a multi-criteria SUMIF by converting conditions to 1/0 arrays and multiplying them. Example: `=SUMPRODUCT((Region="North")*(Month="Jan"), Sales)` sums sales for North in January.

**Q5. What is the difference between XLOOKUP and VLOOKUP?**
A: XLOOKUP is newer and superior: it can look in any direction, returns multiple columns in one formula, has a built-in not-found handler, supports wildcard matching, and can search from the bottom for last occurrences. VLOOKUP is only available in older Excel.

**Q6. How does the FILTER function work?**
A: FILTER(array, include, [if_empty]) returns rows from the array where the include condition is TRUE. Example: `=FILTER(A2:D100, B2:B100="Delhi")` returns all rows where column B is "Delhi". It's dynamic — updates when source data changes.

**Q7. What is a volatile function? Name some.**
A: Volatile functions recalculate every time ANY cell in the workbook changes, causing slowdowns in large files. Examples: `TODAY()`, `NOW()`, `RAND()`, `RANDBETWEEN()`, `OFFSET()`, `INDIRECT()`, `INFO()`. Use them carefully in large models.

**Q8. How would you create a dynamic chart that updates automatically?**
A: Use an Excel Table as the chart data source (Tables auto-expand). Alternatively, create dynamic named ranges using OFFSET+COUNTA and use these as the chart source. In Excel 365, use FILTER/SORT/UNIQUE formulas that spill and reference their spill range.

**Q9. What is INDIRECT and when do you use it?**
A: INDIRECT converts a text string into a cell reference. Use case: When you have multiple sheets named "Jan", "Feb", etc., and want to pull data based on which month the user selects in a cell. `=SUM(INDIRECT(A1&"!B2:B100"))` — change A1 between "Jan"/"Feb" to pull from different sheets.

**Q10. What does Ctrl+Shift+Enter do?**
A: It enters a formula as an array formula in older Excel versions (pre-365). Array formulas perform calculations on multiple values simultaneously. They appear with curly braces `{}` around them. In Excel 365, most array calculations work with just Enter.

**Q11. How do you handle #N/A errors from VLOOKUP?**
A: Wrap with `IFERROR(VLOOKUP(...), "Not Found")` or use `IFNA(VLOOKUP(...), "Not Found")`. IFNA only catches #N/A specifically, while IFERROR catches all errors. Before assuming #N/A is truly a missing value, check for trailing spaces using TRIM on both lookup value and lookup range.

**Q12. What is a structured reference in an Excel Table?**
A: When data is in a Table (Ctrl+T), formulas can reference columns by name instead of cell addresses. Example: `=SUM(SalesTable[Amount])` instead of `=SUM(C2:C1000)`. Structured references auto-expand when rows are added.

**Q13. How do you find duplicate values without removing them?**
A: Use a helper column with `=COUNTIF($A$2:$A2, A2)` — drag down. Values of 1 = first occurrence, 2+ = duplicates. Filter for >1 to see only duplicates. Alternatively use Conditional Formatting → Highlight Cells Rules → Duplicate Values.

**Q14. What is Goal Seek and when would you use it?**
A: Goal Seek (Data → What-If Analysis → Goal Seek) works backwards — you set a target value for a formula cell and it finds the input needed to achieve it. Use case: "What revenue is needed to achieve 20% profit margin?" or "What units must I sell to break even?"

**Q15. Explain the OFFSET function with an example.**
A: OFFSET(reference, rows, cols, [height], [width]) returns a range that is offset from a starting cell. Example: `=SUM(OFFSET(B1, 0, 0, COUNTA(B:B), 1))` creates a dynamic range starting at B1 with height equal to the number of filled cells. Used in dynamic named ranges for auto-expanding charts.
