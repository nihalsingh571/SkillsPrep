# Chapter 04: Average

## 1. Importance

**Why companies ask this topic:**
Average is a core concept that tests a candidate's ability to balance values conceptually without relying on long sums. It's heavily used in Data Interpretation and reasoning puzzles.

**Expected number of questions:**
1 to 3 questions. Often mixed with Age problems or Speed problems.

**Difficulty level:**
Easy to Moderate. The difficulty comes when candidates try to multiply large numbers instead of using the "Deviation Method".

**Companies asking this topic:**
TCS NQT, Infosys, Capgemini, LTIMindtree, and DXC frequently ask "inclusion/exclusion" type average problems.

---

## 2. Quick Revision

**Core Concept:**
Average is the "equal distribution" of values. If the average age of 10 people is 20, it mathematically means everyone has 20 years.
$\text{Average} = \frac{\text{Sum of Observations}}{\text{Number of Observations}}$
$\text{Sum} = \text{Average} \times \text{Number}$

**The Deviation Method (Cheat Code):**
If a new person joins a group and the average increases, the new person brought MORE than the average.
If the average decreases, the new person brought LESS than the average.
*Rule:* Change in Total = Change in Average $\times$ Total members.

**Weighted Average:**
Used when groups of different sizes are combined.
$\text{Combined Avg} = \frac{n_1A_1 + n_2A_2}{n_1 + n_2}$

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The Inclusion/Exclusion shortcut** is the single most tested concept in Average.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Sum of Observations** | Average $\times N$ | Sum = A $\times$ N |
| **Average of first $N$ natural numbers** | $\frac{N+1}{2}$ | Just add the first and last, divide by 2. |
| **Average of first $N$ even numbers** | $N+1$ | Even is one more. |
| **Average of first $N$ odd numbers** | $N$ | Odd is exactly N. |
| **Average of consecutive numbers** | $\frac{\text{First Term} + \text{Last Term}}{2}$ | Works for ANY arithmetic progression. |
| **Inclusion (New member joins)** | $\text{Old Avg} + (\text{New } N \times \text{Increase in Avg})$ | Added value = Avg + Extra distributed. |
| **Exclusion (Member leaves)** | $\text{Old Avg} - (\text{Remaining } N \times \text{Increase in Avg})$ | Leaving value = Avg - Extra absorbed. |
| **Replacement (A replaces B)** | $\text{Weight of New} = \text{Weight of Old} + (\text{Total } N \times \text{Change})$ | Sign is + if avg increases, - if decreases. |

---

## 4. Fast Tricks

**The "Assume an Average" Trick (Deviation)**
Find the average of 87, 84, 86, 90, 82.
*Don't add them!* Assume average = 85.
Deviations: $+2, -1, +1, +5, -3$.
Sum of deviations = $+4$.
Net effect on average = $+4 / 5 = +0.8$.
Actual average = $85 + 0.8 = 85.8$.

**The Age Gap Constant Trick**
The age difference between two people ALWAYS remains constant. If A is 5 years older than B today, A will be 5 years older than B after 50 years. This simple fact solves 50% of age problems.

**The Batting Average Trick**
If a batsman's average increases by $x$ runs after his $N$th innings.
Runs scored in $N$th innings = $\text{Old Avg} + (N \times x)$.

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "Teacher's weight is added, average increases by 1 kg" | Inclusion problem. | $\text{Teacher} = \text{Old Avg} + (\text{New } N \times 1)$. |
| "A person weighing 60kg is replaced... average increases by 2kg" | Replacement problem. | $\text{New Guy} = 60 + (\text{Total } N \times 2)$. |
| "Average of 10 consecutive odd numbers is 40" | Average is the exact middle value. | The 5th and 6th numbers surround 40 (i.e. 39 and 41). |
| "Average score of boys is X, girls is Y, class is Z" | Mixing two groups. | Allegation Cross Method! |

---

## 6. Solving Framework

**Step-by-step fastest solving approach:**
1.  **Identify the change:** Did a member join, leave, or get replaced?
2.  **Calculate the "Deviation Pool":** How much total extra value was brought in or taken away? ($\text{Total } N \times \text{Change in Avg}$).
3.  **Add/Subtract to Base:** Adjust the old average by the deviation pool to find the specific person's value.

**Comparison of Methods:**
*Example: The average weight of 39 students is 40 kg. If the teacher's weight is included, the average increases by 800 grams. Find the teacher's weight.*
*   **Traditional Method:**
    Sum of students = $39 \times 40 = 1560$.
    New Sum = $40 \times 40.8 = 1632$.
    Teacher = $1632 - 1560 = 72$ kg. (Requires heavy multiplication).
*   **Placement Shortcut (Deviation):**
    Teacher brings 40kg (to maintain avg) PLUS provides 0.8kg to all 40 people (including himself).
    $\text{Teacher} = \text{Old Avg} + (\text{New Total } N \times \text{Increase})$
    $\text{Teacher} = 40 + (40 \times 0.8) = 40 + 32 = 72$ kg. (Takes 5 seconds, mental math).

> [!WARNING]
> **When NOT to use the Deviation trick:**
> If the question involves complex ratios and multiple groups joining/leaving simultaneously, use the basic $\text{Sum} = A \times N$ equation to avoid sign errors.

---

## 7. High Quality Practice Questions

**Q1. (Inclusion - Teacher joins)** The average age of a class of 30 students is 15 years. If the teacher's age is included, the average increases by 1 year. What is the teacher's age?
*   **Answer:** 46 years
*   **Detailed Solution:** Sum of students = $30 \times 15 = 450$. Sum with teacher = $31 \times 16 = 496$. Teacher = $496 - 450 = 46$.
*   **Fastest Shortcut:** Teacher = Old Avg + (New N $\times$ Increase) = $15 + (31 \times 1) = 15 + 31 = 46$.
*   **Common Mistake:** Multiplying the increase by the OLD 'N' (30) instead of the NEW 'N' (31).
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (Exclusion - Captain leaves)** The average weight of a cricket team of 11 players is 72 kg. If the captain's weight is excluded, the average weight of the remaining players decreases by 1 kg. What is the weight of the captain?
*   **Answer:** 82 kg
*   **Detailed Solution:** Old total = $11 \times 72 = 792$. New total = $10 \times 71 = 710$. Captain = $792 - 710 = 82$.
*   **Fastest Shortcut:** If excluding him causes average to DROP, he must be HEAVIER than average.
    Captain = Old Avg + (Remaining N $\times$ Decrease) = $72 + (10 \times 1) = 82$.
*   **Common Mistake:** Doing $72 - 10$ instead of $72 + 10$. If the average dropped when he left, he took extra weight with him!
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Infosys

**Q3. (Replacement)** The average weight of 8 men increases by 2.5 kg when a new man replaces one of them weighing 65 kg. What is the weight of the new man?
*   **Answer:** 85 kg
*   **Detailed Solution:** Let the sum of 7 men be S.
    $(S + 65) / 8 = A \implies S + 65 = 8A$.
    $(S + \text{New}) / 8 = A + 2.5 \implies S + \text{New} = 8A + 20$.
    Subtracting equations: $\text{New} - 65 = 20 \implies \text{New} = 85$.
*   **Fastest Shortcut:** New = Old + (Total N $\times$ Change) = $65 + (8 \times 2.5) = 65 + 20 = 85$.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q4. (Batting Average)** A batsman in his 17th innings makes a score of 85, and thereby increases his average by 3. What is his average after the 17th innings?
*   **Answer:** 37
*   **Detailed Solution:** Let old avg (16 innings) be A.
    Total runs before = $16A$.
    Total runs after = $16A + 85$.
    New average = $(16A + 85) / 17 = A + 3$.
    $16A + 85 = 17A + 51 \implies A = 34$.
    New average = $A + 3 = 37$.
*   **Fastest Shortcut:** His 85 runs did two things: provided the Old Avg, and gave $+3$ to all 17 innings.
    $85 = \text{Old Avg} + (17 \times 3) \implies \text{Old Avg} = 85 - 51 = 34$.
    New Avg = $34 + 3 = 37$.
*   **Common Mistake:** Finding the old average (34) and marking it as the answer, forgetting to add 3 for the *current* average.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q5. (Error in Reading)** The average of 50 numbers is 38. If two numbers, namely 45 and 55, are discarded, the average of the remaining numbers is:
*   **Answer:** 37.5
*   **Detailed Solution:** Total sum = $50 \times 38 = 1900$.
    Discarded sum = $45 + 55 = 100$.
    Remaining sum = $1900 - 100 = 1800$.
    Remaining numbers = 48.
    New average = $1800 / 48 = 37.5$.
*   **Fastest Shortcut:** Deviation method. The discarded numbers sum to 100.
    If they both were exactly the average (38+38=76), the new average wouldn't change.
    They took away an EXTRA $100 - 76 = 24$.
    This deficit of 24 is shared among the remaining 48 numbers.
    Drop in average = $24 / 48 = 0.5$.
    New Average = $38 - 0.5 = 37.5$.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** Cognizant

**Q6. (Consecutive Numbers)** The average of 7 consecutive numbers is 20. The largest of these numbers is:
*   **Answer:** 23
*   **Detailed Solution:** Let numbers be $x, x+1, x+2, x+3, x+4, x+5, x+6$.
    Sum = $7x + 21$.
    Average = $(7x + 21) / 7 = x + 3$.
    $x + 3 = 20 \implies x = 17$.
    Largest = $x + 6 = 23$.
*   **Fastest Shortcut:** The average of odd number of consecutive terms is EXACTLY the middle term.
    Since average is 20, the 4th term is 20.
    The sequence is: \_ \_ \_ 20 \_ \_ \_
    The next three are 21, 22, 23. Largest is 23.
*   **Common Mistake:** Using the long algebra formula.
*   **Expected Time:** 2 seconds
*   **Difficulty:** Easy
*   **Company:** Wipro

**Q7. (Weighted Average / Allegation)** The average score of boys in a class is 70 and that of girls is 85. If the average score of the whole class is 76, find the ratio of number of boys to girls.
*   **Answer:** 3:2
*   **Detailed Solution:** Let boys = B, girls = G.
    $70B + 85G = 76(B + G) \implies 70B + 85G = 76B + 76G$.
    $9G = 6B \implies B/G = 9/6 = 3/2$.
*   **Fastest Shortcut:** Allegation Cross.
    Boys (70)        Girls (85)
             Class (76)
    (85-76)=9        (76-70)=6
    Ratio = $9 : 6 = 3 : 2$.
*   **Common Mistake:** Getting the ratio backward (2:3). Remember, cross subtract!
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** IBM

**Q8. (Age Problem with Average)** The average age of a husband and wife was 23 years at the time of their marriage 5 years ago. Now, the average age of husband, wife, and child is 20 years. What is the age of the child?
*   **Answer:** 4 years
*   **Detailed Solution:** 5 years ago, sum of H + W = $23 \times 2 = 46$.
    Today, both have aged 5 years, so current sum of H + W = $46 + 5 + 5 = 56$.
    Today, average of H + W + C = 20 $\implies$ Sum = $20 \times 3 = 60$.
    Child's age = $60 - 56 = 4$ years.
*   **Fastest Shortcut:** Current average of H + W = $23 + 5 = 28$. Sum = 56. Current sum of 3 = 60. Diff = 4.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Tech Mahindra

**Q9. (Average Speed Pitfall)** A car travels from A to B at 40 km/hr and returns from B to A at 60 km/hr. Find its average speed.
*   **Answer:** 48 km/hr
*   **Detailed Solution:** Average Speed is NOT $(40+60)/2 = 50$.
    Avg Speed = Total Distance / Total Time. Let distance = D one way.
    Time 1 = D/40. Time 2 = D/60.
    Total Time = $D/40 + D/60 = (3D + 2D)/120 = 5D/120 = D/24$.
    Total Distance = 2D.
    Avg Speed = $2D / (D/24) = 48$.
*   **Fastest Shortcut:** When distances are equal, Avg Speed = $\frac{2xy}{x+y} = \frac{2 \times 40 \times 60}{40 + 60} = \frac{4800}{100} = 48$.
*   **Common Mistake:** Simply answering 50 km/hr. This is a fatal mistake in placement exams.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** PwC

**Q10. (Days of the week)** The average temperature for Monday, Tuesday, and Wednesday was 40°C. The average for Tuesday, Wednesday, and Thursday was 41°C. If Thursday's temperature was 42°C, what was Monday's temperature?
*   **Answer:** 39°C
*   **Detailed Solution:**
    Eq 1: $M + T + W = 40 \times 3 = 120$.
    Eq 2: $T + W + Th = 41 \times 3 = 123$.
    Subtract Eq 1 from Eq 2: $Th - M = 123 - 120 = 3$.
    Given $Th = 42 \implies 42 - M = 3 \implies M = 39$.
*   **Fastest Shortcut:** (Th - M) = 3 $\times$ (Diff in Avg).
    $Th - M = 3 \times (41 - 40) = 3 \times 1 = 3$.
    $42 - M = 3 \implies M = 39$.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Deloitte

**Q11. (Hostel Expenditure)** In a hostel of 35 students, if the number of students increases by 7, the expenses of the mess increase by Rs. 42 per day while the average expenditure per head diminishes by Re. 1. Find the original expenditure of the mess.
*   **Answer:** Rs. 420
*   **Detailed Solution:** Let original average = $x$. Original Total Exp = $35x$.
    New students = 42. New average = $x - 1$.
    New Total Exp = $42(x - 1)$.
    $42(x - 1) - 35x = 42 \implies 42x - 42 - 35x = 42 \implies 7x = 84 \implies x = 12$.
    Original Expenditure = $35 \times 12 = 420$.
*   **Fastest Shortcut:** Standard Equation setup. There is no simpler shortcut than the linear equation for this specific pattern because the total value AND the average both shift.
*   **Common Mistake:** Assuming the new total is $35x + 42x$ or similar equation errors.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q12. (Misread values)** The mean of 100 observations was calculated as 40. It was found later on that one of the observations was misread as 83 instead of 53. The correct mean is:
*   **Answer:** 39.7
*   **Detailed Solution:** Sum = 4000.
    Correct sum = $4000 - 83 (\text{wrong}) + 53 (\text{correct}) = 4000 - 30 = 3970$.
    Correct mean = $3970 / 100 = 39.7$.
*   **Fastest Shortcut:** Deviation: Difference = $\text{Correct} - \text{Wrong} = 53 - 83 = -30$.
    This -30 needs to be distributed over 100 items.
    Change in average = $-30 / 100 = -0.3$.
    New average = $40 - 0.3 = 39.7$.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q13. (Combining parts)** Of the 3 numbers whose average is 60, the first is 1/4th of the sum of the others. The first number is:
*   **Answer:** 36
*   **Detailed Solution:** Let numbers be A, B, C.
    $A + B + C = 60 \times 3 = 180$.
    Given $A = (1/4)(B + C) \implies 4A = B + C$.
    Substitute in first eq: $A + 4A = 180 \implies 5A = 180 \implies A = 36$.
*   **Fastest Shortcut:** Ratio method. $A : (B+C) = 1 : 4$.
    Total parts = $1 + 4 = 5$.
    Total sum = 180.
    1 part (which is A) = $180 / 5 = 36$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** HCL

**Q14. (Family members born)** The average age of a family of 5 members is 24. If the age of the youngest member is 8 years, find the average age of the family at the time of the birth of the youngest member.
*   **Answer:** 20 years
*   **Detailed Solution:** Current total sum = $5 \times 24 = 120$.
    8 years ago, sum of ages = Current sum - ($8 \text{ years} \times 5 \text{ members}$) = $120 - 40 = 80$.
    "At the time of birth", the youngest was 0 years old. There were still 4 other members.
    Wait, the question asks "average age of the family". Is it divided by 4 or 5?
    Standard placement rule: Divided by the *remaining* members (4) unless specified.
    Wait! "Average age of the family" usually means dividing by 4 if the child is just born (not counted as a whole year living member). Let's check both.
    If divided by 4: $80 / 4 = 20$.
    If divided by 5: $80 / 5 = 16$.
    Standard answer accepted in TCS/Infosys is 20. (Divided by 4 members who were alive right before birth). Let's write the solution clearly.
    Total sum 8 years ago = $120 - 40 = 80$.
    Avg = $80 / 4 = 20$.
*   **Fastest Shortcut:** Average 8 years ago for the 4 older members:
    Current average of those 4 members = $(120 - 8) / 4 = 112 / 4 = 28$.
    8 years ago, their average = $28 - 8 = 20$.
*   **Common Mistake:** Dividing 80 by 5 to get 16. The child wasn't a contributing member of the family's "average age" right *before* birth.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** Hexaware

**Q15. (Middle number of series)** Out of 9 persons, 8 persons spent Rs. 30 each for their meals. The ninth one spent Rs. 20 more than the average expenditure of all the nine. The total money spent by all of them was:
*   **Answer:** Rs. 292.50
*   **Detailed Solution:** Let average of all 9 be $x$. Total sum = $9x$.
    Sum of 8 persons = $8 \times 30 = 240$.
    9th person spent = $x + 20$.
    $240 + (x + 20) = 9x \implies 260 + x = 9x \implies 8x = 260 \implies x = 32.5$.
    Total spent = $9x = 9 \times 32.5 = 292.50$.
*   **Fastest Shortcut:** The extra Rs. 20 spent by the 9th person is essentially compensating for the deficit of the first 8 persons compared to the true average.
    Deficit per person = $20 / 8 = 2.5$.
    True average = $30 + 2.5 = 32.5$.
    Total spent = $9 \times 32.5 = 292.5$.
*   **Common Mistake:** Adding 20 to $30 \times 9$, failing to understand that the 9th person's extra spend shifts the overall average.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Hard
*   **Company:** EY

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Replacement/Inclusion:** Finding the weight of a new person (Requires Deviation method).
2.  **Misread Data:** Adjusting average when 48 is read as 84.
3.  **Temperature week:** Mon-Wed vs Tue-Thu equations.

**Latest trend:**
*   Combining averages with ratios (like Q13).
*   Testing the tricky concept of "Average of family at the time of birth".

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **New Person Joins** | $New = Old Avg + (\text{New } N \times Increase)$ |
| **Person Leaves** | $Left = Old Avg - (\text{Remaining } N \times Increase)$ |
| **Misread Number** | $New Avg = Old Avg + \frac{Correct - Wrong}{N}$ |
| **Avg Speed (Equal Dist)** | $\frac{2xy}{x+y}$ |
| **Consecutive Numbers** | The average is always the EXACT middle term. |
