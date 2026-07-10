# Chapter 20: Data Interpretation

## 1. Importance

**Why companies ask this topic:**
Data Interpretation (DI) is the most practical aptitude skill. It tests your ability to extract meaning from business dashboards, charts, and tables without getting overwhelmed by raw data.

**Expected number of questions:**
4 to 5 questions. (Usually presented as one large chart followed by 4-5 connected questions).

**Difficulty level:**
Easy to Moderate. The math is just basic Percentages, Averages, and Ratios. The difficulty lies entirely in *calculation speed* and *careful reading*.

**Companies asking this topic:**
Every single company. TCS NQT (High weightage), Infosys, Accenture, Cognizant, Wipro, Capgemini, IBM, Deloitte.

---

## 2. Quick Revision

**The 3 Pillars of DI:**
Every DI question is a disguised version of one of these three concepts:
1.  **Ratio:** "What is the ratio of cars produced in 2020 to 2021?"
2.  **Average:** "What is the average production over 5 years?"
3.  **Percentage:** "Production in 2020 is what percent of 2021?" OR "What is the percentage increase?"

**Types of Charts:**
*   **Tabular DI:** Raw data in rows and columns. High calculation intensive.
*   **Bar Graphs:** Easy to read. Compare heights visually before calculating.
*   **Line Graphs:** Shows trends over time. Look for steepest slopes for maximum growth.
*   **Pie Charts:** Data out of $360^{\circ}$ or $100\%$. The ultimate test of fraction/degree conversion.

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The Percentage Formula** ($x$ is what percent of $y$?) is the foundation of 70% of all DI questions.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **$x$ is what % of $y$?** | $\frac{x}{y} \times 100$ | The word after "OF" goes in the denominator. |
| **What % is $x$ more/less than $y$?**| $\frac{\text{Difference}}{\text{Reference value}} \times 100$ | The word after "THAN" goes in the denominator. |
| **Percentage Increase** | $\frac{\text{Final} - \text{Initial}}{\text{Initial}} \times 100$ | Base is ALWAYS the initial value (previous year). |
| **Pie Chart (Degrees to %)** | $\text{Value in } \% = \frac{\text{Angle}}{360^{\circ}} \times 100$ | $36^{\circ} = 10\%$. $18^{\circ} = 5\%$. |
| **Pie Chart (% to Degrees)** | $\text{Angle} = \frac{\text{Percentage}}{100} \times 360^{\circ}$ | $1\% = 3.6^{\circ}$. |
| **Average Growth Rate** | $\frac{\text{Sum of all yearly growth \%}}{\text{Number of years}}$ | Calculate year-by-year % increase, then average. |

---

## 4. Fast Tricks

**The "Visual Elimination" Trick**
If a bar graph asks: "In which year was the percentage increase maximum?"
Do NOT calculate the % increase for every year. Look for the bar that shows the largest visual jump relative to its previous height. A jump from 10 to 20 is a 100% increase (huge), while a jump from 100 to 120 is only a 20% increase, even though the absolute height difference (20) is larger.

**The "Base Approximation" Trick**
"What is 342 as a percentage of 815?"
Don't do $342/815 \times 100$. Look at the base: 815.
$10\%$ of $815 = 81.5$
$40\%$ of $815 = 81.5 \times 4 \approx 326$.
342 is slightly more than 326.
So the answer must be slightly more than 40%. (Around 42%). Look at the options and tick.

**The "Global Ratio" Pie Chart Trick**
If a pie chart gives total population = 450,000, and asks for the ratio of City A (15%) to City B (25%).
NEVER calculate the actual populations ($15\%$ of 450,000).
Ratio = $15\% : 25\% = 3 : 5$. (The total population cancels out).

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "What percent OF total..." | Division fraction. | Value / Total $\times 100$. |
| "What percent MORE THAN..."| Difference fraction. | (Diff / Base) $\times 100$. |
| "Ratio of A in 2018 to B in 2019" | Don't calculate totals if not needed. | Just put the raw values from chart in ratio. |
| "Angle of the sector for..." | Pie chart conversion. | $\% \times 3.6^{\circ}$. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach for DI:**
1.  **Read the Axis/Headers First:** Spend 15 seconds understanding the units (Are they in thousands? millions? degrees?). This saves you from off-by-zero errors.
2.  **Read the Question's "OF/THAN" targets:** Identify exactly what goes in the numerator and denominator.
3.  **Approximate before Calculating:** If options are far apart (e.g., 20%, 40%, 60%, 80%), use the 10% base approximation trick. NEVER do long division unless options are very close (like 42.1% and 42.8%).

**Comparison of Methods:**
*Example: Total Students = 8500. Biology students are 18%. Chemistry students are 14%. How many more students study Biology than Chemistry?*
*   **Traditional Method:**
    Biology = $18\%$ of $8500 = 1530$.
    Chemistry = $14\%$ of $8500 = 1190$.
    Difference = $1530 - 1190 = 340$. (Calculated two large percentages).
*   **Placement Shortcut (Global Percentage Method):**
    Difference in % = $18\% - 14\% = 4\%$.
    Difference in students = $4\%$ of $8500 = 4 \times 85 = 340$. (Single, easy calculation).

> [!WARNING]
> **The Zero-Base Trap:**
> You cannot calculate a percentage increase if the initial value is 0. If a company produced 0 cars in 2018 and 100 in 2019, the percentage increase is undefined/infinite, not 100%.

---

## 7. High Quality Practice Questions (Simulated Dataset)

**DATASET 1 (Q1 to Q5):**
*The following table shows the number of laptops produced (in thousands) by three companies (Dell, HP, Lenovo) over 5 years.*

| Year | Dell | HP | Lenovo |
| :--- | :--- | :--- | :--- |
| 2018 | 45 | 50 | 60 |
| 2019 | 55 | 55 | 65 |
| 2020 | 65 | 60 | 50 |
| 2021 | 50 | 75 | 70 |
| 2022 | 85 | 80 | 90 |

**Q1. What is the average production of HP laptops over the given 5 years?**
*   **Answer:** 64,000
*   **Detailed Solution:** Sum of HP = $50 + 55 + 60 + 75 + 80 = 320$.
    Average = $320 / 5 = 64$.
    Since data is in thousands, Average = 64,000.
*   **Fastest Shortcut:** Assume an average of 60. Deviations: $-10, -5, 0, +15, +20$.
    Sum of deviations = $+20$. Average deviation = $20/5 = +4$.
    Actual average = $60 + 4 = 64$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. The total production of Dell in 2019 and 2020 together is what percent of the total production of Lenovo over all 5 years?**
*   **Answer:** 35.8%
*   **Detailed Solution:** Dell (2019 + 2020) = $55 + 65 = 120$.
    Lenovo (Total) = $60 + 65 + 50 + 70 + 90 = 335$.
    Percentage = $(120 / 335) \times 100$.
    $= (24 / 67) \times 100 \approx 35.8\%$.
*   **Fastest Shortcut:** Approximation. $10\%$ of $335 = 33.5$.
    $30\% = 100.5$. We need 120. We are short by roughly 20.
    $1\%$ of $335 = 3.35$. $6\%$ is roughly 20.
    So $30\% + 6\% \approx 36\%$. Options will let you pick 35.8%.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Medium
*   **Company:** Infosys

**Q3. What is the ratio of total production of all companies in 2018 to total production of all companies in 2022?**
*   **Answer:** 31 : 51
*   **Detailed Solution:** Total 2018 = $45 + 50 + 60 = 155$.
    Total 2022 = $85 + 80 + 90 = 255$.
    Ratio = $155 : 255 = 31 : 51$ (Divide by 5).
*   **Fastest Shortcut:** Just add the rows and divide.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** Wipro

**Q4. In which year was the percentage increase in Dell's production maximum as compared to the previous year?**
*   **Answer:** 2022
*   **Detailed Solution:**
    2019: Jump from 45 to 55 $\implies +10$ on base $45 \implies 22.2\%$.
    2020: Jump from 55 to 65 $\implies +10$ on base $55 \implies 18.1\%$.
    2021: Production decreased (50).
    2022: Jump from 50 to 85 $\implies +35$ on base $50 \implies 70\%$.
*   **Fastest Shortcut:** Visual/Mental elimination. The jump in 2022 is 35 from 50 (more than half). The others are tiny fractions. No calculation needed.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q5. The total production of HP in 2021 is what percent more than the production of Lenovo in 2020?**
*   **Answer:** 50%
*   **Detailed Solution:** HP(2021) = 75. Lenovo(2020) = 50.
    Difference = $75 - 50 = 25$.
    "THAN Lenovo 2020", so base is 50.
    Percentage = $(25 / 50) \times 100 = 50\%$.
*   **Fastest Shortcut:** 75 is $1.5\times$ of 50. That means 50% more.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**DATASET 2 (Q6 to Q10): Pie Chart**
*A pie chart shows the distribution of 3600 employees in 5 departments: HR (10%), IT (25%), Sales (30%), Marketing (20%), Finance (15%).*

**Q6. What is the total number of employees in IT and Finance together?**
*   **Answer:** 1440
*   **Detailed Solution:** Total % = $IT (25\%) + Finance (15\%) = 40\%$.
    $40\%$ of $3600 = 0.4 \times 3600 = 1440$.
*   **Fastest Shortcut:** Add percentages first, then calculate.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Cognizant

**Q7. What is the central angle corresponding to the Sales department?**
*   **Answer:** $108^{\circ}$
*   **Detailed Solution:** Sales = 30%.
    Angle = $30\% \text{ of } 360^{\circ} = \frac{30}{100} \times 360 = 108^{\circ}$.
*   **Fastest Shortcut:** $1\% = 3.6^{\circ}$. So $30 \times 3.6 = 108$.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q8. The number of employees in Marketing is what percent of the number of employees in HR?**
*   **Answer:** 200%
*   **Detailed Solution:** Marketing = 20%. HR = 10%.
    Required % = $(20 / 10) \times 100 = 2 \times 100 = 200\%$.
*   **Fastest Shortcut:** Marketing is double of HR. Double means 200%. No need to use the 3600 total.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Medium
*   **Company:** IBM

**Q9. If 20% of the IT employees are female, how many male employees are there in the IT department?**
*   **Answer:** 720
*   **Detailed Solution:** Total IT employees = $25\%$ of $3600 = 900$.
    Female = 20%. So Male = 80%.
    Male in IT = $80\%$ of $900 = 0.8 \times 900 = 720$.
*   **Fastest Shortcut:** Male IT = $80\% \text{ of } 25\% \text{ of } 3600$.
    $0.8 \times 0.25 = 0.2$ ($20\%$ of total).
    $20\%$ of $3600 = 720$. (Much faster!).
*   **Expected Time:** 15 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

**Q10. If the total number of employees increases by 10% next year, but the HR percentage remains the same, how many new HR employees will be added?**
*   **Answer:** 36
*   **Detailed Solution:** New Total = $3600 \times 1.1 = 3960$.
    New HR = $10\%$ of $3960 = 396$.
    Old HR = $10\%$ of $3600 = 360$.
    New added = $396 - 360 = 36$.
*   **Fastest Shortcut:** The increase in HR is simply 10% of the overall increase.
    Overall increase = 360.
    $10\%$ of $360 = 36$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**DATASET 3 (Q11 to Q15): Line Graph (Profit/Loss)**
*A line graph shows the Profit % earned by Company A over 5 years (2010 to 2014): 10%, 20%, 15%, 30%, 25%.*
*Profit % = $\frac{\text{Income} - \text{Expenditure}}{\text{Expenditure}} \times 100$*

**Q11. If the Expenditure in 2011 was Rs. 200 lakhs, what was the Income?**
*   **Answer:** 240 lakhs
*   **Detailed Solution:** Profit in 2011 = 20%.
    Profit = $20\%$ of Expenditure = $20\%$ of $200 = 40$ lakhs.
    Income = Expenditure + Profit = $200 + 40 = 240$ lakhs.
*   **Fastest Shortcut:** Income = $120\%$ of Exp. $1.2 \times 200 = 240$.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** EY

**Q12. If the Income in 2013 was Rs. 260 lakhs, what was the Expenditure?**
*   **Answer:** 200 lakhs
*   **Detailed Solution:** Profit in 2013 = 30%.
    Income = Expenditure $\times 1.30$.
    $260 = E \times 1.3 \implies E = 260 / 1.3 = 200$ lakhs.
*   **Fastest Shortcut:** $E = I / 1.3$.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** PwC

**Q13. In which year did the company earn the maximum absolute profit?**
*   **Answer:** Cannot be determined
*   **Detailed Solution:** The graph only gives Profit PERCENTAGE. Absolute profit depends on the base Expenditure. Without knowing the expenditure for each year, we cannot find the absolute profit.
*   **Fastest Shortcut:** Recognize "Cannot be determined" instantly when absolute values are asked from purely percentage graphs.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q14. If the Expenditure in 2010 and 2012 were equal, what is the ratio of Income in 2010 to Income in 2012?**
*   **Answer:** 22 : 23
*   **Detailed Solution:** Let Expenditure be 100.
    Income 2010 = $100 + 10\% \text{ of } 100 = 110$.
    Income 2012 = $100 + 15\% \text{ of } 100 = 115$.
    Ratio = $110 : 115$. Divide by 5 = $22 : 23$.
*   **Fastest Shortcut:** Ratio of Incomes = Ratio of $(100 + P\%)$.
    $= 110 : 115 = 22 : 23$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q15. If the Income in 2014 was Rs. 500 lakhs, what was the Profit earned in that year?**
*   **Answer:** 100 lakhs
*   **Detailed Solution:** Profit in 2014 = 25%.
    Income = $125\%$ of Expenditure.
    $500 = 1.25 \times E \implies E = 500 / 1.25 = 400$ lakhs.
    Profit = Income - Expenditure = $500 - 400 = 100$ lakhs.
*   **Fastest Shortcut:** If Profit is 25% (1/4 of Exp), then Income is 5/4 of Exp.
    Profit is 1/5th of Income.
    $1/5 \text{ of } 500 = 100$. (Insanely fast trick).
*   **Expected Time:** 10 seconds
*   **Difficulty:** Hard
*   **Company:** IBM

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Global vs Local Percentages:** Asking for the difference in numbers by using the difference in pie-chart percentages (Q6).
2.  **Cannot Be Determined:** Providing a line graph of Profit % and asking for absolute profit without giving Expenditure (Q13).
3.  **"OF" vs "THAN":** Checking if the student knows which number goes in the denominator.

**Latest trend:**
*   **Spider Web / Radar Charts:** Same mathematical concepts as Line graphs, just drawn in a circle to confuse candidates. Just read the nodes like a bar graph.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **Percentage Shortcut** | Calculate $10\%$ and $1\%$ mentally to approximate options. |
| **Pie Chart Totals** | Don't use the Total Value if asked for a Ratio or Percentage. |
| **Profit % Graph** | Income = Expenditure $\times (100 + P)/100$. |
| **Visual Elimination** | For "Maximum % Increase", look for the largest bar jump relative to its own height. |
| **"Cannot be determined"** | Absolute values cannot be derived from purely % graphs without a base. |
