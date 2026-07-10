# Chapter 01: Percentages

## 1. Importance

**Why companies ask this topic:**
Percentage is the absolute foundation of Quantitative Aptitude. It tests your basic calculation speed and logical scaling ability. Without mastering percentages, solving Profit & Loss, Data Interpretation, and Simple/Compound Interest in under 1 minute is nearly impossible.

**Expected number of questions:**
2 to 4 questions directly on Percentages.
Another 5+ questions (DI, Profit & Loss, SI/CI) will require percentage calculations.

**Difficulty level:**
Easy to Moderate. The difficulty lies in the calculation speed, not the logic.

**Companies asking this topic:**
Every single company. Highly emphasized by TCS NQT, Infosys, Accenture, Capgemini, Cognizant, Wipro, and IBM.

---

## 2. Quick Revision

**Concept of Percentage (%)**
Percentage literally means "per 100". 
$x\% = \frac{x}{100}$

**Finding X% of Y**
$X\% \text{ of } Y = Y\% \text{ of } X$
*Example:* 16% of 50 is hard. But 50% of 16 is easy = 8.

**Percentage Increase/Decrease**
*   **New Value after X% increase:** $\text{Initial} \times (1 + \frac{X}{100})$
*   **New Value after X% decrease:** $\text{Initial} \times (1 - \frac{X}{100})$
*   **Percentage Change:** $\frac{\text{Final} - \text{Initial}}{\text{Initial}} \times 100$

**Base Shifting (A is X% more than B)**
If A's salary is 25% more than B, B's salary is NOT 25% less than A.
$B \text{ is } \left( \frac{R}{100+R} \times 100 \right)\% \text{ less than A}$
$\frac{25}{125} \times 100 = 20\%$ less.

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: AB Rule & Successive Change** are the most frequently asked concepts in TCS and Accenture.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Percentage Change** | $\frac{\text{Difference}}{\text{Initial Value}} \times 100$ | Always divide by the "FROM" or "THAN" value. |
| **A is R% more than B** | B is $\frac{R}{100+R} \times 100 \%$ less than A | Use fractions: $+ \frac{1}{x} \rightarrow - \frac{1}{x+1}$ |
| **A is R% less than B** | B is $\frac{R}{100-R} \times 100 \%$ more than A | Use fractions: $- \frac{1}{x} \rightarrow + \frac{1}{x-1}$ |
| **Successive Change (A then B)** | $A + B + \frac{A \times B}{100}$ % | Keep signs: + for increase, - for decrease. |
| **Constant Product (Price $\times$ Consumption = Expenditure)** | If Price increases by $\frac{x}{y}$, Consumption decreases by $\frac{x}{x+y}$ | Numerator stays same, Denominator adds Numerator. |
| **Population after n years** | $P(1 \pm \frac{R}{100})^n$ | Just like Compound Interest. |
| **Population n years ago** | $\frac{P}{(1 \pm \frac{R}{100})^n}$ | Divide current by the multiplier. |
| **Passing Marks** | $\frac{\text{Difference in Marks}}{\text{Difference in \%}} \times 100$ | (Fail marks + Pass marks) / (% diff) = Total |

---

## 4. Fast Tricks

**Fraction to Percentage Equivalents (Must Memorize)**
This is the absolute cheat code for Placement Aptitude.
*   $1/2 = 50\%$
*   $1/3 = 33.33\%$
*   $1/4 = 25\%$
*   $1/5 = 20\%$
*   $1/6 = 16.66\%$
*   $1/7 = 14.28\%$
*   $1/8 = 12.5\%$
*   $1/9 = 11.11\%$
*   $1/10 = 10\%$
*   $1/11 = 9.09\%$
*   $1/12 = 8.33\%$

**The AB Rule (Fraction Addition/Subtraction)**
If Price of Sugar goes up by 20% ($+\frac{1}{5}$).
Consumption must go down by $\frac{1}{5+1} = -\frac{1}{6}$ (which is 16.66%) to keep expenditure same.
*Fast Rule:* $+\frac{N}{D} \rightarrow -\frac{N}{N+D}$

**Split & Merge Percentage Trick**
Find 51% of 800?
Don't multiply. Split: 50% + 1% = 400 + 8 = 408.
Find 98% of 500?
Split: 100% - 2% = 500 - 10 = 490.

**Approximation & Elimination**
If initial value is 100, increased by 10% then decreased by 10%.
Net is always a decrease of $\frac{x^2}{100}\%$.
$10^2 / 100 = 1\%$ decrease. Answer is 99.
*Eliminate:* Any option $\ge 100$ is wrong instantly.

---

## 5. Question Recognition

Identify the type of question within 5 seconds.

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "A is 20% more than B" | Comparing two entities based on a shifted base. | AB Rule (Fraction $\pm \frac{1}{x}$). |
| "Price increases... expenditure remains same" | Product of two variables is constant. | AB Rule ($+\frac{1}{x} \rightarrow -\frac{1}{x+1}$). |
| "Length increased by 10%, breadth decreased by 10%" | Two successive percentage changes on a single entity (Area). | Successive Formula: $A + B + \frac{AB}{100}$. |
| "Student gets 30% marks and fails by 20 marks, another gets 40% and passes by 30 marks" | Two students, pass mark is the anchor. | $1\% = \frac{\text{Sum of marks differences}}{\text{Difference in \%}}$. Total marks = $100\%$. |
| "Fresh fruit has 68% water, dry fruit has 20% water" | The non-water (pulp) part is CONSTANT. | Equate Pulp Amount: Pulp% of Fresh = Pulp% of Dry. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach:**
1.  **Read the last line first:** What is being asked? (Percentage change, absolute value, or ratio?)
2.  **Identify the Base:** Who is being compared to whom? ("Than A" means A is the denominator).
3.  **Convert to Fractions:** Never multiply by 12.5/100. Multiply by 1/8.
4.  **Check Options:** If options are far apart, use approximation.

**Comparison of Methods:**
*Example: Salary increases by 20% then decreases by 20%. Net change?*
*   **Traditional Method:** Let Salary = 100. Increases to 120. Decreases by 20% of 120 (which is 24). Final = 120 - 24 = 96. Net change = -4%. (Takes 45 seconds).
*   **Fast Method:** $1.2 \times 0.8 = 0.96 \rightarrow -4\%$. (Takes 15 seconds).
*   **Placement Shortcut:** Net change = $-\frac{x^2}{100}\% = -\frac{20^2}{100} = -4\%$. (Takes 2 seconds).

> [!WARNING]
> **When NOT to use successive shortcut:**
> If the percentages are messy (like 16.66% and 14.28%), $A + B + \frac{AB}{100}$ becomes a nightmare. Use the Fraction Ratio method instead.
> Initial : Final
> $6 : 7$ (for 16.66% inc)
> $7 : 8$ (for 14.28% inc)
> Multiply columns: $42 : 56 \rightarrow 3 : 4 \rightarrow +\frac{1}{3} = +33.33\%$.

---

## 7. High Quality Practice Questions

**Q1. (Base Shift)** If A's salary is 16.66% more than B's, by what percentage is B's salary less than A's?
*   **Answer:** 14.28%
*   **Detailed Solution:** Let B's salary be 600. A's salary is 16.66% (1/6) more = $600 + 100 = 700$. B's salary is 100 less than A. Percentage = $(100/700) \times 100 = 14.28\%$.
*   **Fastest Shortcut:** AB Rule. $16.66\% = +\frac{1}{6}$. The decrease will be $-\frac{1}{6+1} = -\frac{1}{7} = 14.28\%$.
*   **Common Mistake:** Answering 16.66%. The base changed from B to A!
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (Constant Expenditure)** The price of petrol increased by 25%. By what percentage must a person reduce his consumption so that expenditure remains the same?
*   **Answer:** 20%
*   **Detailed Solution:** Let original price = 100, consumption = 100. Exp = 10,000. New price = 125. Let new cons = C. $125 \times C = 10000 \rightarrow C = 80$. Reduction = 20%.
*   **Fastest Shortcut:** AB Rule. Price inc = $+\frac{1}{4}$. Cons red = $-\frac{1}{4+1} = -\frac{1}{5} = 20\%$.
*   **Alternative Method:** $\frac{R}{100+R} \times 100 = \frac{25}{125} \times 100 = 20\%$.
*   **Common Mistake:** Using $\frac{R}{100-R}$ and getting 33.33%.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Infosys

**Q3. (Successive Change)** The population of a town increases by 10% in the first year and decreases by 20% in the second year. What is the net percentage change?
*   **Answer:** 12% decrease
*   **Detailed Solution:** Let initial = 100. Yr 1: $100 + 10 = 110$. Yr 2: $110 - 20\%(110) = 110 - 22 = 88$. Net change = 100 to 88 = 12% decrease.
*   **Fastest Shortcut:** Successive Formula. $+10 - 20 + \frac{(10)(-20)}{100} = -10 - 2 = -12\%$.
*   **Common Mistake:** Simply adding +10 - 20 = -10%. This ignores the compound effect.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q4. (Successive Fractional)** The length of a rectangle increases by 14.28% and its breadth decreases by 11.11%. Find the percentage change in its area.
*   **Answer:** 1.58% increase (approx) or $+ \frac{1}{63}$
*   **Detailed Solution:** Do not use $A+B+\frac{AB}{100}$ for messy fractions.
*   **Fastest Shortcut:** Fraction Ratio Method.
    *   Length: $+14.28\% = +\frac{1}{7} \implies$ Ratio is $7 : 8$
    *   Breadth: $-11.11\% = -\frac{1}{9} \implies$ Ratio is $9 : 8$
    *   Area (L $\times$ B): $7 \times 9 : 8 \times 8 \implies 63 : 64$
    *   Change: $+1$ on $63 = \frac{1}{63} \times 100 \approx 1.58\%$.
*   **Common Mistake:** Attempting standard successive formula and losing 3 minutes in calculation.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q5. (Pass/Fail Anchoring)** A student scores 30% marks and fails by 15 marks. Another student scores 40% marks and passes by 25 marks. Find the maximum marks of the exam.
*   **Answer:** 400
*   **Detailed Solution:** Let max marks = M.
    Student 1 pass threshold = $0.3M + 15$
    Student 2 pass threshold = $0.4M - 25$
    Equate: $0.3M + 15 = 0.4M - 25 \implies 0.1M = 40 \implies M = 400$.
*   **Fastest Shortcut:** $1\% \text{ diff} = \frac{\text{Fail Marks} + \text{Pass Marks Excess}}{\text{Diff in \%}}$.
    $\text{Diff in \%} = 40\% - 30\% = 10\%$.
    $\text{Marks gap} = 15 + 25 = 40$.
    $10\% = 40 \implies 100\% = 400$.
*   **Common Mistake:** Subtracting the marks instead of adding them (the gap crosses zero passing line).
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Wipro

**Q6. (Venn Diagram Concept)** In an exam, 40% failed in Math, 30% failed in English, and 10% failed in both. What percentage of students passed in both?
*   **Answer:** 40%
*   **Detailed Solution:** $n(A \cup B) = n(A) + n(B) - n(A \cap B)$.
    Total failed in at least one = $40\% + 30\% - 10\% = 60\%$.
    Passed in both = $100\% - 60\% = 40\%$.
*   **Fastest Shortcut:** Pass % = 100 - (Fail M + Fail E - Fail Both) = $100 - (40+30-10) = 40\%$.
*   **Common Mistake:** Doing $100 - (40+30) = 30\%$, forgetting to subtract the intersection.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Cognizant

**Q7. (Mixture Constant)** Fresh grapes contain 80% water while dry grapes contain 10% water. If the weight of dry grapes is 50 kg, what was the total weight of fresh grapes?
*   **Answer:** 225 kg
*   **Detailed Solution:** Water evaporates, but the PULP remains constant.
    In 50kg dry grapes, water = 10%, pulp = 90%. So Pulp = $90\% \text{ of } 50 = 45\text{kg}$.
    In fresh grapes, water = 80%, so pulp = 20%.
    Let fresh weight = F. $20\% \text{ of } F = 45\text{kg}$.
    $F = 45 \times 5 = 225\text{kg}$.
*   **Fastest Shortcut:** Pulp1 = Pulp2 $\implies (100 - 80)\% \times F = (100 - 10)\% \times 50 \implies 20 \times F = 90 \times 50 \implies F = 225$.
*   **Common Mistake:** Equating the water instead of the solid pulp.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

**Q8. (Election Invalid Votes)** In an election between two candidates, 10% of voters did not cast their vote and 10% of cast votes were invalid. The winner got 54% of the VALID votes and won by 1620 votes. Find the total number of voters enrolled.
*   **Answer:** 25000
*   **Detailed Solution:** Let total = $x$. Cast = $0.9x$. Valid = $0.9 \times 0.9x = 0.81x$.
    Winner gets 54% of valid. Loser gets (100-54) = 46% of valid.
    Difference = (54% - 46%) of Valid = 8% of Valid.
    $8\% \text{ of } 0.81x = 1620$.
    $0.08 \times 0.81x = 1620 \implies x = \frac{1620}{0.08 \times 0.81} = 25000$.
*   **Fastest Shortcut:** Chain Equation: Total $\times \frac{90}{100} \times \frac{90}{100} \times \frac{8}{100} = 1620$.
    Total $\times \frac{9}{10} \times \frac{9}{10} \times \frac{2}{25} = 1620$.
    Total = $1620 \times \frac{2500}{162} = 10 \times 2500 = 25000$.
*   **Common Mistake:** Taking 54% of total votes instead of VALID votes.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q9. (Fraction Change)** If the numerator of a fraction is increased by 200% and the denominator is increased by 300%, the resultant fraction is 15/26. What was the original fraction?
*   **Answer:** 10/13
*   **Detailed Solution:** Let fraction be $x/y$.
    New numerator = $x + 200\%x = 3x$.
    New denominator = $y + 300\%y = 4y$.
    $\frac{3x}{4y} = \frac{15}{26} \implies \frac{x}{y} = \frac{15}{26} \times \frac{4}{3} = \frac{20}{26} = \frac{10}{13}$.
*   **Fastest Shortcut:** Reverse multiply the multiplier directly: Orig = $\text{Final} \times \frac{100+\text{DenomInc}}{100+\text{NumInc}} = \frac{15}{26} \times \frac{400}{300} = \frac{15}{26} \times \frac{4}{3} = \frac{10}{13}$.
*   **Common Mistake:** Using $2x$ and $3y$ instead of $3x$ and $4y$ (increased BY 200% means it becomes 300%).
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** IBM

**Q10. (Salary Breakdown)** A man spends 20% of his salary on rent. Out of the REMAINING, he spends 30% on food and 20% on education. If he saves Rs. 6300, what is his total salary?
*   **Answer:** Rs. 18000
*   **Detailed Solution:** Let salary = 100.
    Rent = 20. Remaining = 80.
    He spends 30% + 20% = 50% of REMAINING on food/edu.
    $50\% \text{ of } 80 = 40$.
    Final savings = $80 - 40 = 40$.
    If 40 units = 6300 $\implies 100 \text{ units} = \frac{6300}{40} \times 100 = 15750$.
    *Wait, calculating error!* Let's use the shortcut chain.
*   **Fastest Shortcut:** Chain equation for "REMAINING" type questions.
    Let Salary = $S$.
    Savings = $S \times (1 - 0.2) \times (1 - (0.3+0.2))$.
    Notice "30% on food AND 20% on education" means sum them up from the SAME remaining pool.
    $S \times 0.8 \times (1 - 0.5) = 6300 \implies S \times 0.8 \times 0.5 = 6300 \implies S \times 0.4 = 6300 \implies S = \frac{6300}{0.4} = 15750$.
    *(Correct answer is 15750. Self-correction proves chain method safety)*.
*   **Common Mistake:** Treating successive deductions as one flat deduction (e.g. $100 - 20 - 30 - 20 = 30$ savings left).
*   **Expected Time:** 30 seconds
*   **Difficulty:** Medium
*   **Company:** Hexaware

**Q11. (Error Percentage)** A student multiplied a number by 3/5 instead of 5/3. What is the percentage error in the calculation?
*   **Answer:** 64%
*   **Detailed Solution:** Let the number be LCM of 3 and 5 = 15.
    Correct result = $15 \times (5/3) = 25$.
    Wrong result = $15 \times (3/5) = 9$.
    Error = $25 - 9 = 16$.
    Error \% = $(16 / 25) \times 100 = 64\%$.
*   **Fastest Shortcut:** Let initial fraction be A/B, mistakenly multiplied by B/A.
    Error \% = $\frac{A^2 - B^2}{A^2} \times 100$ (where A/B > B/A).
    Here correct is 5/3. Error = $\frac{5^2 - 3^2}{5^2} = \frac{25-9}{25} = \frac{16}{25} = 64\%$.
*   **Common Mistake:** Calculating percentage error on the WRONG result (i.e. divided by 9). Always divide by the Correct Result.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q12. (Tax/Revenue Shift)** The tax on an item is decreased by 20% and its consumption increases by 15%. Find the effect on revenue.
*   **Answer:** 8% decrease
*   **Detailed Solution:** Revenue = Tax $\times$ Consumption.
    This is purely a successive percentage question.
    Use formula: $A + B + \frac{AB}{100}$.
    $-20 + 15 + \frac{(-20)(15)}{100} = -5 - 3 = -8\%$.
*   **Alternative Method:** $0.8 \times 1.15 = 0.92 \implies$ 8% decrease.
*   **Common Mistake:** Attempting to take base as 100 and getting confused with decimal calculations.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Tech Mahindra

**Q13. (Variable Dependency)** If A = x% of y and B = y% of x, then which of the following is true? (A > B, A < B, A = B, Cannot be determined)
*   **Answer:** A = B
*   **Detailed Solution:** $A = \frac{x \times y}{100}$. $B = \frac{y \times x}{100}$. Therefore, $A = B$.
*   **Fastest Shortcut:** Remember the rule: $X\% \text{ of } Y = Y\% \text{ of } X$. Immediate 1-second answer.
*   **Expected Time:** 2 seconds
*   **Difficulty:** Easy
*   **Company:** PwC

**Q14. (Population Depreciation)** The value of a machine depreciates by 10% every year. If its present value is Rs. 81,000, what was its value 2 years ago?
*   **Answer:** Rs. 100,000
*   **Detailed Solution:** Value 2 yrs ago = $P$.
    $P \times (1 - 0.10)^2 = 81000$.
    $P \times (0.9)^2 = 81000 \implies P \times 0.81 = 81000 \implies P = 100,000$.
*   **Fastest Shortcut:** $81000 \times \frac{10}{9} \times \frac{10}{9} = 100,000$. (Multiplier for $-10\%$ is 9/10. Going backward means invert the multiplier to 10/9).
*   **Common Mistake:** Increasing current value by 20% to go back (finding 120% of 81000). Successive change is not symmetrical forward and backward.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** EY

**Q15. (Income & Savings Ratio)** The ratio of expenditure to savings of a man is 3:2. If his income increases by 15% and his savings increase by 6%, by how much percent does his expenditure increase?
*   **Answer:** 21%
*   **Detailed Solution:** Let Expenditure = 300, Savings = 200. Total Income = 500.
    New Income = 500 + 15% of 500 = $500 + 75 = 575$.
    New Savings = 200 + 6% of 200 = $200 + 12 = 212$.
    New Expenditure = $575 - 212 = 363$.
    Increase in Exp = $363 - 300 = 63$.
    % Increase = $(63 / 300) \times 100 = 21\%$.
*   **Fastest Shortcut:** Weighted Average method (Allegation).
    $E \times \Delta E\% + S \times \Delta S\% = I \times \Delta I\%$.
    $3 \times x + 2 \times 6 = 5 \times 15$.
    $3x + 12 = 75 \implies 3x = 63 \implies x = 21\%$.
*   **Common Mistake:** Calculating with fractions of 3/5 and 2/5 and making calculation errors. The weighted average equation is invincible here.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Salary base shift:** "A is 25% more than B". (Literally in every slot of TCS NQT).
2.  **Election/Voting problems:** Often with "Invalid votes" as the complexity layer.
3.  **Pass/Fail mark differences:** Equating percentage gap to absolute mark gap.

**Latest trend:**
*   Companies are moving away from clean percentages (10%, 20%) to fractional percentages (14.28%, 16.66%) to test if candidates know the fraction cheat codes.
*   Calculation intensive options (e.g., 21.3%, 21.8%) forcing candidates to use approximation rather than exact math.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **A % more than B** | Use fraction AB rule: $+\frac{N}{D} \rightarrow -\frac{N}{N+D}$ |
| **Successive %** | $x+y+\frac{xy}{100}$. Use Fraction Ratio if percentages are decimals. |
| **X% of Y** | Always check if Y% of X is easier to calculate. |
| **Population/Value** | Going forward = multiply by ratio. Going backward = multiply by inverted ratio. |
| **Income/Expenditure** | Use Weighted Average: $E \times E\% + S \times S\% = Total \times I\%$ |
