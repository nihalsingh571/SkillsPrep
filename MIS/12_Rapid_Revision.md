# MIS Executive — Rapid Revision Cheat Sheet

> Read this the night before your interview. Everything critical in one page.

---

## 1. TOP 30 EXCEL FORMULAS — Syntax & Purpose

| # | Formula | Syntax | One-Line Purpose |
|---|---------|--------|-----------------|
| 1 | **SUM** | `=SUM(range)` | Adds all numbers in a range |
| 2 | **SUMIF** | `=SUMIF(range, criteria, sum_range)` | Sums values that meet one condition |
| 3 | **SUMIFS** | `=SUMIFS(sum_range, range1, crit1, range2, crit2)` | Sums values meeting multiple conditions |
| 4 | **COUNT** | `=COUNT(range)` | Counts cells containing numbers only |
| 5 | **COUNTA** | `=COUNTA(range)` | Counts all non-empty cells (any type) |
| 6 | **COUNTIF** | `=COUNTIF(range, criteria)` | Counts cells meeting one condition |
| 7 | **COUNTIFS** | `=COUNTIFS(range1, crit1, range2, crit2)` | Counts cells meeting multiple conditions |
| 8 | **AVERAGE** | `=AVERAGE(range)` | Returns the arithmetic mean of a range |
| 9 | **AVERAGEIF** | `=AVERAGEIF(range, criteria, avg_range)` | Averages values that meet one condition |
| 10 | **IF** | `=IF(logical_test, value_if_true, value_if_false)` | Returns one value if true, another if false |
| 11 | **IFERROR** | `=IFERROR(value, value_if_error)` | Replaces error with a custom value |
| 12 | **VLOOKUP** | `=VLOOKUP(lookup_val, table_array, col_index, 0)` | Looks up a value in the first column of a table |
| 13 | **XLOOKUP** | `=XLOOKUP(lookup_val, lookup_array, return_array)` | Modern VLOOKUP — searches any column, returns any column |
| 14 | **INDEX** | `=INDEX(array, row_num, col_num)` | Returns a value at a specific row/col in a range |
| 15 | **MATCH** | `=MATCH(lookup_val, lookup_array, 0)` | Returns the position of a value in a range |
| 16 | **LEFT** | `=LEFT(text, num_chars)` | Extracts characters from the left of a string |
| 17 | **RIGHT** | `=RIGHT(text, num_chars)` | Extracts characters from the right of a string |
| 18 | **MID** | `=MID(text, start_num, num_chars)` | Extracts characters from the middle of a string |
| 19 | **TRIM** | `=TRIM(text)` | Removes extra spaces from text (keeps single spaces between words) |
| 20 | **CONCATENATE** | `=CONCATENATE(text1, text2)` or `=text1&" "&text2` | Joins two or more text strings into one |
| 21 | **TEXT** | `=TEXT(value, format_text)` | Converts a number to text with specified formatting |
| 22 | **TODAY** | `=TODAY()` | Returns today's date (dynamic, updates daily) |
| 23 | **DATEDIF** | `=DATEDIF(start_date, end_date, "unit")` | Calculates difference between two dates in days/months/years |
| 24 | **NETWORKDAYS** | `=NETWORKDAYS(start_date, end_date, [holidays])` | Counts working days between two dates (excludes weekends) |
| 25 | **LARGE** | `=LARGE(array, k)` | Returns the k-th largest value in a range |
| 26 | **SMALL** | `=SMALL(array, k)` | Returns the k-th smallest value in a range |
| 27 | **RANK** | `=RANK(number, ref, [order])` | Returns the rank of a number in a list |
| 28 | **SUMPRODUCT** | `=SUMPRODUCT(array1, array2)` | Multiplies arrays element-by-element and sums results |
| 29 | **FILTER** | `=FILTER(array, include, [if_empty])` | Returns rows that meet a condition (dynamic array) |
| 30 | **UNIQUE** | `=UNIQUE(array)` | Returns a list of unique values from a range (dynamic array) |

> **Key DATEDIF units:** `"D"` = Days, `"M"` = Months, `"Y"` = Years

---

## 2. TOP 20 KEYBOARD SHORTCUTS

| # | Shortcut | Action |
|---|----------|--------|
| 1 | `Ctrl + C / Ctrl + V` | Copy / Paste |
| 2 | `Ctrl + Z / Ctrl + Y` | Undo / Redo |
| 3 | `Ctrl + S` | Save file |
| 4 | `Ctrl + Home / Ctrl + End` | Go to first / last cell with data |
| 5 | `Ctrl + Shift + End` | Select from active cell to last used cell |
| 6 | `Ctrl + Arrow Keys` | Jump to end of data in any direction |
| 7 | `Ctrl + Shift + Arrow` | Select entire row/column block of data |
| 8 | `Ctrl + T` | Create Table from selection |
| 9 | `Alt + =` | Auto-Sum selected range |
| 10 | `F2` | Edit active cell (enter edit mode) |
| 11 | `F4` | Toggle absolute/relative cell reference ($) |
| 12 | `Ctrl + 1` | Open Format Cells dialog |
| 13 | `Ctrl + ;` | Insert today's date (static) |
| 14 | `Ctrl + Shift + L` | Toggle AutoFilter on/off |
| 15 | `Alt + D + F + F` | Apply Filter (older shortcut) |
| 16 | `Ctrl + D` | Fill Down (copy top cell to selected cells below) |
| 17 | `Ctrl + R` | Fill Right (copy left cell to selected cells) |
| 18 | `Ctrl + F / Ctrl + H` | Find / Find & Replace |
| 19 | `Alt + F11` | Open VBA Editor |
| 20 | `Ctrl + Shift + "+"` | Insert row or column |

---

## 3. VLOOKUP vs INDEX/MATCH vs XLOOKUP

| Feature | VLOOKUP | INDEX/MATCH | XLOOKUP |
|---------|---------|-------------|---------|
| **Direction** | Left-to-right only | Any direction | Any direction |
| **Lookup column** | Must be leftmost | Lookup can be any column | Lookup can be any column |
| **Return column** | Fixed column number | Flexible, auto-adjusts | Return any column/row |
| **Column insertion safe?** | ❌ No — breaks if column inserted | ✅ Yes — formula adjusts | ✅ Yes |
| **Error handling** | Need IFERROR wrapper | Need IFERROR wrapper | Built-in (if_not_found argument) |
| **Approximate match** | ✅ Supported | ✅ Supported | ✅ Supported |
| **Multiple criteria** | ❌ Not directly | ✅ Yes (with array logic) | ✅ Yes |
| **Availability** | All versions | All versions | Excel 2019+ / Microsoft 365 |
| **Speed (large data)** | Slower | Faster | Fastest |
| **When to use** | Quick lookups on static tables | Flexible lookups, older Excel | Best overall — use whenever available |

**Quick syntax reminders:**
```
VLOOKUP:     =VLOOKUP(A2, Sheet2!$A:$C, 2, 0)
INDEX/MATCH: =INDEX(Sheet2!$B:$B, MATCH(A2, Sheet2!$A:$A, 0))
XLOOKUP:     =XLOOKUP(A2, Sheet2!$A:$A, Sheet2!$B:$B, "Not Found")
```

---

## 4. PIVOT TABLE QUICK REFERENCE

### The 4 Areas:
| Area | What Goes Here | Example |
|------|---------------|---------|
| **Rows** | Categories to group by | Region, Department, Month |
| **Columns** | Cross-tabulation categories | Quarter, Product Category |
| **Values** | Numbers to calculate | Sales Amount, Count of ID |
| **Filters** | Report-level filter (dropdown) | Year, Status |

### Key Options to Know:
- **Value Field Settings:** Change Sum → Count, Average, Max, Min, % of Total
- **Show Values As:** % of Grand Total, % of Row, Running Total, Rank
- **Group Dates:** Right-click a date field → Group → by Month/Quarter/Year
- **Calculated Field:** Insert → Calculated Field (create custom formulas inside pivot)
- **Slicer:** PivotTable Analyze → Insert Slicer (visual filter button)
- **Timeline:** Insert → Timeline (date-based visual filter)

### Refresh Steps:
1. Right-click anywhere in the Pivot Table
2. Click **"Refresh"** — OR — PivotTable Analyze → Refresh → Refresh All
3. If new rows were added outside the original range: **Change Data Source** first

> ⚠️ **Pivot Tables don't auto-update.** Always refresh after data changes.

---

## 5. POWER BI QUICK REFERENCE

### Desktop vs Service:

| Feature | Power BI Desktop | Power BI Service (Web) |
|---------|-----------------|----------------------|
| **What it is** | Windows app for building reports | Cloud platform for sharing & collaboration |
| **Data connection** | Yes — direct, gateway, file | Via published datasets |
| **Report creation** | Full editing capabilities | Limited editing |
| **Sharing** | Publish to Service | Share dashboards, workspaces |
| **Scheduling refresh** | Not here | Yes — schedule up to 8x/day (free), 48x/day (Premium) |
| **Use it for** | Building & developing | Publishing & consuming |

### What is DAX?
**DAX (Data Analysis Expressions)** is the formula language used in Power BI, Power Pivot, and Analysis Services to create calculated columns, measures, and tables.

### 10 Key DAX Functions:

| # | Function | Syntax | Purpose |
|---|----------|--------|---------|
| 1 | **SUM** | `SUM(Table[Column])` | Sums a column |
| 2 | **CALCULATE** | `CALCULATE(expression, filter1, filter2)` | Evaluates expression in a modified filter context — most powerful DAX function |
| 3 | **FILTER** | `FILTER(Table, condition)` | Returns a filtered table |
| 4 | **ALL** | `ALL(Table or Column)` | Removes filters — used inside CALCULATE |
| 5 | **DIVIDE** | `DIVIDE(numerator, denominator, [alternate])` | Safe division (handles divide-by-zero) |
| 6 | **IF** | `IF(logical_test, result_true, result_false)` | Conditional logic |
| 7 | **RELATED** | `RELATED(Table[Column])` | Fetches value from related table (like VLOOKUP between tables) |
| 8 | **COUNTROWS** | `COUNTROWS(Table)` | Counts rows in a table or filtered table |
| 9 | **DISTINCTCOUNT** | `DISTINCTCOUNT(Table[Column])` | Counts unique values in a column |
| 10 | **DATEADD** | `DATEADD(Dates[Date], -1, MONTH)` | Time intelligence — shifts dates back/forward |

**Most important measure pattern:**
```dax
Sales LY = CALCULATE([Total Sales], DATEADD(Dates[Date], -1, YEAR))
```

---

## 6. POWER QUERY QUICK REFERENCE

**What Power Query does:** Power Query is Excel/Power BI's ETL (Extract, Transform, Load) tool. It connects to data sources, cleans and reshapes data, and loads it ready for analysis — without changing the original source.

**Access it:** Data tab → Get Data / From Table/Range → Power Query Editor

### 10 Key Transformation Steps:

| # | Step | What It Does |
|---|------|-------------|
| 1 | **Remove Duplicates** | Eliminates duplicate rows based on selected columns |
| 2 | **Remove Blank Rows** | Deletes rows where all selected columns are null |
| 3 | **Split Column** | Splits one column into multiple by delimiter or character count |
| 4 | **Merge Columns** | Combines two columns into one with a separator |
| 5 | **Trim / Clean** | Removes leading/trailing spaces and non-printable characters |
| 6 | **Change Data Type** | Converts columns to Text, Number, Date, etc. |
| 7 | **Filter Rows** | Keeps only rows matching a condition |
| 8 | **Pivot / Unpivot** | Reshapes data from wide to tall format or vice versa |
| 9 | **Merge Queries** | Joins two tables (like VLOOKUP but more powerful) |
| 10 | **Append Queries** | Stacks two tables on top of each other (like combining sheets) |

> **Key advantage:** All steps are recorded and auto-apply when you refresh — making it a one-time setup for recurring data cleaning.

---

## 7. KEY BUSINESS FORMULAS

| Metric | Formula | Notes |
|--------|---------|-------|
| **Attrition Rate** | `(Employees Left ÷ Avg. Headcount) × 100` | Monthly or Annual. Avg HC = (Opening + Closing) ÷ 2 |
| **SLA Compliance %** | `(Tickets Resolved within SLA ÷ Total Tickets) × 100` | Higher = better |
| **NPS (Net Promoter Score)** | `% Promoters − % Detractors` | Promoters = 9-10, Passives = 7-8, Detractors = 0-6 |
| **CAC (Customer Acquisition Cost)** | `Total Sales & Marketing Spend ÷ New Customers Acquired` | Lower = more efficient |
| **CSAT (Customer Satisfaction)** | `(Satisfied Responses ÷ Total Responses) × 100` | Usually based on 4-5 star ratings |
| **MoM Growth %** | `((This Month − Last Month) ÷ Last Month) × 100` | Month-over-Month comparison |
| **YoY Growth %** | `((This Year − Last Year) ÷ Last Year) × 100` | Year-over-Year comparison |
| **Gross Margin %** | `((Revenue − COGS) ÷ Revenue) × 100` | COGS = Cost of Goods Sold |
| **Conversion Rate** | `(Conversions ÷ Total Visitors/Leads) × 100` | Sales funnel efficiency |
| **AHT (Average Handle Time)** | `(Talk Time + Hold Time + After-Call Work) ÷ Total Calls` | Call center KPI — lower is better |

---

## 8. COMMON INTERVIEW TRAPS TO AVOID

| # | Trap | What Goes Wrong | What to Do Instead |
|---|------|----------------|-------------------|
| 1 | **"I know everything"** | Claiming mastery in tools you've only touched | Say: "I'm proficient in X and still learning Y" |
| 2 | **Confusing VLOOKUP column index** | Saying col_index counts from the sheet start | The index counts from the table_array, not column A |
| 3 | **Saying Pivot Tables update automatically** | This is FALSE — they require manual refresh | Always mention "you need to refresh the pivot" |
| 4 | **No STAR structure on behavioral questions** | Rambling without a clear outcome | Use: Situation → Task → Action → Result |
| 5 | **Badmouthing previous employers/college** | Makes you look unprofessional | Keep it positive — say "I'm looking for new challenges" |
| 6 | **Saying "I don't have any weaknesses"** | Sounds dishonest or arrogant | Give a real, minor weakness with your improvement plan |
| 7 | **No questions at end of interview** | Signals low interest | Always prepare 3 smart questions |
| 8 | **Confusing COUNTIF and COUNTA** | COUNTA counts non-empty cells; COUNTIF counts by condition | Practice both with examples |
| 9 | **Saying XLOOKUP is same as VLOOKUP** | XLOOKUP is significantly more powerful and flexible | Know the key differences: any direction, built-in error handling, no column number needed |
| 10 | **Overpromising on salary or role** | Setting unrealistic expectations | Be honest about your level and show eagerness to learn |

---

## 9. 30-SECOND ANSWERS — 10 Most Asked Questions

| Question | Power Answer (30 seconds) |
|----------|--------------------------|
| **Tell me about yourself** | "I'm a [Degree] graduate with strong Excel and Power BI skills. I've built reports and dashboards in projects. I'm detail-oriented, fast learner, and excited to start my MIS career here." |
| **Why MIS?** | "I love working with data and making it meaningful. MIS lets me combine analytical thinking with real business impact — that's exactly the kind of work I want to do." |
| **Your biggest strength?** | "Attention to detail. I don't just submit numbers — I validate them. I caught a 15% formula error in a college project before it was shared with stakeholders." |
| **Your weakness?** | "I tend to over-check my work. I'm fixing this with structured validation checklists so I review fast and accurately, not slowly." |
| **Why this company?** | "Your reputation for [X], your data-driven culture, and this role's scope to work on live business reporting — all of this matches exactly where I want to grow." |
| **Where in 3 years?** | "Senior MIS Analyst — mastering SQL, Power BI, and owning the reporting strategy. This role is the foundation I want to build that on." |
| **Salary expectation?** | "I'm flexible and aligned with your fresher standard. My priority is the learning opportunity and growth this role offers." |
| **How do you handle errors?** | "Own it immediately. Identify what went wrong, correct it, notify stakeholders with the fixed version, and add a step to my process to prevent recurrence." |
| **How do you ensure accuracy?** | "Four-step process: check source data, audit formulas, compare to prior period, and do a final fresh-eyes review before submitting." |
| **Do you know Power BI?** | "Yes — I've self-studied Power BI. I can connect data sources, build relationships, create basic DAX measures, and design interactive dashboards." |

---

## 10. ON THE DAY OF INTERVIEW — CHECKLIST

### 📋 Night Before:
- [ ] Re-read your resume — know every line cold
- [ ] Prepare your "Tell me about yourself" answer and practice aloud
- [ ] Research the company: website, LinkedIn, recent news
- [ ] Prepare 3–5 questions to ask the interviewer
- [ ] Lay out your clothes, documents, and bag
- [ ] Sleep by 11 PM

### 📁 What to Carry:
- [ ] 2–3 printed copies of your updated resume
- [ ] College marksheets / degree / certificates (originals + photocopies)
- [ ] Government ID proof (Aadhaar/PAN)
- [ ] Passport-size photographs (at least 2)
- [ ] Pen and small notepad
- [ ] Any project work / portfolio printout (optional but impressive)

### ⏰ Morning Of:
- [ ] Wake up 90 minutes before you need to leave
- [ ] Eat a proper breakfast (low energy = poor performance)
- [ ] Arrive 10–15 minutes early (not 30 — you'll just stress)
- [ ] Silence your phone before entering

### 🗣️ During the Interview:
- [ ] Greet warmly, firm handshake, smile
- [ ] Listen to the full question before answering
- [ ] Pause 2–3 seconds before answering complex questions (it's okay)
- [ ] Use STAR format for behavioral questions
- [ ] If you don't know something: "I haven't worked with that yet, but I'm keen to learn"
- [ ] Never interrupt the interviewer
- [ ] Ask your 2–3 smart questions at the end

### 🎯 What to Say When Asked Anything You Don't Know:
> *"I haven't encountered that specific scenario yet, but based on my understanding, I would approach it by [logical answer]. I'd also make sure to ask my team lead for guidance and learn from the experience."*

### ✅ After the Interview:
- [ ] Send a thank-you email within 24 hours (optional but professional)
- [ ] Note down questions you struggled with — prepare better answers for next time

---

> **Remember:** Interviewers are not trying to trick you. They want to find someone reliable, eager to learn, and honest. Be that person.
>
> **You've prepared. You're ready. Go get it. 💪**
