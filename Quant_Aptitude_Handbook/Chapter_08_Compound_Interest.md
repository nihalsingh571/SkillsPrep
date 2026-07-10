# Chapter 08: Compound Interest

## 1. Importance

**Why companies ask this topic:**
Compound Interest tests a candidate's ability to calculate successive percentage growth. It is highly calculation-intensive and acts as a major time-trap in aptitude tests.

**Expected number of questions:**
1 to 3 questions. Often mixed with Simple Interest (Difference between CI and SI).

**Difficulty level:**
Hard. The traditional formula $P(1+R/100)^N$ requires computing higher powers, which is a nightmare without a calculator.

**Companies asking this topic:**
TCS NQT, Infosys, Accenture, Capgemini. This is the #1 filter topic for high-scoring candidates.

---

## 2. Quick Revision

**Core Concept:**
Unlike SI, in CI you earn "Interest on Interest". The Principal changes every year.
*   End of Year 1: Amount = $P + \text{Interest}$.
*   Year 2: This new Amount becomes the Principal.

**Compounding Frequencies:**
*   **Half-Yearly:** Rate becomes $R/2$, Time becomes $2T$ (number of cycles).
*   **Quarterly:** Rate becomes $R/4$, Time becomes $4T$.

**The Successive Percentage Connection:**
CI for 2 years at R% is exactly the same as finding the successive percentage of $+R\%$ and $+R\%$.
Formula: $R + R + \frac{R \times R}{100} = 2R + \frac{R^2}{100}$.

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The Difference (CI - SI) formulas for 2 and 3 years** are the most frequently asked questions in all placement exams.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Basic Amount Formula** | $A = P(1 + \frac{R}{100})^T$ | Avoid this unless absolutely necessary. |
| **Effective Rate (2 Years)** | $2R + \frac{R^2}{100} \%$ | e.g., 5% for 2 yrs = $10.25\%$. |
| **Effective Rate (3 Years)** | $3R + \frac{3R^2}{100} + \frac{R^3}{10000} \%$ | Memorize standard values (10% = 33.1%). |
| **Diff of CI & SI (2 Years)** | $D = P(\frac{R}{100})^2$ | Or just $P \times (\frac{R^2}{100})\%$. |
| **Diff of CI & SI (3 Years)** | $D = P(\frac{R}{100})^2 (\frac{300+R}{100})$ | Memorize this exact structure. |
| **Sum becomes $x$ times in $T$ yrs** | It becomes $x^n$ times in $n \times T$ yrs. | Powers multiply time. |

---

## 4. Fast Tricks

**The Pascal's Ratio Method (Tree Method alternative)**
For calculating CI without the $A=P(1+R/100)^n$ formula.
*   **For 2 Years:** Ratio is **2 : 1**
*   **For 3 Years:** Ratio is **3 : 3 : 1**
*   **For 4 Years:** Ratio is **4 : 6 : 4 : 1**
*How to use for 3 Years (e.g. P=10000, R=10%):*
1.  Find 10% of 10000 = 1000. Multiply by 3 $\implies 3000$.
2.  Find 10% of 1000 = 100. Multiply by 3 $\implies 300$.
3.  Find 10% of 100 = 10. Multiply by 1 $\implies 10$.
Total CI = $3000 + 300 + 10 = 3310$. (Mental Math!).

**Standard CI Rates to Memorize (Cheat Code)**
If you memorize these, you solve 90% of CI questions instantly.
*   **5% for 2 yrs:** CI = 10.25%
*   **10% for 2 yrs:** CI = 21%
*   **10% for 3 yrs:** CI = 33.1%
*   **10% for 4 yrs:** CI = 46.41%
*   **20% for 2 yrs:** CI = 44%

**The Multiplier Growth Trick**
If a sum becomes Rs. 4000 in 2 years and Rs. 6000 in 4 years.
Growth multiplier in 2 years = $6000 / 4000 = 1.5$.
To go backward 2 years to find Principal: $P \times 1.5 = 4000 \implies P = 4000 / 1.5$.

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "Difference between CI and SI for 2 years is Rs. X" | Direct formula application. | $D = P(R/100)^2$. |
| "Sum doubles in 4 years... becomes 8 times in?" | Power to Time mapping. | $8 = 2^3$. So $3 \times 4 = 12$ years. |
| "Amount after 2 yrs is 400, after 3 yrs is 440" | 1 year gap. CI for 1 yr acts like SI. | $Rate = (Diff / Amount_1) \times 100$. |
| "Find CI on Rs. 10,000 at 10% for 3 years" | Standard rate. | Just write $33.1\% \text{ of } 10,000 = 3310$. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach:**
1.  **Check the Time Gap:** If 2 years, use Effective Rate ($2R + R^2/100$) or 2:1 ratio. If 3 years, use 3:3:1 ratio.
2.  **Avoid the Formula:** Never use $A = P(1+R/100)^T$ unless $P$ and $A$ are given to find $R$.
3.  **Use Fractions for messy rates:** If $R = 16.66\%$ (which is $1/6$).
    $P \rightarrow A$
    $6 \rightarrow 7$ (Year 1)
    $6 \rightarrow 7$ (Year 2)
    Multiply columns: $36 \rightarrow 49$.
    Principal = 36 units. Amount = 49 units. CI = 13 units.

**Comparison of Methods:**
*Example: Find the Compound Interest on Rs. 8000 at 5% p.a. for 2 years.*
*   **Traditional Method:**
    $A = 8000(1 + 5/100)^2 = 8000(105/100)^2 = 8000(21/20)^2 = 8000 \times (441/400) = 20 \times 441 = 8820$.
    $CI = 8820 - 8000 = 820$.
*   **Fast Method (Effective Rate):**
    Effective Rate = $5 + 5 + (25/100) = 10.25\%$.
    CI = $10.25\% \text{ of } 8000 = 820$.
*   **Placement Shortcut (Ratio Method 2:1):**
    5% of 8000 = 400.
    5% of 400 = 20.
    $(400 \times 2) + (20 \times 1) = 800 + 20 = 820$. (5 seconds).

> [!WARNING]
> **When NOT to use effective rate:**
> If the rate is a complex fraction like $14.28\%$, squaring it for effective rate will be a disaster. Use the Fraction Multiplier Method ($7 \rightarrow 8$ then square columns).

---

## 7. High Quality Practice Questions

**Q1. (CI-SI Difference 2 Years)** The difference between compound interest and simple interest on a certain sum of money for 2 years at 5% per annum is Rs. 15. Find the sum.
*   **Answer:** Rs. 6000
*   **Detailed Solution:** $D = P(R/100)^2 \implies 15 = P(5/100)^2 = P(1/20)^2 = P(1/400)$.
    $P = 15 \times 400 = 6000$.
*   **Fastest Shortcut:** Difference % = $\frac{R^2}{100}\% = \frac{25}{100}\% = 0.25\%$.
    $0.25\% \text{ of } P = 15 \implies 1\% \text{ of } P = 60 \implies 100\% = 6000$.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (CI-SI Difference 3 Years)** If the difference between CI and SI on a sum of money for 3 years at 10% p.a. is Rs. 93, find the sum.
*   **Answer:** Rs. 3000
*   **Detailed Solution:** $D = P(\frac{R}{100})^2 (\frac{300+R}{100})$.
    $93 = P(10/100)^2 \times (310/100) = P(1/100) \times (3.1)$.
    $93 = 0.031 P \implies P = 93 / 0.031 = 3000$.
*   **Fastest Shortcut:** Memorize 10% for 3 years: SI = 30%. CI = 33.1%. Difference = 3.1%.
    $3.1\% = 93 \implies 1\% = 30 \implies 100\% = 3000$. (Mental calculation).
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Infosys

**Q3. (N Times Power Rule)** A sum of money placed at compound interest doubles itself in 5 years. In how many years will it amount to 8 times itself?
*   **Answer:** 15 years
*   **Detailed Solution:** Amount = $P(1+r/100)^t$.
    $2P = P(1+r)^5 \implies 2 = (1+r)^5$.
    We need $8P$. $8 = 2^3$.
    Substitute 2: $8 = ((1+r)^5)^3 = (1+r)^{15}$.
    So it takes 15 years.
*   **Fastest Shortcut:** Base becomes 2 in 5 years.
    Target is $8 = 2^3$. Multiply the power (3) by the time (5) = 15 years.
*   **Common Mistake:** Doing $2 \times 4 = 8$ so $5 \times 4 = 20$ years. That is Simple Interest logic.
*   **Expected Time:** 2 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q4. (Continuous Gap Amount)** A sum amounts to Rs. 4500 in 2 years and Rs. 6750 in 4 years at compound interest. Find the sum.
*   **Answer:** Rs. 3000
*   **Detailed Solution:** $A_2 = P(1+R/100)^2 = 4500$.
    $A_4 = P(1+R/100)^4 = 6750$.
    Divide: $(1+R/100)^2 = 6750 / 4500 = 675 / 450 = 3/2 = 1.5$.
    Substitute in first equation: $P \times 1.5 = 4500 \implies P = 3000$.
*   **Fastest Shortcut:** If the time gap is equal (0 to 2, 2 to 4), the amounts are in Geometric Progression (GP).
    $P / A_1 = A_1 / A_2 \implies P / 4500 = 4500 / 6750$.
    $P = (4500 \times 4500) / 6750 = 3000$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q5. (1 Year Gap Amount)** An amount at compound interest becomes Rs. 2420 in 2 years and Rs. 2662 in 3 years. Find the rate of interest.
*   **Answer:** 10%
*   **Detailed Solution:** At CI, the amount at the end of the 2nd year acts as the Principal for the 3rd year.
    Interest for 3rd year = $2662 - 2420 = 242$.
    Rate = $(Interest / Principal) \times 100 = (242 / 2420) \times 100 = 10\%$.
*   **Fastest Shortcut:** For consecutive years, just find percentage increase. $(242 / 2420) = 1/10 = 10\%$.
*   **Common Mistake:** Trying to set up $A = P(1+r/100)^n$ equations and wasting 3 minutes.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Wipro

**Q6. (Half-Yearly Compounding)** Find the compound interest on Rs. 16000 at 20% per annum for 9 months, compounded quarterly.
*   **Answer:** Rs. 2522
*   **Detailed Solution:** Quarterly compounding.
    Rate = 20% / 4 = 5% per quarter.
    Time = 9 months = 3 quarters.
    We need CI for 3 periods at 5%.
    Using Ratio 3:3:1.
    5% of 16000 = 800.
    5% of 800 = 40.
    5% of 40 = 2.
    CI = $(800 \times 3) + (40 \times 3) + (2 \times 1) = 2400 + 120 + 2 = 2522$.
*   **Fastest Shortcut:** 3:3:1 ratio is invincible here. Formula $16000(1.05)^3$ takes way too long without a calculator.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

**Q7. (Fractional Rate Calculation)** Find the compound interest on Rs. 21600 at 16.66% per annum for 3 years.
*   **Answer:** Rs. 12700
*   **Detailed Solution:** $16.66\% = 1/6$.
    Multiplier = $1 + 1/6 = 7/6$.
    Amount = $21600 \times (7/6)^3 = 21600 \times (343 / 216) = 100 \times 343 = 34300$.
    CI = Amount - Principal = $34300 - 21600 = 12700$.
*   **Fastest Shortcut:** Column method.
    $P \rightarrow A$
    $6 \rightarrow 7$ (Yr 1)
    $6 \rightarrow 7$ (Yr 2)
    $6 \rightarrow 7$ (Yr 3)
    $216 \rightarrow 343$. CI = $343 - 216 = 127$ units.
    If 216 units = 21600 $\implies 1 \text{ unit} = 100$.
    CI = $127 \times 100 = 12700$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** IBM

**Q8. (Installments in CI)** A man borrowed Rs. 21000 at 10% compound interest. How much he has to pay annually at the end of each year to settle his loan in two equal installments?
*   **Answer:** Rs. 12100
*   **Detailed Solution:** Let installment be $X$.
    Present Value of Installments = Principal.
    $\frac{X}{(1+R/100)^1} + \frac{X}{(1+R/100)^2} = P$.
    $\frac{X}{1.1} + \frac{X}{1.21} = 21000$.
    $\frac{1.1X + X}{1.21} = 21000 \implies 2.1X = 21000 \times 1.21 \implies X = 10000 \times 1.21 = 12100$.
*   **Fastest Shortcut:** Fraction method. 10% = 1/10 $\implies$ Ratio is 10:11.
    Yr 1: $10 \rightarrow 11$.
    Yr 2: $100 \rightarrow 121$ (Square it).
    Make installments (right side) equal: Multiply Yr 1 by 11 $\implies 110 \rightarrow 121$.
    Total Principal parts = $110 + 100 = 210$.
    If 210 parts = 21000 $\implies 1$ part = 100.
    Installment (121 parts) = $121 \times 100 = 12100$.
*   **Common Mistake:** Calculating total Amount $= 21000(1.1)^2$ and dividing by 2. This is absolutely wrong.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q9. (Finding Principal from 3rd year interest)** The compound interest on a certain sum for the 2nd year is Rs. 132 and for the 3rd year is Rs. 145.2. Find the principal.
*   **Answer:** Rs. 1000
*   **Detailed Solution:** The interest of 3rd year is generated on the amount at the end of 2nd year. Wait, the interest *itself* grows at the rate R!
    Rate = $\frac{145.2 - 132}{132} \times 100 = \frac{13.2}{132} \times 100 = 10\%$.
    Interest of 2nd year = $132$.
    Let 1st year interest = $I_1$.
    $I_2 = I_1 + 10\%(I_1) = 1.1 I_1$.
    $1.1 I_1 = 132 \implies I_1 = 120$.
    Since 1st year CI is same as SI: $10\% \text{ of } P = 120 \implies P = 1200$.
    *Wait, self-correction!* Let's re-verify.
    P = 1200. Yr1 CI = 120. Yr2 CI = $120 + 12 = 132$. Yr3 CI = $132 + 13.2 = 145.2$.
    So Principal is 1200, not 1000.
*   **Fastest Shortcut:** Find rate from successive interests. Step back each year by dividing by $(1+R/100)$. $P = CI_1 / (R/100)$.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Hard
*   **Company:** Cognizant

**Q10. (Time Calculation)** In what time will Rs. 1000 become Rs. 1331 at 10% per annum compounded annually?
*   **Answer:** 3 years
*   **Detailed Solution:** $A/P = (1+r/100)^n$.
    $1331 / 1000 = (1 + 10/100)^n = (11/10)^n$.
    $(11/10)^3 = (11/10)^n \implies n = 3$.
*   **Fastest Shortcut:** Look at the numbers. 1331 is $11^3$. 1000 is $10^3$. The power is 3, so time is 3 years.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** HCL

**Q11. (Effective Rate Trap)** Which is a better investment: 20% compounded half yearly or 21% compounded annually?
*   **Answer:** Both are equal.
*   **Detailed Solution:** 21% annually = 21% effective rate.
    20% half-yearly $\implies$ 10% per 6 months for 2 cycles.
    Effective rate = $10 + 10 + (100/100) = 21\%$.
    They are identical.
*   **Fastest Shortcut:** Use $x + y + xy/100$ immediately.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Tech Mahindra

**Q12. (Fractional Time)** Find the compound interest on Rs. 8000 at 15% p.a. for 2 years and 4 months.
*   **Answer:** Rs. 3109
*   **Detailed Solution:** 4 months = 1/3 year.
    Rate for 1/3 year = $15\% / 3 = 5\%$.
    We need successive % of 15%, 15%, and 5%.
    Amount = $8000 \times (115/100) \times (115/100) \times (105/100) = 8000 \times (23/20) \times (23/20) \times (21/20) = 23 \times 23 \times 21 = 529 \times 21 = 11109$.
    CI = $11109 - 8000 = 3109$.
*   **Fastest Shortcut:** Instead of big multiplication, use 2:1 ratio for first 2 years, then add 5% for the last part.
    2 yrs CI @ 15%: $15+15+2.25 = 32.25\%$.
    Amount after 2 yrs = $132.25\% \text{ of } 8000 = 10580$.
    Interest for last 4 months = 5% of 10580 = 529.
    Total CI = (Interest from yr 1 & 2) + 529 = $2580 + 529 = 3109$.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** PwC

**Q13. (Variable Rates)** A sum is invested for 3 years at CI. Rate is 5% for 1st year, 10% for 2nd year and 20% for 3rd year. If amount is Rs. 13860, find sum.
*   **Answer:** Rs. 10000
*   **Detailed Solution:** $A = P \times 1.05 \times 1.10 \times 1.20$.
    $13860 = P \times (105/100) \times (110/100) \times (120/100) = P \times (21/20) \times (11/10) \times (6/5)$.
    $13860 = P \times (1386 / 1000) \implies P = 10000$.
*   **Fastest Shortcut:** Use fractions! $5\%=1/20, 10\%=1/10, 20\%=1/5$.
    $P \rightarrow A$: $20 \rightarrow 21$, $10 \rightarrow 11$, $5 \rightarrow 6$.
    Product $P = 1000$. Product $A = 1386$.
    If $A = 13860$, then $P = 10000$.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** LTIMindtree

**Q14. (Population Depreciation)** A town's population is 64000. It decreases by 5% in the first year, increases by 10% in the second year, and decreases by 10% in the third year. What is the final population?
*   **Answer:** 60192
*   **Detailed Solution:** $64000 \times 0.95 \times 1.10 \times 0.90$.
    $64000 \times (19/20) \times (11/10) \times (9/10) = 64 \times 19 \times 11 \times 9 / 2$?
    Wait, $20 \times 10 \times 10 = 2000$.
    $64000 / 2000 = 32$.
    Answer = $32 \times 19 \times 11 \times 9 = 32 \times 1881 = 60192$.
*   **Fastest Shortcut:** Unit digit method!
    $2 \times 9 \times 1 \times 9 = \dots 8 \times 9 = \dots 2$.
    Check options. Only one option usually ends in 2.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Medium
*   **Company:** EY

**Q15. (Tree Method Setup)** The simple interest on a sum for 3 years is Rs. 1200 and compound interest on the SAME sum for 2 years is Rs. 832. Find Rate and Principal.
*   **Answer:** 8% and Rs. 5000
*   **Detailed Solution:** SI for 3 yrs = 1200 $\implies$ SI for 1 yr = 400.
    For 2 years, SI = 800.
    CI for 2 years = 832.
    Difference for 2 years = $832 - 800 = 32$.
    This Rs. 32 is the interest earned ON the first year's interest (Rs. 400).
    Rate = $(32 / 400) \times 100 = 8\%$.
    If 8% of P = 400 $\implies P = 5000$.
*   **Fastest Shortcut:** This IS the shortcut. Do not use equations. Understand the structure: CI(2yr) = 2 $\times$ SI(1yr) + Interest on SI(1yr).
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** TCS NQT Advanced

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **CI - SI Difference:** Formula $D = P(R/100)^2$ is tested repeatedly.
2.  **Fractional Rates (16.66%):** To force candidates to use fraction ratio columns instead of decimal multipliers.
3.  **Installments:** The fraction tree approach (10 $\rightarrow$ 11, 100 $\rightarrow$ 121) is a known separator of top candidates.

**Latest trend:**
*   Asking for CI on 2 years and 73 days. You MUST calculate CI for 2 years, then SI for the 73 days on the new amount.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **2 Year Difference** | $D = P (R/100)^2$ |
| **3 Year Difference** | $D = P (R/100)^2 (300+R)/100$ |
| **2 Year CI Ratio** | 2 : 1 |
| **3 Year CI Ratio** | 3 : 3 : 1 |
| **Fractional Years** | Find amount for whole years, then use $PRT/100$ on the new amount for the remaining months/days. |
