# Macros & VBA Basics — 30 Interview Questions

> For MIS Executive interviews — automation knowledge separates strong candidates

---

**1. What is a Macro in Excel?**

A Macro is a recorded sequence of actions in Excel that can be replayed automatically to perform repetitive tasks. Instead of manually formatting a report, applying filters, or copying data every day, you record the steps once and run the macro to do it instantly. Macros are stored in the workbook or a Personal Macro Workbook and run with a single click or keyboard shortcut. They are the first step toward Excel automation.

---

**2. What is VBA?**

VBA (Visual Basic for Applications) is the programming language behind Excel macros. While the macro recorder captures your mouse clicks and converts them to VBA code, you can also write VBA code directly to create logic, loops, conditions, and automation that the recorder cannot capture. VBA runs inside the Excel environment and can control workbooks, worksheets, cells, charts, and even other Office applications. It is the primary automation tool for MIS professionals who work in Excel-heavy environments.

---

**3. What is the difference between recording a Macro and writing VBA?**

Recording a macro captures your actions step by step and converts them to VBA code — it is fast but limited (cannot add logic, loops, or conditions). Writing VBA manually allows you to build sophisticated automation — loops through hundreds of rows, dynamic decisions based on cell values, and error handling. A good MIS professional uses the recorder to get the basic code structure, then edits the VBA to make it dynamic and robust.

---

**4. How do you record a Macro in Excel?**

To record a macro: (1) Go to the Developer tab (or View > Macros > Record Macro), (2) Click "Record Macro," (3) Give it a name, assign a shortcut key if needed, and choose where to store it, (4) Perform the steps you want to automate (formatting, copying, filtering, etc.), (5) Click "Stop Recording" when done. The recorded steps are now saved as VBA code that can be replayed anytime. Enable the Developer tab via File > Options > Customize Ribbon.

---

**5. How do you run a Macro?**

A macro can be run in several ways: (1) Press the assigned keyboard shortcut (e.g., Ctrl+Shift+R), (2) Go to Developer > Macros, select the macro name, click Run, (3) Click a button on the worksheet that has been assigned to the macro, or (4) Run it from the VBA Editor by pressing F5 with the cursor inside the Sub. Macros assigned to buttons on dashboards are common in MIS — they allow non-technical users to trigger automation.

---

**6. Where are macros stored in Excel?**

Macros can be stored in three locations: (1) This Workbook — macro is available only when that specific file is open, (2) New Workbook — stored in a newly created workbook, (3) Personal Macro Workbook (PERSONAL.XLSB) — stored in a hidden workbook that opens automatically with Excel, making the macro available in all files. For MIS utilities that you want to use across multiple reports, store them in the Personal Macro Workbook.

---

**7. What is a .xlsm file?**

A .xlsm file is an Excel Macro-Enabled Workbook — it is the file format required to save an Excel file that contains VBA macros. If you save a macro-containing workbook as .xlsx (the default format), Excel will strip out all the VBA code. Always save workbooks with macros as .xlsm. When opening a .xlsm file, Excel shows a security warning asking you to enable macros — this is a safety measure.

---

**8. What is the VBA Editor and how do you open it?**

The VBA Editor (also called the IDE — Integrated Development Environment) is the interface where you write, edit, and debug VBA code. Open it by pressing Alt+F11, or via Developer > Visual Basic. Inside the editor, you can see the Project Explorer (lists all open workbooks and sheets), Properties window, and the main code area where you write your Subs and Functions. The Immediate Window (Ctrl+G) is useful for testing quick commands.

---

**9. What is the difference between a Sub and a Function in VBA?**

A Sub (Subroutine) is a block of VBA code that performs actions but does not return a value. Macros are Subs. A Function is a block of VBA code that performs a calculation and returns a value — similar to Excel's built-in functions like SUM or VLOOKUP. Example: `Function TaxCalc(amount As Double) As Double` returns a calculated tax value. Functions can be called from other code or used directly in Excel cells as custom formulas.

---

**10. What is a Module in VBA?**

A Module is a container inside the VBA Editor where you write your VBA code. It is like a text file that holds one or more Sub and Function procedures. You can insert a new Module via Insert > Module in the VBA Editor. Standard modules are the most common — sheet-specific modules (like Sheet1 code) are used for event-driven code (e.g., running code when a cell is changed). Organizing code into logical modules keeps large VBA projects manageable.

---

**11. What is the basic VBA syntax for a macro?**

The basic structure of a VBA macro is:
```vba
Sub MacroName()
    ' Your code goes here
    MsgBox "Hello, MIS!"
End Sub
```
Every macro starts with `Sub` followed by the name and parentheses, and ends with `End Sub`. Lines beginning with an apostrophe (`'`) are comments — ignored by Excel but useful for documentation. Variable declarations, logic, and actions are placed between `Sub` and `End Sub`.

---

**12. How do you declare variables in VBA?**

Variables in VBA are declared using the `Dim` keyword, followed by the variable name and data type. Common data types: `Integer` (whole numbers), `Long` (large integers), `Double` (decimal numbers), `String` (text), `Boolean` (True/False), `Date` (date values), `Variant` (any type). Example:
```vba
Dim empName As String
Dim salary As Double
Dim isActive As Boolean
```
Using `Option Explicit` at the top of the module forces all variables to be declared, reducing errors.

---

**13. What is a Range object in VBA?**

The Range object refers to a cell or group of cells in a worksheet. You can reference a range using `Range("A1")` for a single cell, `Range("A1:C10")` for a block, or `Cells(row, col)` using row and column numbers. Example: `Range("A1").Value = "Report Date"` writes text into cell A1. `Cells(1, 1)` also refers to A1 using row 1, column 1. The Range object is central to almost all VBA automation in Excel.

---

**14. How do you loop through rows in VBA?**

A `For...Next` loop is used to iterate through a fixed number of rows. Example:
```vba
Dim i As Integer
For i = 1 To 100
    If Cells(i, 1).Value = "" Then Exit For
    Cells(i, 2).Value = Cells(i, 1).Value * 1.1
Next i
```
This loop goes from row 1 to 100, multiplying column A values by 1.1 and writing results to column B. Using `Exit For` stops the loop when a blank row is found — useful when data length is unknown.

---

**15. What is a For Each loop for cells in VBA?**

A `For Each` loop iterates through each cell in a defined range without needing to know the exact count. Example:
```vba
Dim cell As Range
For Each cell In Range("A1:A50")
    If cell.Value > 100 Then
        cell.Interior.Color = RGB(255, 0, 0) ' Highlight red
    End If
Next cell
```
This is cleaner and more readable than a counter-based loop when working with a specific range. It is commonly used for conditional formatting, data cleaning, and validation tasks.

---

**16. How does an If-Then-Else statement work in VBA?**

If-Then-Else allows VBA to make decisions based on conditions. Example:
```vba
If Range("B2").Value >= 90 Then
    Range("C2").Value = "Excellent"
ElseIf Range("B2").Value >= 75 Then
    Range("C2").Value = "Good"
Else
    Range("C2").Value = "Needs Improvement"
End If
```
Conditions can check cell values, variable values, or any logical expression. Multiple `ElseIf` branches handle multiple scenarios. This is the core decision-making construct in VBA.

---

**17. How do you copy and paste with VBA?**

To copy a range and paste it elsewhere using VBA:
```vba
Range("A1:D100").Copy Destination:=Range("F1")
```
For paste-values-only (to avoid copying formulas):
```vba
Range("A1:D100").Copy
Range("F1").PasteSpecial Paste:=xlPasteValues
Application.CutCopyMode = False ' Clears the clipboard marquee
```
Paste-values is critical in MIS automation to avoid circular references and ensure the pasted data is static, not formula-dependent.

---

**18. How do you clear a range in VBA?**

To clear data from a range, you have several options:
```vba
Range("A1:D100").ClearContents  ' Clears values only, keeps formatting
Range("A1:D100").ClearFormats   ' Clears formatting only, keeps values
Range("A1:D100").Clear          ' Clears everything (values + formatting)
```
In MIS automation, `ClearContents` is most commonly used to reset a report template before repopulating it with fresh data, without destroying the headers or formatting.

---

**19. How do you auto-fit columns with VBA?**

Auto-fitting columns adjusts column widths to fit the widest content automatically. Example:
```vba
Columns("A:F").AutoFit
```
To auto-fit all used columns in the active sheet:
```vba
Cells.EntireColumn.AutoFit
```
This is a common finishing step in MIS report macros — after populating data, auto-fitting ensures the report looks clean and professional without manual column resizing.

---

**20. How do you use MsgBox in VBA?**

MsgBox displays a pop-up message to the user during macro execution. Example:
```vba
MsgBox "Report has been generated successfully!"
```
MsgBox can also ask a question and return a response:
```vba
Dim response As Integer
response = MsgBox("Do you want to continue?", vbYesNo, "Confirm")
If response = vbYes Then MsgBox "Proceeding..."
```
MsgBox is useful for confirming that a macro completed, warning users about overwriting data, or guiding them through a multi-step process.

---

**21. How do you use InputBox in VBA?**

InputBox prompts the user to type in a value that the macro then uses. Example:
```vba
Dim reportMonth As String
reportMonth = InputBox("Enter the Report Month (e.g., July 2025):")
Range("A1").Value = "MIS Report — " & reportMonth
```
InputBox makes macros dynamic — the same macro can generate reports for different months, teams, or scenarios based on user input. Always validate the input (check if it is blank) before using it in logic.

---

**22. What are Workbooks.Open and Workbooks.Close in VBA?**

`Workbooks.Open` opens an Excel file from a specified path; `Workbooks.Close` closes it. Example:
```vba
Dim wb As Workbook
Set wb = Workbooks.Open("C:\Reports\Sales_Data.xlsx")
' Process the data here
wb.Close SaveChanges:=False
```
This is used in MIS automation to open source data files, extract or copy data, and then close them — enabling fully automated multi-file reporting without manual file opening.

---

**23. What is Worksheet.Activate in VBA?**

`Worksheet.Activate` makes a specific sheet the active (visible) sheet. Example:
```vba
Sheets("Summary").Activate
' Or by index:
Sheets(1).Activate
```
However, best practice is to avoid using Activate where possible — instead, reference sheets directly: `Sheets("Summary").Range("A1").Value = "Total"`. Excessive use of Activate slows down macros and makes the code harder to maintain. Direct references are faster and more reliable.

---

**24. What does Application.ScreenUpdating = False do?**

Setting `Application.ScreenUpdating = False` prevents Excel from redrawing the screen while a macro runs, which significantly speeds up execution — especially for macros that loop through many rows or switch between sheets. Always re-enable it at the end of the macro:
```vba
Application.ScreenUpdating = False
' ... all your macro code ...
Application.ScreenUpdating = True
```
Without this, the screen flickers rapidly as the macro works, which is distracting and slower. This is a standard best practice for any production VBA macro.

---

**25. How do you save a file with VBA?**

To save the active workbook:
```vba
ActiveWorkbook.Save
```
To save a copy with a new name (Save As):
```vba
ActiveWorkbook.SaveAs Filename:="C:\Reports\MIS_July2025.xlsx"
```
To save as PDF:
```vba
ActiveSheet.ExportAsFixedFormat Type:=xlTypePDF, Filename:="C:\Reports\Report.pdf"
```
Automatic saving after report generation ensures no data is lost and the file is ready for distribution without manual intervention.

---

**26. How do you loop through all sheets in a workbook?**

Use a For Each loop on the `Worksheets` collection:
```vba
Dim ws As Worksheet
For Each ws In ThisWorkbook.Worksheets
    ws.Range("A1").Value = "Updated"  ' Apply action to every sheet
Next ws
```
This is useful for applying uniform formatting across all sheets, protecting all sheets at once, or collecting summary data from multiple department sheets into a master sheet. It is a very common pattern in MIS consolidation macros.

---

**27. How do you protect a sheet with VBA?**

To protect a sheet (lock it from editing):
```vba
Sheets("Dashboard").Protect Password:="MIS123"
```
To unprotect:
```vba
Sheets("Dashboard").Unprotect Password:="MIS123"
```
In MIS templates, protecting sheets prevents accidental editing of formulas by end users. You can also allow specific actions (like selecting cells) while keeping formulas locked using the `UserInterfaceOnly` or specific permission parameters in the Protect method.

---

**28. What are common Macro use cases in MIS?**

Common MIS macro use cases include: (1) Auto-formatting a pasted raw data dump into a clean report, (2) Auto-generating a PDF and emailing it via Outlook, (3) Consolidating data from multiple sheets or files into a master sheet, (4) Auto-applying conditional formatting to highlight SLA breaches, (5) Refreshing all pivot tables with one click, and (6) Auto-populating report headers (date, month, department) dynamically. These automations save hours of daily/weekly effort and eliminate manual errors.

---

**29. What are Macro security settings in Excel?**

Excel has four macro security levels: (1) Disable all macros without notification — blocks all macros, (2) Disable all macros with notification — asks user to enable, (3) Disable all macros except digitally signed macros — only trusted signed code runs, (4) Enable all macros — not recommended (security risk). Access via File > Options > Trust Center > Trust Center Settings > Macro Settings. For corporate MIS files, macros are typically enabled only for trusted locations or digitally signed workbooks.

---

**30. What are best practices for writing maintainable VBA?**

Best practices for VBA code: (1) Always use `Option Explicit` to force variable declaration, (2) Add comments explaining the purpose of each section, (3) Use meaningful variable names (`lastRow` not `x`), (4) Break large macros into smaller helper Subs, (5) Use `Application.ScreenUpdating = False` for performance, (6) Always handle errors with `On Error GoTo ErrorHandler`, and (7) Test on a copy of data before running on live files. Well-written VBA is readable, fast, and safe — critical for shared MIS tools that multiple people rely on.

---
