# Chapter 21: LCM and HCF

## 1. Importance

**Why companies ask this topic:**
LCM and HCF test basic divisibility logic. This topic is frequently disguised as "Bells ringing together", "Traffic lights changing", or "Finding the largest tile to fit a floor".

**Expected number of questions:**
1 to 2 questions.

**Difficulty level:**
Easy. The calculations are simple once you identify whether the question requires an LCM (finding a common multiple in the future) or an HCF (finding the largest common divisor).

**Companies asking this topic:**
Infosys, TCS NQT, Wipro, Capgemini, LTIMindtree.

---

## 2. Quick Revision

**Core Concept:**
*   **LCM (Least Common Multiple):** The smallest number that is a multiple of all given numbers. Used when things need to *meet* or *sync up* in the future.
*   **HCF (Highest Common Factor / GCD):** The largest number that perfectly divides all given numbers. Used when things need to be *split* or *measured* evenly.

**Prime Factorization Method:**
*   **HCF:** Product of the lowest powers of common prime factors.
*   **LCM:** Product of the highest powers of all prime factors.

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The Product Formula** ($\text{LCM} \times \text{HCF} = A \times B$) is the most frequently tested formula in this chapter.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Product Rule** | $\text{LCM} \times \text{HCF} = \text{Product of Two Numbers}$ | ONLY works for TWO numbers. |
| **Fractions (LCM)** | $\frac{\text{LCM of Numerators}}{\text{HCF of Denominators}}$ | The requested operation is applied to the Numerator. |
| **Fractions (HCF)** | $\frac{\text{HCF of Numerators}}{\text{LCM of Denominators}}$ | |
| **Decimals** | Make decimal places equal, find LCM/HCF, restore decimals. | e.g. 1.2, 0.24 $\implies$ 120, 24. |
| **Co-prime numbers** | $\text{HCF} = 1$, $\text{LCM} = \text{Product of numbers}$ | Consecutive numbers are always co-prime. |

---

## 4. Fast Tricks

**The "Difference Trick" for HCF**
The HCF of two numbers can NEVER be greater than their difference. It is either the difference itself or a factor of the difference.
Example: HCF of 48 and 64.
Difference = $64 - 48 = 16$.
Does 16 divide 48? Yes. Does it divide 64? Yes.
So, HCF = 16. (Zero prime factorization needed).

**The "Option Elimination" Trick for LCM**
If a question asks for the LCM of 12, 15, 20, 27.
Look at 27. It is a multiple of 9. Therefore, the LCM MUST be a multiple of 9.
Check the options. Use the "Sum of digits" divisibility rule for 9. Usually, only one option will be divisible by 9. Pick it and move on.

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "Bells ringing together", "Runners meeting" | Finding a future synchronized time. | Find **LCM**. |
| "Largest size of square tiles", "Maximum capacity" | Dividing space/liquid evenly. | Find **HCF**. |
| "Leaves remainder $R$ in each case" (Largest Num)| $(N_1 - R)$, $(N_2 - R)$, find HCF. | Subtract remainder FIRST, then HCF. |
| "Leaves remainder $R$ in each case" (Smallest Num)| LCM of numbers, then $+ R$. | Find LCM FIRST, then add remainder. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach for "Remainder" questions:**
1.  **Read "Smallest" vs "Largest":** Smallest $\implies$ LCM. Largest $\implies$ HCF.
2.  **For LCM (Smallest number leaving remainder $R$):** Find LCM of divisors. Then add $R$. $\text{Ans} = \text{LCM} + R$.
3.  **For HCF (Largest number leaving remainder $R$):** Subtract $R$ from the numbers first. Then find HCF. $\text{Ans} = \text{HCF}(N_1-R_1, N_2-R_2)$.

**Comparison of Methods:**
*Example: Find the greatest number that will divide 43, 91 and 183 so as to leave the same remainder in each case.*
*   **Traditional Method:**
    Let number be $x$, remainder be $r$.
    $43 = ax + r$, $91 = bx + r$, $183 = cx + r$.
    Subtract equations... Takes 3 minutes to set up.
*   **Placement Shortcut (The Difference Method):**
    Take differences of the given numbers:
    $91 - 43 = 48$.
    $183 - 91 = 92$.
    $183 - 43 = 140$.
    Find HCF of differences: HCF(48, 92, 140).
    Difference between 92 and 48 = 44. Factors of 44: 4, 11, 22, 44.
    4 divides all of them perfectly. So HCF = **4**. (Takes 20 seconds).

> [!WARNING]
> **The 3 Number Trap:**
> The formula $\text{LCM} \times \text{HCF} = A \times B$ is strictly for TWO numbers. It fails for 3 or more numbers. Do NOT use $\text{LCM} \times \text{HCF} = A \times B \times C$.

---

## 7. High Quality Practice Questions

**Q1. (Basic LCM/HCF Product)** The HCF of two numbers is 11 and their LCM is 7700. If one of the numbers is 275, then the other is:
*   **Answer:** 308
*   **Detailed Solution:** $\text{LCM} \times \text{HCF} = A \times B$.
    $7700 \times 11 = 275 \times B$.
    $B = (7700 \times 11) / 275 = 7700 / 25 = 308$.
*   **Fastest Shortcut:** Just apply the formula.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (Bells Ringing)** Six bells commence tolling together and toll at intervals of 2, 4, 6, 8, 10 and 12 seconds respectively. In 30 minutes, how many times do they toll together?
*   **Answer:** 16
*   **Detailed Solution:** "Together" means LCM.
    LCM(2, 4, 6, 8, 10, 12) = 120 seconds = 2 minutes.
    They toll together every 2 minutes.
    In 30 minutes: $30 / 2 = 15$ times.
    *Wait, don't forget the first toll at $T=0$!*
    Total = $15 + 1 = 16$ times.
*   **Fastest Shortcut:** $(\text{Total Time} / \text{LCM}) + 1$.
*   **Common Mistake:** Forgetting to add the +1 for the starting toll.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** Infosys

**Q3. (Fractions)** The LCM of 2/3, 4/9, 5/6 is:
*   **Answer:** 20/3
*   **Detailed Solution:** LCM of fractions = $\frac{\text{LCM of Numerators}}{\text{HCF of Denominators}}$.
    LCM of (2, 4, 5) = 20.
    HCF of (3, 9, 6) = 3.
    Answer = 20/3.
*   **Fastest Shortcut:** Use the formula directly.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Wipro

**Q4. (Largest tile size)** Find the greatest possible length which can be used to measure exactly the lengths 4 m 95 cm, 9 m and 16 m 65 cm.
*   **Answer:** 45 cm
*   **Detailed Solution:** Convert to cm first.
    Lengths: 495, 900, 1665.
    "Greatest possible length" means HCF.
    Find HCF(495, 900, 1665).
    Difference(900, 495) = 405.
    Factors of 405 ending in 5: 45, 81.
    Check 45: $495/45 = 11$. $900/45 = 20$. $1665/45 = 37$.
    It works. HCF = 45 cm.
*   **Fastest Shortcut:** Option elimination using divisibility. If options are 15, 25, 35, 45. Try dividing by 9 (sum of digits for 495 is 18). So 45 must be the factor.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q5. (Smallest Remainder)** Find the least number which when divided by 6, 7, 8, 9, and 12 leaves the same remainder 1 in each case.
*   **Answer:** 505
*   **Detailed Solution:** "Least" means LCM.
    LCM(6, 7, 8, 9, 12) = 504.
    Add remainder 1 $\implies 504 + 1 = 505$.
*   **Fastest Shortcut:** Option elimination. Subtract 1 from the options and check which one is divisible by 9 and 8.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q6. (Greatest Remainder - Same)** Find the greatest number that will divide 43, 91 and 183 so as to leave the same remainder in each case.
*   **Answer:** 4
*   **Detailed Solution:** (From Solving Framework).
    Differences: $91-43 = 48$. $183-91 = 92$. $183-43 = 140$.
    HCF(48, 92, 140) = 4.
*   **Fastest Shortcut:** HCF of differences.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** Deloitte

**Q7. (Greatest Remainder - Different)** Find the greatest number which on dividing 1657 and 2037 leaves remainders 6 and 5 respectively.
*   **Answer:** 127
*   **Detailed Solution:** "Greatest" means HCF.
    Subtract remainders FIRST:
    $1657 - 6 = 1651$.
    $2037 - 5 = 2032$.
    Find HCF(1651, 2032).
    Difference = $2032 - 1651 = 381$.
    Factors of 381: $3 \times 127$.
    Since 1651 is not divisible by 3 (sum of digits 13), HCF must be 127.
*   **Fastest Shortcut:** Subtract remainder $\implies$ Take difference $\implies$ Factorize difference.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** IBM

**Q8. (Ratio and HCF)** Two numbers are in the ratio 3 : 4 and their HCF is 4. Their LCM is:
*   **Answer:** 48
*   **Detailed Solution:** Let numbers be $3x$ and $4x$.
    Their HCF is $x$. So $x = 4$.
    Numbers are $3(4) = 12$ and $4(4) = 16$.
    LCM of 12 and 16 = 48.
*   **Fastest Shortcut:** If numbers are ratio $a:b$, LCM = $a \times b \times \text{HCF}$.
    LCM = $3 \times 4 \times 4 = 48$.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Cognizant

**Q9. (Co-prime product)** The product of two co-prime numbers is 117. Their LCM should be:
*   **Answer:** 117
*   **Detailed Solution:** By definition, co-prime numbers have an HCF of 1.
    $\text{LCM} \times \text{HCF} = \text{Product}$.
    $\text{LCM} \times 1 = 117 \implies \text{LCM} = 117$.
*   **Fastest Shortcut:** Pure theory definition.
*   **Expected Time:** 2 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q10. (Circular Track)** A, B and C start at the same time in the same direction to run around a circular stadium. A completes a round in 252 seconds, B in 308 seconds and c in 198 seconds, all starting at the same point. After what time will they again at the starting point?
*   **Answer:** 46 minutes 12 seconds
*   **Detailed Solution:** "Meet again" means LCM.
    LCM(252, 308, 198).
    $252 = 2^2 \times 3^2 \times 7$.
    $308 = 2^2 \times 7 \times 11$.
    $198 = 2 \times 3^2 \times 11$.
    LCM = $2^2 \times 3^2 \times 7 \times 11 = 4 \times 9 \times 7 \times 11 = 2772$ seconds.
    Convert to minutes: $2772 / 60 = 46$ minutes and 12 seconds.
*   **Fastest Shortcut:** Factorization is the only way here.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** EY

**Q11. (Traffic Lights)** Three different traffic lights change after every 48 sec, 72 sec and 108 sec. If they all change simultaneously at 8:20:00 hrs, then at what time will they again change simultaneously?
*   **Answer:** 8:27:12 hrs
*   **Detailed Solution:** LCM(48, 72, 108).
    LCM = 432 seconds.
    Convert to minutes: $432 / 60 = 7$ minutes and 12 seconds.
    Time = 8:20:00 + 7 mins 12 secs = 8:27:12.
*   **Fastest Shortcut:** Use prime factorization or difference method for LCM.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Medium
*   **Company:** PwC

**Q12. (Smallest multiple with remainder)** Find the least multiple of 23, which when divided by 18, 21 and 24 leaves remainders 7, 10 and 13 respectively.
*   **Answer:** 3013
*   **Detailed Solution:**
    Divisors: 18, 21, 24.
    Remainders: 7, 10, 13.
    Notice the difference between Divisor and Remainder is constant:
    $18-7 = 11$, $21-10 = 11$, $24-13 = 11$.
    Let $K = 11$.
    Number format: $(\text{LCM of Divisors} \times n) - K$.
    LCM(18, 21, 24) = 504.
    Number = $504n - 11$.
    We need this number to be a multiple of 23.
    Test $n=1$: $504(1) - 11 = 493$. $493 / 23 = 21.4$ (Not divisible).
    Test $n=2$: $504(2) - 11 = 997$. $997 / 23 = 43.3$ (Not divisible).
    Test $n=6$: $504(6) - 11 = 3024 - 11 = 3013$.
    $3013 / 23 = 131$. (Divisible!).
*   **Fastest Shortcut:** Instead of manual testing, divide options by 23! Only one will be perfectly divisible.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q13. (Product of two numbers)** The product of two numbers is 4107. If the HCF of these numbers is 37, then the greater number is:
*   **Answer:** 111
*   **Detailed Solution:** Let the numbers be $37a$ and $37b$ (since HCF is 37, they must be multiples of 37, where $a,b$ are co-prime).
    $37a \times 37b = 4107$.
    $a \times b = 4107 / (37 \times 37) = 4107 / 1369 = 3$.
    Since $a \times b = 3$ and they are co-prime, the pairs are (1, 3).
    The numbers are $37 \times 1 = 37$, and $37 \times 3 = 111$.
    The greater number is 111.
*   **Fastest Shortcut:** $ab = \text{Product} / \text{HCF}^2$.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** HCL

**Q14. (Sum of numbers and HCF)** The sum of two numbers is 528 and their HCF is 33. The number of pairs of numbers satisfying the above conditions is:
*   **Answer:** 4
*   **Detailed Solution:** Let numbers be $33a$ and $33b$.
    $33a + 33b = 528 \implies a + b = 528 / 33 = 16$.
    Pairs of $(a,b)$ that add to 16 AND are co-prime:
    (1, 15) - Yes
    (2, 14) - No (div by 2)
    (3, 13) - Yes
    (4, 12) - No
    (5, 11) - Yes
    (6, 10) - No
    (7, 9) - Yes
    (8, 8) - No
    Total pairs = 4.
*   **Fastest Shortcut:** Find sum of co-prime ratios. List odd pairs that sum to target and eliminate multiples.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Hard
*   **Company:** Tech Mahindra

**Q15. (Square tiles)** Find the least number of square tiles required to pave the ceiling of a room 15 m 17 cm long and 9 m 2 cm broad.
*   **Answer:** 814
*   **Detailed Solution:** $L = 1517$ cm. $B = 902$ cm.
    To use the LEAST number of tiles, the tile must be of the LARGEST possible size.
    Largest tile size = HCF(1517, 902).
    Difference = $1517 - 902 = 615$.
    Factors of 615: $5 \times 123 = 5 \times 3 \times 41$.
    Check 41: $1517 / 41 = 37$. $902 / 41 = 22$. It works. HCF = 41 cm.
    Tile size = $41 \times 41$.
    Number of tiles = Total Area / Tile Area = $(1517 \times 902) / (41 \times 41) = 37 \times 22 = 814$.
*   **Fastest Shortcut:** Number of tiles = $(\text{Length} / \text{HCF}) \times (\text{Breadth} / \text{HCF})$.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** IBM

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Bells/Traffic Lights:** The classic LCM application.
2.  **Product Formula:** $\text{LCM} \times \text{HCF} = A \times B$.
3.  **Same Remainder:** Finding the HCF of the differences.

**Latest trend:**
*   Mixing HCF logic with ratios (like Q13 and Q14) where you must define the numbers as $Hx$ and $Hy$.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **Bells/Runners Sync** | Find LCM. Add 1 for the starting bell toll. |
| **Fractions** | LCM = $\frac{\text{LCM Num}}{\text{HCF Den}}$. HCF = $\frac{\text{HCF Num}}{\text{LCM Den}}$. |
| **HCF Difference trick** | HCF is always a factor of the difference between numbers. |
| **Least num leaving same $R$** | LCM + $R$. |
| **Greatest num leaving same $R$**| HCF of differences between the numbers. |
