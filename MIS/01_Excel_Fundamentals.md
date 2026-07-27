# Excel Fundamentals — Complete Notes
## From Zero to Confident Excel User

---

## 1. WHAT IS MICROSOFT EXCEL?

Excel is a **spreadsheet application** used to store, organize, calculate, and analyze data. It is the most widely used tool in the MIS world.

**Why Excel for MIS?**
- Handles millions of rows of business data
- Built-in formulas eliminate manual calculation errors
- Pivot Tables summarize thousands of rows in seconds
- Charts and dashboards communicate insights visually

---

## 2. EXCEL INTERFACE — KNOW EVERY PART

```
┌─────────────────────────────────────────────────────────────────┐
│ Title Bar        File  Home  Insert  Page Layout  Formulas ...  │  ← Ribbon (Tabs)
├──────────┬──────────────────────────────────────────────────────┤
│ Name Box │ Formula Bar  [=SUM(A1:A10)                         ] │
├──────────┴──────────────────────────────────────────────────────┤
│   │  A   │   B   │   C   │   D   │   E   │   F   │             │
│ 1 │      │       │       │       │       │       │  ← Row 1    │
│ 2 │      │       │       │       │       │       │             │
│...│      │       │       │       │       │       │             │
└─────────────────────────────────────────────────────────────────┘
```

| Part | What It Does |
|---|---|
| **Ribbon** | Tabs with grouped commands (Home, Insert, Formulas, Data, etc.) |
| **Name Box** | Shows the current cell address (e.g., A1). Click here to navigate to any cell. |
| **Formula Bar** | Shows the actual formula or content of the selected cell |
| **Column Headers** | Letters A, B, C... (up to XFD — 16,384 columns) |
| **Row Headers** | Numbers 1, 2, 3... (up to 1,048,576 rows) |
| **Sheet Tabs** | Navigate between worksheets |
| **Status Bar** | Shows Sum, Average, Count of selected cells at the bottom |

**Cell Address:** The intersection of a column and row. `B5` = Column B, Row 5.

**Range:** A group of cells. `A1:D10` = all cells from A1 to D10.

---

## 3. ESSENTIAL KEYBOARD SHORTCUTS (Learn These First!)

### Navigation
| Shortcut | Action |
|---|---|
| `Ctrl + Home` | Go to cell A1 |
| `Ctrl + End` | Go to last used cell |
| `Ctrl + Arrow Keys` | Jump to edge of data |
| `Ctrl + G` / `F5` | Go To (navigate to any cell/range) |
| `Ctrl + F` | Find |
| `Ctrl + H` | Find & Replace |
| `Tab` | Move right |
| `Shift + Tab` | Move left |
| `Enter` | Move down |
| `Shift + Enter` | Move up |

### Selection
| Shortcut | Action |
|---|---|
| `Ctrl + Shift + End` | Select from current cell to last used cell |
| `Ctrl + Shift + Home` | Select from current cell to A1 |
| `Ctrl + A` | Select all data / entire sheet |
| `Ctrl + Space` | Select entire column |
| `Shift + Space` | Select entire row |
| `Shift + Click` | Select range |
| `Ctrl + Click` | Select non-contiguous cells |

### Editing
| Shortcut | Action |
|---|---|
| `Ctrl + C` | Copy |
| `Ctrl + X` | Cut |
| `Ctrl + V` | Paste |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Delete` | Clear cell content |
| `F2` | Edit cell (enter edit mode) |
| `Ctrl + D` | Fill Down (copy formula from cell above) |
| `Ctrl + R` | Fill Right |
| `Ctrl + ;` | Insert today's date |
| `Ctrl + Shift + ;` | Insert current time |
| `Alt + Enter` | New line within a cell |

### Formatting
| Shortcut | Action |
|---|---|
| `Ctrl + 1` | Format Cells dialog |
| `Ctrl + B` | Bold |
| `Ctrl + I` | Italic |
| `Ctrl + U` | Underline |
| `Ctrl + Shift + $` | Currency format |
| `Ctrl + Shift + %` | Percentage format |
| `Ctrl + Shift + #` | Date format |
| `Alt + H + O + I` | Auto-fit column width |

### File Operations
| Shortcut | Action |
|---|---|
| `Ctrl + S` | Save |
| `Ctrl + W` | Close workbook |
| `Ctrl + N` | New workbook |
| `Ctrl + O` | Open workbook |
| `Ctrl + P` | Print |
| `F12` | Save As |

### Power User Shortcuts
| Shortcut | Action |
|---|---|
| `Ctrl + T` | Create Table |
| `Alt + =` | AutoSum |
| `Ctrl + Shift + L` | Toggle Filter |
| `F4` | Repeat last action / Toggle cell reference ($) |
| `Ctrl + Shift + Enter` | Enter as array formula (older Excel) |
| `Ctrl + `` ` | Toggle formula view |

---

## 4. CELL REFERENCES — CRITICAL CONCEPT

Understanding cell references is **the most important foundation** in Excel.

### Types of References

**Relative Reference (A1)**
- Changes when you copy the formula to another cell.
- When you copy `=A1+B1` from row 1 to row 2, it becomes `=A2+B2`.
- **Use when:** You want the formula to adjust to each row/column.

```
Row 1: =A1*C1  (Employee salary × tax rate)
Row 2: =A2*C2  (automatically adjusts — correct!)
Row 3: =A3*C3
```

**Absolute Reference ($A$1)**
- The `$` sign LOCKS the row and/or column. Never changes when copied.
- `$A$1` = locked completely (both column A and row 1)
- **Use when:** You're referencing a fixed value like a tax rate, bonus %, exchange rate.

```
C1 = Tax Rate (e.g., 18%)
Row 1: =A1*$C$1   → A1 × 18% 
Row 2: =A2*$C$1   → A2 × 18% (C1 stays locked!)
Row 3: =A3*$C$1
```

**Mixed Reference**
- `$A1` = Column A locked, row can change
- `A$1` = Row 1 locked, column can change
- **Use in:** Multiplication tables, cross-reference matrices.

```
Creating a multiplication table:
      B        C        D
1   =$A2*B$1  =$A2*C$1  =$A2*D$1   ← Row 1 locked for headers
2   =$A3*B$1  =$A3*C$1  =$A3*D$1   ← Column A locked for row labels
```

### F4 Toggle Trick
Press `F4` while in a formula to cycle through:
`A1` → `$A$1` → `A$1` → `$A1` → `A1`

---

## 5. BASIC FORMULAS AND FUNCTIONS

### Arithmetic Operations
```excel
= A1 + B1        Addition
= A1 - B1        Subtraction
= A1 * B1        Multiplication
= A1 / B1        Division
= A1 ^ 2         A1 to the power of 2
= MOD(A1, 3)     Remainder when A1 divided by 3
```

### SUM Functions

**SUM** — Add a range of numbers
```excel
=SUM(A1:A100)           Sum all values in A1 to A100
=SUM(A1:A10, C1:C10)    Sum two non-adjacent ranges
=SUM(A:A)               Sum entire column A
```

**SUMIF** — Sum based on one condition
```excel
=SUMIF(range, criteria, sum_range)

=SUMIF(B:B, "Delhi", C:C)
-- Sum column C where column B = "Delhi"

=SUMIF(D:D, ">5000", D:D)
-- Sum all values in D that are greater than 5000

=SUMIF(E:E, "Sales", F:F)
-- Sum F where E = "Sales"
```

**SUMIFS** — Sum based on multiple conditions
```excel
=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...)

=SUMIFS(C:C, B:B, "Delhi", A:A, "Q1")
-- Sum C where B=Delhi AND A=Q1

=SUMIFS(Sales, Region, "North", Month, "Jan", Status, "Closed")
-- Total sales in North region, January, with Closed status
```

### COUNT Functions

**COUNT** — Count numeric cells only
```excel
=COUNT(A1:A100)      Counts only numbers (skips text, blanks)
```

**COUNTA** — Count non-empty cells
```excel
=COUNTA(A1:A100)     Counts everything except blank cells
```

**COUNTBLANK** — Count empty cells
```excel
=COUNTBLANK(A1:A100)  Counts empty/blank cells only
```

**COUNTIF** — Count based on one condition
```excel
=COUNTIF(range, criteria)

=COUNTIF(B:B, "Delhi")          Count rows where B = Delhi
=COUNTIF(C:C, ">5000")          Count values greater than 5000
=COUNTIF(D:D, "Sales*")         Count cells starting with "Sales" (* = wildcard)
=COUNTIF(E:E, "")               Count blank cells
=COUNTIF(F:F, "<>"&"")          Count non-blank cells
```

**COUNTIFS** — Count based on multiple conditions
```excel
=COUNTIFS(B:B, "Delhi", C:C, ">5000")
-- Count rows where B=Delhi AND C>5000

=COUNTIFS(A:A, "Sales", B:B, "North", C:C, ">10000")
```

### AVERAGE Functions
```excel
=AVERAGE(A1:A100)              Average of range
=AVERAGEIF(B:B, "Delhi", C:C)  Average of C where B = Delhi
=AVERAGEIFS(C:C, B:B, "Delhi", D:D, "Q1")  Multiple conditions
```

### MAX and MIN
```excel
=MAX(A1:A100)           Highest value
=MIN(A1:A100)           Lowest value
=MAXIFS(C:C, B:B, "North")  Max value where condition is met (Excel 2019+)
=MINIFS(C:C, B:B, "North")  Min value where condition is met
```

### LARGE and SMALL
```excel
=LARGE(A1:A100, 1)    Largest value (1st highest)
=LARGE(A1:A100, 2)    2nd largest value
=LARGE(A1:A100, 3)    3rd largest value
=SMALL(A1:A100, 1)    Smallest value
```

---

## 6. LOGICAL FUNCTIONS

### IF Function — The Decision Maker
```excel
=IF(condition, value_if_true, value_if_false)

=IF(A1>5000, "High", "Low")
-- If A1 > 5000, show "High", else "Low"

=IF(B2="Yes", 100, 0)
-- If B2 is Yes, give 100, else 0

=IF(C3="", "Missing", C3)
-- If C3 is empty, show "Missing", else show C3's value
```

**Nested IF — Multiple conditions**
```excel
=IF(A1>=90, "Excellent",
    IF(A1>=75, "Good",
        IF(A1>=60, "Average", "Poor")))

-- Real MIS example: Performance rating
=IF(D2>=100%, "Exceeds Target",
    IF(D2>=90%, "Meets Target",
        IF(D2>=75%, "Near Target", "Below Target")))
```

### AND / OR — Combine Conditions
```excel
=AND(A1>5000, B1="Active")     → TRUE only if BOTH are true
=OR(A1="Delhi", A1="Mumbai")   → TRUE if EITHER is true

-- Used inside IF:
=IF(AND(A1>5000, B1="Active"), "Eligible", "Not Eligible")
=IF(OR(A1="Delhi", A1="Mumbai"), "Metro", "Non-Metro")
```

### IFS — Multiple Conditions (Cleaner than Nested IF)
```excel
=IFS(A1>=90, "A", A1>=75, "B", A1>=60, "C", A1<60, "D")
-- No nesting needed! Evaluates top to bottom.
```

### IFERROR — Handle Errors Gracefully
```excel
=IFERROR(VLOOKUP(A2, Sheet2!A:B, 2, 0), "Not Found")
-- If VLOOKUP gives error (#N/A, #VALUE), show "Not Found" instead

=IFERROR(A1/B1, 0)
-- If dividing by zero gives error, show 0

=IFERROR(formula, "")
-- Show blank instead of error — very common in MIS reports
```

### IFNA — Handle Only #N/A Errors
```excel
=IFNA(VLOOKUP(A2, Sheet2!A:B, 2, 0), "Not Found")
-- More specific than IFERROR — only catches #N/A
```

---

## 7. TEXT FUNCTIONS — Essential for Data Cleaning

### Joining and Splitting Text

**CONCATENATE / CONCAT / & operator**
```excel
=A1&" "&B1                      "Nihal" & " " & "Kumar" → "Nihal Kumar"
=CONCAT(A1, " ", B1)            Same result
=TEXTJOIN(", ", TRUE, A1:A5)    Join range with delimiter, skip blanks
```

**LEFT, RIGHT, MID — Extract parts of text**
```excel
=LEFT("EMPID-2024", 5)       → "EMPID"  (first 5 characters)
=RIGHT("EMPID-2024", 4)      → "2024"   (last 4 characters)
=MID("EMPID-2024", 7, 4)     → "2024"   (start at position 7, take 4 chars)

-- Real use: Extract year from "TXN-2024-001"
=MID("TXN-2024-001", 5, 4)   → "2024"
```

**LEN — Count characters**
```excel
=LEN("Hello")      → 5
=LEN(A1)           → Length of text in A1
-- Use to find rows where phone number ≠ 10 digits:
=IF(LEN(A2)<>10, "Invalid", "Valid")
```

**FIND / SEARCH — Find position of text**
```excel
=FIND("@", "nihal@gmail.com")    → 6  (position of @, case-sensitive)
=SEARCH("@", "nihal@gmail.com")  → 6  (case-insensitive)
-- Use with MID to extract domain:
=MID(A2, FIND("@", A2)+1, 100)   → "gmail.com"
```

### Cleaning Text

**TRIM — Remove extra spaces**
```excel
=TRIM("  Hello   World  ")   → "Hello World"
-- Critical for data cleaning — spaces cause VLOOKUP failures!
```

**UPPER, LOWER, PROPER — Change case**
```excel
=UPPER("nihal kumar")    → "NIHAL KUMAR"
=LOWER("NIHAL KUMAR")    → "nihal kumar"
=PROPER("nihal kumar")   → "Nihal Kumar"
```

**SUBSTITUTE — Replace text**
```excel
=SUBSTITUTE("01-Jan-2024", "-", "/")     → "01/Jan/2024"
=SUBSTITUTE(A1, " ", "_")               → Replace spaces with underscore
=SUBSTITUTE("EMPID-001", "EMPID-", "")  → "001"  (remove prefix)
```

**REPLACE — Replace by position**
```excel
=REPLACE("EMPID-001", 1, 5, "STAFF")   → "STAFF-001"
-- Replace 5 characters starting at position 1 with "STAFF"
```

**TEXT — Format numbers as text**
```excel
=TEXT(45000, "₹#,##0")           → "₹45,000"
=TEXT(TODAY(), "DD-MMM-YYYY")     → "27-Jul-2024"
=TEXT(0.18, "0%")                 → "18%"
-- Real use: When concatenating numbers with text
="Total Sales: "&TEXT(SUM(C:C), "₹#,##0")
```

**VALUE — Convert text-number to actual number**
```excel
=VALUE("45000")     → 45000 (number, not text)
-- When numbers imported from ERP as text, SUM doesn't work — use VALUE first
```

---

## 8. DATE AND TIME FUNCTIONS

### Getting Current Date/Time
```excel
=TODAY()      → Current date (updates every day automatically)
=NOW()        → Current date and time (updates every recalculation)
```

### Date Arithmetic
```excel
=TODAY() - A1             Days since date in A1
=A2 - A1                  Difference in days between two dates
=EDATE(A1, 3)             Date 3 months after A1 (for tenure, expiry)
=EOMONTH(A1, 0)           Last day of the month of A1
=EOMONTH(A1, -1)+1        First day of the month of A1
```

### Extracting Parts of a Date
```excel
=DAY("27-Jul-2024")       → 27
=MONTH("27-Jul-2024")     → 7
=YEAR("27-Jul-2024")      → 2024
=WEEKDAY(A1, 2)           → Day of week (1=Monday with type 2)
=TEXT(A1, "dddd")         → "Sunday" (full day name)
=TEXT(A1, "MMM")          → "Jul" (month abbreviation)
```

### DATEDIF — Calculate Age/Tenure (Hidden Function!)
```excel
=DATEDIF(start_date, end_date, unit)

=DATEDIF(A1, TODAY(), "Y")    → Years between dates (employee tenure)
=DATEDIF(A1, TODAY(), "M")    → Months between dates
=DATEDIF(A1, TODAY(), "D")    → Days between dates
=DATEDIF(A1, TODAY(), "YM")   → Months remaining after years subtracted

-- Full tenure string:
=DATEDIF(A2,TODAY(),"Y")&" Yrs "&DATEDIF(A2,TODAY(),"YM")&" Months"
→ "2 Yrs 3 Months"
```

### NETWORKDAYS — Count Working Days
```excel
=NETWORKDAYS(A1, A2)               Working days between A1 and A2 (excludes weekends)
=NETWORKDAYS(A1, A2, holidays)     Also exclude public holidays (list in a range)

-- Use in: TAT (Turnaround Time) calculations, SLA tracking
```

### WORKDAY — Find Date After N Working Days
```excel
=WORKDAY(A1, 30)         Date 30 working days after A1
=WORKDAY(TODAY(), 5)     Date 5 business days from today
```

---

## 9. LOOKUP FUNCTIONS — The Heart of MIS

### VLOOKUP — Most Asked in Interviews!

**Syntax:**
```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```

**Parameters:**
- `lookup_value` — What you're searching for (e.g., Employee ID)
- `table_array` — The range to search in (e.g., the master data table)
- `col_index_num` — Which column number to return data from
- `range_lookup` — `FALSE` or `0` = exact match (use this always in MIS!), `TRUE` = approximate

**Example:**
```excel
-- Master sheet: A=EmpID, B=Name, C=Department, D=Salary
-- Report sheet: A=EmpID, want to pull Name, Department, Salary

=VLOOKUP(A2, Master!A:D, 2, 0)   → Returns Name (column 2)
=VLOOKUP(A2, Master!A:D, 3, 0)   → Returns Department (column 3)
=VLOOKUP(A2, Master!A:D, 4, 0)   → Returns Salary (column 4)

-- With IFERROR to avoid #N/A errors:
=IFERROR(VLOOKUP(A2, Master!A:D, 2, 0), "Not Found")
```

**⚠️ VLOOKUP Limitations (Very Frequently Asked!):**
1. Can only look to the **right** — lookup column MUST be the leftmost column
2. Returns only the **first match** (duplicate lookup values cause issues)
3. **Breaks if you insert columns** in the middle (col_index is a hardcoded number)
4. **Slower** than INDEX/MATCH on large datasets
5. **Case-insensitive** — doesn't distinguish "DELHI" from "delhi"

### HLOOKUP — Horizontal Lookup
```excel
=HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup])
-- Same as VLOOKUP but searches across rows instead of columns
-- Rarely used compared to VLOOKUP
```

### INDEX + MATCH — The Professional's Choice

**INDEX** — Returns the value at a specific position in a range
```excel
=INDEX(range, row_number, [column_number])
=INDEX(A1:A100, 5)    → Returns the 5th value in the range
```

**MATCH** — Returns the position (row number) of a value in a range
```excel
=MATCH(lookup_value, lookup_array, [match_type])
=MATCH("Delhi", A1:A100, 0)  → Returns the row number where "Delhi" is found
-- match_type 0 = exact match (always use this!)
```

**Combined INDEX + MATCH:**
```excel
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))

-- Same as VLOOKUP example but better:
=INDEX(Master!B:B, MATCH(A2, Master!A:A, 0))   → Returns Name
=INDEX(Master!C:C, MATCH(A2, Master!A:A, 0))   → Returns Department
=INDEX(Master!D:D, MATCH(A2, Master!A:A, 0))   → Returns Salary

-- Can look LEFT (which VLOOKUP cannot!):
=INDEX(Master!A:A, MATCH(A2, Master!C:C, 0))   → Find EmpID from Department name
```

**Why INDEX/MATCH is better than VLOOKUP:**
1. ✅ Can look **left, right, up, down** (any direction)
2. ✅ **Does not break** when columns are inserted/deleted
3. ✅ **Faster** on large datasets
4. ✅ Can match on **rows and columns** simultaneously (2D lookup)
5. ✅ More flexible with dynamic arrays

### XLOOKUP — Modern Replacement (Excel 365 / 2021)
```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [not_found], [match_mode])

=XLOOKUP(A2, Master!A:A, Master!B:B, "Not Found")
-- Look for A2 in Master column A, return corresponding Master column B

-- Can return multiple columns at once!
=XLOOKUP(A2, Master!A:A, Master!B:D, "Not Found")
-- Returns Name, Department, AND Salary all at once!
```

**XLOOKUP advantages:**
- Returns multiple columns in one formula
- Built-in "not found" handling (no IFERROR needed)
- Searches from bottom by default option
- Works both horizontally and vertically

### MATCH with INDEX for Two-Way Lookup
```excel
-- Find value at the intersection of a row and column:
=INDEX(data_range, MATCH(row_header, row_labels, 0), MATCH(col_header, col_labels, 0))

-- Example: Sales data table with months as columns and regions as rows
=INDEX(B2:M10, MATCH("North", A2:A10, 0), MATCH("March", B1:M1, 0))
-- Returns North region's March sales
```

---

## 10. DATA VALIDATION — Prevent Wrong Data Entry

Data Validation forces users to enter only acceptable data — crucial for MIS data integrity.

**How to set up:**
`Data Tab → Data Validation → Settings`

### Types of Validation

**Dropdown List**
```
Allow: List
Source: Delhi,Mumbai,Bangalore,Chennai
-- Or reference a range: =$F$1:$F$10
```
Use for: Region, Department, Status fields (prevents typos)

**Number Range**
```
Allow: Whole Number
Data: between
Minimum: 0
Maximum: 100
```
Use for: Percentage fields, rating fields

**Date Range**
```
Allow: Date
Data: between
Start: =TODAY()-365
End: =TODAY()
```
Use for: Valid date ranges

**Text Length**
```
Allow: Text Length
Data: equal to
Length: 10
```
Use for: Phone numbers, PAN numbers (must be exactly 10 chars)

**Custom Formula**
```
Allow: Custom
Formula: =LEN(A1)=10    → Only allow 10-character entries
Formula: =ISNUMBER(A1)  → Only allow numeric values
```

**Input Message & Error Alert:**
- Input Message: Guidance shown when cell is selected ("Enter 10-digit phone number")
- Error Alert: Message shown when invalid data entered ("Invalid! Enter exactly 10 digits")

---

## 11. CONDITIONAL FORMATTING — Make Data Speak Visually

Conditional formatting automatically applies colors, icons, data bars based on cell values.

`Home Tab → Conditional Formatting`

### Common Use Cases

**Highlight cells above/below a threshold:**
- `Highlight Cells Rules → Greater Than → 10000 → Red Fill`
- Use case: Highlight sales reps who missed target

**Top/Bottom N values:**
- `Top/Bottom Rules → Top 10 Items → Green fill`
- Use case: Highlight top performers in a report

**Data Bars (mini bar chart in cell):**
- `Data Bars → Blue Data Bar`
- Use case: Visually show quantity/sales amounts in one glance

**Color Scales:**
- Red to Green gradient automatically applied based on value range
- Use case: Heatmap of performance across regions/months

**Icon Sets:**
- Traffic lights, arrows, stars based on value thresholds
- Use case: Status indicators — ✅ Achieved, ⚠️ Near Target, ❌ Missed

### Custom Formula-Based Rules (Advanced)
```excel
-- Highlight entire row where Status = "Pending":
Rule Type: Use a formula
Formula: =$C2="Pending"    ($C locks column, row changes dynamically)
Apply to: $A$2:$G$1000

-- Highlight row if due date is past:
Formula: =$D2<TODAY()

-- Highlight duplicates in column A:
Formula: =COUNTIF($A$2:$A2, A2)>1
```

**Manage Rules:**
`Conditional Formatting → Manage Rules` — View, edit, delete, reorder rules.

---

## 12. FILTERS AND SORTING

### AutoFilter
- `Data → Filter` (or `Ctrl + Shift + L`)
- Click dropdown arrow on column header to filter
- Filter by value, text, number, date
- Multiple column filters work as AND conditions

### Advanced Filter
- `Data → Advanced`
- Can filter to a separate location (extract unique records)
- Can use formula-based criteria

### Custom Sort
- `Data → Sort`
- Sort by multiple columns (e.g., Region → then by Sales descending)
- Sort by cell color or icon (after conditional formatting)

### Filter Tricks
```excel
-- Filter text containing specific word:
Text Filters → Contains → "Delhi"

-- Filter dates in a specific month:
Date Filters → This Month / Last Month / Custom Range

-- Filter unique values:
Copy filtered results to new sheet for unique list
```

---

## 13. PASTE SPECIAL — Underused but Powerful

`Right-click → Paste Special` or `Ctrl + Alt + V`

| Option | Use Case |
|---|---|
| **Paste Values** | Remove formulas, paste only the result (before sharing reports) |
| **Paste Formats** | Apply formatting without changing content |
| **Paste Column Width** | Match column width of source |
| **Transpose** | Convert rows to columns or vice versa |
| **Add/Subtract** | Paste and add/subtract from existing values |

**Keyboard shortcut for Paste Values:** `Alt + E + S + V + Enter`
**Quick shortcut:** `Ctrl + Shift + V` (in some versions)

---

## 14. NAMED RANGES — Cleaner Formulas

Instead of `=SUMIF($B$2:$B$1000, "Delhi", $C$2:$C$1000)`, use names:
```excel
-- Define a named range:
Select B2:B1000 → Name Box → type "Region" → Enter

-- Now use it:
=SUMIF(Region, "Delhi", Sales)    ← Much more readable!
```

`Formulas → Name Manager` — Create, edit, delete named ranges.

---

## 15. FREEZE PANES — Essential for Large Reports

- `View → Freeze Panes → Freeze Top Row` — Keep headers visible when scrolling
- `View → Freeze Panes → Freeze First Column` — Keep IDs visible when scrolling right
- `View → Freeze Panes → Freeze Panes` — Freeze both rows and columns (select the cell at the intersection point first)

**Tip:** Always freeze panes before sharing a report — non-frozen large reports are frustrating to read.

---

## 16. REMOVING DUPLICATES

`Data → Remove Duplicates`
- Select which columns to check for duplicates
- Keep the first occurrence, delete the rest

**Formula to FIND duplicates (don't delete yet):**
```excel
=COUNTIF($A$2:$A2, A2)    -- Put in helper column
-- First occurrence = 1, duplicate = 2 or more
-- Filter for >1 to see duplicates before deleting
```

---

## 17. DATA TYPES AND COMMON ERRORS

### Excel Error Messages

| Error | Meaning | Common Fix |
|---|---|---|
| `#N/A` | Lookup value not found | Wrap with IFERROR; check for spaces using TRIM |
| `#VALUE!` | Wrong data type (number expected, text given) | Check data types; use VALUE() |
| `#DIV/0!` | Dividing by zero | Wrap with IFERROR or check denominator |
| `#REF!` | Referenced cell was deleted | Recalculate references |
| `#NAME?` | Formula name misspelled | Check spelling; make sure using correct function name |
| `#NUM!` | Invalid numeric value | Check if formula produces valid number |
| `######` | Column too narrow to display | Widen the column |

---

## 18. PRINTING AND PAGE SETUP

### Before Printing a Report
1. `Page Layout → Orientation` — Landscape for wide tables
2. `Page Layout → Scale to Fit` — Fit to 1 page wide
3. `Print Area → Set Print Area` — Print only selected range
4. `View → Page Break Preview` — See where pages break
5. `Header/Footer` — Add company name, date, page numbers
6. Freeze panes don't apply to print — use `Page Layout → Print Titles` to repeat header rows on each page

---

## 19. PRACTICAL EXERCISES

**Exercise 1: Attendance Report**
Create a sheet with: EmpID, Name, Department, Days Present, Days Absent, Working Days (22), Attendance %
- Calculate Attendance % = Days Present / Working Days
- Highlight <80% in red using conditional formatting
- Add COUNTIF to count employees below 80% attendance

**Exercise 2: Sales Dashboard Raw Data**
Create: Date, Salesperson, Region, Product, Units, Price
- Calculate Total Sales = Units × Price
- SUMIF by Region
- SUMIF by Month (use MONTH() function)
- COUNTIF to count transactions per salesperson

**Exercise 3: Data Cleaning Exercise**
Given a messy dataset:
- Remove leading/trailing spaces using TRIM
- Standardize city names with PROPER
- Extract first name using LEFT(name, FIND(" ",name)-1)
- Remove duplicates
- Validate phone numbers using LEN

---

## 20. INTERVIEW QUESTIONS — EXCEL FUNDAMENTALS

**Q1. What is the difference between COUNT, COUNTA, and COUNTBLANK?**
A: COUNT = counts only numeric cells. COUNTA = counts all non-empty cells (numbers + text). COUNTBLANK = counts empty/blank cells only.

**Q2. What does Ctrl + Shift + L do?**
A: Toggles AutoFilter on/off on the selected data range.

**Q3. How do you lock a cell reference in a formula?**
A: Use the `$` sign. `$A$1` locks both row and column. Press `F4` to cycle through reference types.

**Q4. What is the difference between SUMIF and SUMIFS?**
A: SUMIF handles one condition. SUMIFS handles multiple conditions. Note: in SUMIFS, the sum_range comes first; in SUMIF it comes last.

**Q5. How do you find the second-largest value without removing the first?**
A: `=LARGE(A1:A100, 2)` returns the 2nd largest. LARGE(range, n) returns the nth largest value.

**Q6. How do you remove duplicates from a list?**
A: Data tab → Remove Duplicates → Select columns to check. Or use a helper column: `=COUNTIF($A$2:$A2, A2)` and filter for values > 1.

**Q7. What does IFERROR do?**
A: It catches any formula error and returns a specified value instead. `=IFERROR(formula, "Error Message")` — commonly used with VLOOKUP to show "Not Found" instead of #N/A.

**Q8. How do you insert today's date automatically that doesn't change?**
A: Press `Ctrl + ;` (semicolon) to insert a static date. `=TODAY()` inserts a dynamic date that updates daily.

**Q9. What is conditional formatting? Give an example.**
A: Conditional formatting automatically applies visual formatting (colors, icons, data bars) based on cell values or formulas. Example: Highlight all sales figures below target in red, or highlight the top 10 performers in green.

**Q10. What is the TRIM function used for?**
A: TRIM removes all leading and trailing spaces and reduces multiple internal spaces to one. Critical for data cleaning before VLOOKUP — spaces cause #N/A errors.

**Q11. How do you freeze the top row in Excel?**
A: View tab → Freeze Panes → Freeze Top Row. This keeps the header visible when scrolling down in a large report.

**Q12. What is Paste Special? When do you use Paste Values?**
A: Paste Special (Ctrl+Alt+V) lets you paste specific attributes only. Paste Values removes formulas and pastes only the calculated results — essential before sharing reports so recipients can't see formulas and the file doesn't break.

**Q13. What is the difference between `=TODAY()` and `=NOW()`?**
A: TODAY() returns only the current date. NOW() returns current date AND time. Both update automatically when the file recalculates.

**Q14. How do you calculate the number of working days between two dates?**
A: `=NETWORKDAYS(start_date, end_date)` excludes weekends. `=NETWORKDAYS(start_date, end_date, holidays_range)` also excludes public holidays.

**Q15. What is DATEDIF and why is it "hidden"?**
A: DATEDIF calculates the difference between two dates in specified units (Y=years, M=months, D=days). It's "hidden" because it doesn't appear in Excel's formula autocomplete — you must type it manually. Example: `=DATEDIF(A2, TODAY(), "Y")` for years of service.
