# Chapter 17: Probability

## 1. Importance

**Why companies ask this topic:**
Probability tests logical counting (from Permutations and Combinations) combined with fraction evaluation. It is highly favored by product-based companies to test analytical thinking and risk assessment.

**Expected number of questions:**
1 to 3 questions.

**Difficulty level:**
Moderate to Hard. The main difficulty is identifying whether to use $AND (\times)$ or $OR (+)$ logic.

**Companies asking this topic:**
TCS NQT (Advanced section), Infosys (Puzzle section), Deloitte, IBM, EY, PwC.

---

## 2. Quick Revision

**Core Concept:**
$\text{Probability of an Event } P(E) = \frac{\text{Number of Favorable Outcomes}}{\text{Total Number of Possible Outcomes}}$
*   Probability is always between 0 and 1. ($0 \le P(E) \le 1$)
*   $P(\text{Event happening}) + P(\text{Event NOT happening}) = 1$.
*   $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.

**The AND / OR Rule:**
*   **AND ($\cap$):** Used for Independent Events. **MULTIPLY**.
    *(e.g., Draw a King AND then draw a Queen)*
*   **OR ($\cup$):** Used for Mutually Exclusive Events. **ADD**.
    *(e.g., Draw a King OR a Queen)*

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The Combination Formula ($^nC_r$)** is used in 90% of probability questions involving selecting multiple items (balls from bags, cards from decks).

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Probability Definition** | $P(E) = \frac{n(E)}{n(S)}$ | Favorable / Total |
| **Not happening** | $P(E') = 1 - P(E)$ | "At least one" = $1 - \text{None}$ |
| **Tossing $n$ coins** | Total outcomes = $2^n$ | 2 coins = 4. 3 coins = 8. |
| **Throwing $n$ dice** | Total outcomes = $6^n$ | 2 dice = 36. |
| **Drawing cards** | Total outcomes = 52 | 4 suits (Spades, Clubs, Hearts, Diamonds) |
| **Leap Year 53 Sundays** | Probability = $2/7$ | $366 = 52 \text{ weeks} + 2 \text{ odd days}$. |
| **Non-Leap Year 53 Sundays** | Probability = $1/7$ | $365 = 52 \text{ weeks} + 1 \text{ odd day}$. |

---

## 4. Fast Tricks

**The "At Least One" Trick**
"What is the probability of getting AT LEAST one Head in 3 coin tosses?"
Do NOT calculate 1 Head, 2 Heads, and 3 Heads.
Calculate NO Heads (which is all Tails: TTT).
$P(\text{No Heads}) = 1/8$.
$P(\text{At least one Head}) = 1 - 1/8 = 7/8$.

**The 2-Dice Sum Shortcut**
When throwing 2 dice, memorize the number of ways to get a specific sum:
*   Sum 2 or 12 $\implies$ 1 way
*   Sum 3 or 11 $\implies$ 2 ways
*   Sum 4 or 10 $\implies$ 3 ways
*   Sum 5 or 9 $\implies$ 4 ways
*   Sum 6 or 8 $\implies$ 5 ways
*   Sum 7 $\implies$ 6 ways (Highest probability: $6/36 = 1/6$)
*(Notice the symmetry around 7).*

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "A bag contains 3 red, 4 blue. Draw 2 balls" | Selection without replacement. | Denominator is $^7C_2$. |
| "Draw 1 card... King OR Spade" | Mutually inclusive OR. | $P(A) + P(B) - P(A \cap B)$. |
| "A speaks truth 60%, B speaks truth 70%. Contradict?" | A true AND B false, OR A false AND B true. | $(A \times B') + (A' \times B)$. |
| "A leap year selected at random" | The 2 extra days. | $2/7$ probability for any specific day. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach for "Drawing Balls/Cards":**
1.  **Find the Denominator First:** Identify total items and how many are drawn. Use $C$ (e.g., $^9C_2$).
2.  **Find the Numerator:** Use $C$ for each color/type required. Multiply if AND. Add if OR.
3.  **Evaluate Combinations:** Use the quick descending multiplication method to expand the $C$ terms.

**Comparison of Methods:**
*Example: A bag contains 4 Red and 5 Blue balls. Two balls are drawn at random. Find the probability that both are Red.*
*   **Traditional Method (Event by Event):**
    Draw 1: $P(\text{Red}) = 4/9$.
    Draw 2: Bag now has 3 Red, 8 Total. $P(\text{Red}) = 3/8$.
    $P = (4/9) \times (3/8) = 12/72 = 1/6$.
*   **Placement Shortcut (Combination Method):**
    Denominator: Total ways to draw 2 balls from 9 = $^9C_2 = (9 \times 8)/2 = 36$.
    Numerator: Ways to draw 2 Red from 4 Red = $^4C_2 = (4 \times 3)/2 = 6$.
    Probability = $6/36 = 1/6$.
    *(Both methods are fast, but the Combination method is vastly superior when drawing 3 or more balls).*

> [!WARNING]
> **"With Replacement" vs "Without Replacement":**
> If the question says "A ball is drawn, *replaced*, and then another is drawn", the denominator remains the same for both draws (e.g., $4/9 \times 4/9$). This is rare in placements. By default, always assume WITHOUT replacement (using Combinations).

---

## 7. High Quality Practice Questions

**Q1. (Coins Basic)** Two coins are tossed simultaneously. What is the probability of getting exactly one head?
*   **Answer:** 1/2
*   **Detailed Solution:** Sample space = {HH, HT, TH, TT}. Total = 4.
    Favorable (Exactly one head) = {HT, TH}. Total = 2.
    $P = 2/4 = 1/2$.
*   **Fastest Shortcut:** Write down the small sample space mentally.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (Coins At Least One)** Three coins are tossed. Find the probability of getting at least one tail.
*   **Answer:** 7/8
*   **Detailed Solution:** Total outcomes = $2^3 = 8$.
    At least one tail = 1 - P(No tails).
    No tails means all Heads (HHH). There is only 1 way.
    $P(\text{No tails}) = 1/8$.
    $P(\text{At least one tail}) = 1 - 1/8 = 7/8$.
*   **Fastest Shortcut:** This is the standard "At least one" trick.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Infosys

**Q3. (Dice Sum)** Two dice are thrown simultaneously. What is the probability of getting a sum of 9?
*   **Answer:** 1/9
*   **Detailed Solution:** Total outcomes = $6 \times 6 = 36$.
    Favorable sums for 9: (3,6), (4,5), (5,4), (6,3). Total = 4 ways.
    $P = 4/36 = 1/9$.
*   **Fastest Shortcut:** Use the Dice Sum memory trick! Sum of 9 $\implies$ 4 ways. Directly write 4/36.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Wipro

**Q4. (Dice Doublet)** Two dice are thrown. Find the probability of getting a doublet or a sum of 10.
*   **Answer:** 2/9
*   **Detailed Solution:** Total = 36.
    Doublets: (1,1), (2,2), (3,3), (4,4), (5,5), (6,6). Total = 6.
    Sum 10: (4,6), (5,5), (6,4). Total = 3.
    Notice (5,5) is counted in both!
    By formula: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.
    Favorable = $6 + 3 - 1 = 8$.
    $P = 8/36 = 2/9$.
*   **Fastest Shortcut:** Just list and count carefully without duplicates: (1,1), (2,2), (3,3), (4,4), (6,6), (4,6), (6,4), (5,5). That's 8.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q5. (Cards OR logic)** One card is drawn at random from a pack of 52 cards. What is the probability that the card is either a King or a Spade?
*   **Answer:** 4/13
*   **Detailed Solution:** Total cards = 52.
    Kings = 4. Spades = 13.
    King of Spades is counted twice!
    Favorable = Kings + Spades - (King of Spades) = $4 + 13 - 1 = 16$.
    $P = 16/52 = 4/13$.
*   **Fastest Shortcut:** Set logic. $n(A) + n(B) - n(A \cap B)$.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Accenture

**Q6. (Cards Without Replacement)** Two cards are drawn together from a pack of 52 cards. The probability that one is a spade and one is a heart, is:
*   **Answer:** 13/102
*   **Detailed Solution:**
    Denominator = $^{52}C_2 = (52 \times 51) / 2 = 1326$.
    Numerator = 1 Spade AND 1 Heart = $^{13}C_1 \times ^{13}C_1 = 13 \times 13 = 169$.
    $P = 169 / 1326 = 13 / 102$.
*   **Alternative Method:**
    Draw 1 Spade then 1 Heart: $(13/52) \times (13/51)$.
    OR Draw 1 Heart then 1 Spade: $(13/52) \times (13/51)$.
    Total = $2 \times (1/4) \times (13/51) = 13/102$.
*   **Fastest Shortcut:** The event-by-event method with the $\times 2$ multiplier for arrangement is often faster to calculate than large combinations.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

**Q7. (Balls Selection AND)** A bag contains 2 red, 3 green and 2 blue balls. Two balls are drawn at random. What is the probability that none of the balls drawn is blue?
*   **Answer:** 10/21
*   **Detailed Solution:** Total balls = $2 + 3 + 2 = 7$.
    Denominator = $^7C_2 = (7 \times 6) / 2 = 21$.
    "None is blue" means both balls must be drawn from the Red + Green pool.
    Red + Green pool = $2 + 3 = 5$ balls.
    Numerator = $^5C_2 = (5 \times 4) / 2 = 10$.
    $P = 10 / 21$.
*   **Fastest Shortcut:** Treat the "Not Blue" balls as a single valid pool. Draw from that pool.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** IBM

**Q8. (Balls Selection Same Color)** A box contains 4 red, 5 green, and 6 white balls. Two balls are drawn. What is the probability that they are of the same color?
*   **Answer:** 31/105
*   **Detailed Solution:** Total = 15.
    Denominator = $^{15}C_2 = (15 \times 14) / 2 = 105$.
    "Same color" means (2 Red) OR (2 Green) OR (2 White).
    Numerator = $^4C_2 + ^5C_2 + ^6C_2$.
    $= 6 + 10 + 15 = 31$.
    $P = 31 / 105$.
*   **Fastest Shortcut:** Standard Combination OR logic. Calculate combinations mentally.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** Cognizant

**Q9. (Contradiction/Truth logic)** A speaks truth in 75% of cases and B in 80% of cases. In what percentage of cases are they likely to contradict each other, narrating the same incident?
*   **Answer:** 35%
*   **Detailed Solution:**
    $P(A) = 3/4$, $P(A') = 1/4$.
    $P(B) = 4/5$, $P(B') = 1/5$.
    Contradict means: (A is true AND B is false) OR (A is false AND B is true).
    $= P(A) \times P(B') + P(A') \times P(B)$.
    $= (3/4 \times 1/5) + (1/4 \times 4/5)$.
    $= 3/20 + 4/20 = 7/20$.
    Percentage = $(7/20) \times 100 = 35\%$.
*   **Fastest Shortcut:** This IS the standard approach. Just remember to cross-multiply the truth/lie probabilities.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q10. (Hitting Target)** The probability that A hits a target is 1/3 and the probability that B hits it is 2/5. What is the probability that the target will be hit, if both shoot at it?
*   **Answer:** 3/5
*   **Detailed Solution:** "Target will be hit" means AT LEAST ONE person hits it.
    It's faster to find the probability that NO ONE hits it, and subtract from 1.
    $P(\text{A misses}) = 1 - 1/3 = 2/3$.
    $P(\text{B misses}) = 1 - 2/5 = 3/5$.
    $P(\text{Both miss}) = (2/3) \times (3/5) = 2/5$.
    $P(\text{Target hit}) = 1 - 2/5 = 3/5$.
*   **Alternative:** $P(A \cup B) = P(A) + P(B) - P(A \cap B) = 1/3 + 2/5 - (1/3 \times 2/5) = 5/15 + 6/15 - 2/15 = 9/15 = 3/5$.
*   **Fastest Shortcut:** The "Nobody hits it" reverse method is universally safer and faster.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** EY

**Q11. (Leap Year Sundays)** What is the probability that a leap year, selected at random, will contain 53 Sundays?
*   **Answer:** 2/7
*   **Detailed Solution:** Leap year = 366 days.
    $366 / 7 = 52$ weeks and 2 extra days.
    52 weeks guarantee 52 Sundays.
    The 2 extra days can be:
    (Sun, Mon), (Mon, Tue), (Tue, Wed), (Wed, Thu), (Thu, Fri), (Fri, Sat), (Sat, Sun).
    Total combinations = 7.
    Favorable (containing Sunday) = (Sun, Mon) and (Sat, Sun). Total = 2.
    Probability = 2/7.
*   **Fastest Shortcut:** Leap year = 2/7. Non-leap year = 1/7. Just memorize it.
*   **Expected Time:** 2 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q12. (Defective Bulbs)** A box contains 20 electric bulbs, out of which 4 are defective. Two bulbs are chosen at random from this box. The probability that at least one of these is defective is:
*   **Answer:** 7/19
*   **Detailed Solution:** Total = 20. Defective = 4. Non-defective = 16.
    "At least one defective" = $1 - P(\text{None are defective})$.
    "None are defective" means both are drawn from the 16 good bulbs.
    $P(\text{None}) = ^{16}C_2 / ^{20}C_2 = \frac{16 \times 15 / 2}{20 \times 19 / 2} = \frac{120}{190} = 12/19$.
    $P(\text{At least one}) = 1 - 12/19 = 7/19$.
*   **Fastest Shortcut:** The $1 - P(\text{None})$ trick saves you from calculating $(1D, 1G) + (2D, 0G)$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** PwC

**Q13. (Tickets)** Tickets numbered 1 to 20 are mixed up and then a ticket is drawn at random. What is the probability that the ticket drawn has a number which is a multiple of 3 or 5?
*   **Answer:** 9/20
*   **Detailed Solution:** Total = 20.
    Multiples of 3: {3, 6, 9, 12, 15, 18} (6 outcomes).
    Multiples of 5: {5, 10, 15, 20} (4 outcomes).
    Multiple of BOTH (LCM of 3 and 5 = 15): {15} (1 outcome).
    $P(A \cup B) = P(A) + P(B) - P(A \cap B)$.
    Favorable = $6 + 4 - 1 = 9$.
    $P = 9/20$.
*   **Fastest Shortcut:** Count the sets mentally. Don't forget to subtract the common multiples!
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Tech Mahindra

**Q14. (Conditional Replacement)** A bag contains 5 red and 3 green balls. Another bag contains 4 red and 6 green balls. If one ball is drawn from each bag, find the probability that both are red.
*   **Answer:** 1/4
*   **Detailed Solution:** These are two independent events.
    Bag 1: $P(\text{Red}) = 5/8$.
    Bag 2: $P(\text{Red}) = 4/10 = 2/5$.
    Both are Red = $P(\text{Red from 1}) \text{ AND } P(\text{Red from 2})$.
    $P = (5/8) \times (2/5) = 10 / 40 = 1/4$.
*   **Fastest Shortcut:** Multiply independent probabilities directly.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** HCL

**Q15. (Words arrangement Probability)** If the letters of the word 'APPLE' are arranged randomly, what is the probability that the vowels are together?
*   **Answer:** 2/5
*   **Detailed Solution:** This is a P&C question masquerading as Probability.
    Total arrangements of APPLE = $5! / 2! = 60$. (Denominator).
    Vowels together: Tie 'A' and 'E' into a block.
    Letters to arrange = P, P, L, [AE]. Total 4 blocks.
    Arrangements = $4! / 2!$ (for repeating P) $= 12$.
    Internal arrangement of [AE] = $2! = 2$.
    Favorable arrangements = $12 \times 2 = 24$. (Numerator).
    $P = 24 / 60 = 2 / 5$.
*   **Fastest Shortcut:** Do the P&C steps cleanly to avoid numerator/denominator confusion.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Balls from Bags:** $^nC_r$ logic without replacement.
2.  **Dice Sums:** Sum of 2 dice is a staple in Wipro and Capgemini.
3.  **Truth/Lie Contradiction:** Classic TCS Advanced question.

**Latest trend:**
*   Mixing P&C with Probability (like Q15) to test two chapters in a single question.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **AND logic** | Independent. MULTIPLY probabilities. |
| **OR logic** | Mutually Exclusive. ADD probabilities. |
| **At least one** | $1 - P(\text{None})$. Absolute time saver. |
| **Drawing 2+ items** | Use $^nC_r$ to calculate total and favorable ways. |
| **Leap Year 53 days** | 2/7 probability for any day. |
