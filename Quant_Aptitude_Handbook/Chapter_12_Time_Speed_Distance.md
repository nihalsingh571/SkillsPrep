# Chapter 12: Time Speed Distance

## 1. Importance

**Why companies ask this topic:**
Time, Speed, and Distance (TSD) tests a candidate's ability to handle proportional logic and unit conversions. It forms the base for Trains and Boats & Streams.

**Expected number of questions:**
2 to 3 questions. It is a massive scoring area.

**Difficulty level:**
Moderate to Hard. The primary difficulty is remembering to convert km/hr to m/s before multiplying.

**Companies asking this topic:**
TCS NQT, Infosys, IBM, Accenture, Wipro, LTIMindtree.

---

## 2. Quick Revision

**Core Concept:**
$\text{Distance} = \text{Speed} \times \text{Time}$

**Unit Conversions (Mandatory!):**
*   **km/hr to m/s:** Multiply by $5/18$
*   **m/s to km/hr:** Multiply by $18/5$

**Proportionality Rules:**
1.  **Distance is Constant:** Speed $\propto 1/Time$. (If you go twice as fast, you take half the time).
2.  **Time is Constant:** Distance $\propto Speed$. (If you drive for 2 hours, the faster car covers more distance).
3.  **Speed is Constant:** Distance $\propto Time$.

**Average Speed:**
Average Speed is NEVER $(S_1 + S_2) / 2$.
$\text{Average Speed} = \frac{\text{Total Distance}}{\text{Total Time}}$

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The "Early/Late" formula** solves the most common TSD question in 5 seconds.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Basic Equation** | $D = S \times T$ | DST Triangle |
| **km/hr $\leftrightarrow$ m/s** | $km/hr \times (5/18) = m/s$ | $18 \text{ km/hr} = 5 \text{ m/s}$. |
| **Avg Speed (Equal Distances)** | $\frac{2xy}{x+y}$ | Use for round trips. |
| **Avg Speed (3 Equal Distances)** | $\frac{3xyz}{xy + yz + zx}$ | Rare, but good to know. |
| **Early/Late Distance Trick** | $D = \frac{S_1 \times S_2}{S_1 \sim S_2} \times \Delta T$ | Product/Difference $\times$ Time gap. |
| **Meeting after starting (Cross)** | $S_A / S_B = \sqrt{T_B / T_A}$ | Only if they meet and continue. |
| **Gunshot / Sound trick** | $D = S_{sound} \times \Delta T$ | Relative speed of sound vs train. |

---

## 4. Fast Tricks

**The 18:5 Ratio Table**
Memorize the multiples:
$18 \text{ km/hr} = 5 \text{ m/s}$
$36 \text{ km/hr} = 10 \text{ m/s}$
$54 \text{ km/hr} = 15 \text{ m/s}$
$72 \text{ km/hr} = 20 \text{ m/s}$
$90 \text{ km/hr} = 25 \text{ m/s}$

**The Early/Late Shortcut**
If you walk at 4 km/hr, you are 10 mins late. At 5 km/hr, you are 5 mins early. Find Distance.
$D = \frac{4 \times 5}{5 - 4} \times \frac{15}{60}$ (Time gap is 15 mins, converted to hours).
$D = 20 / 1 \times 1/4 = 5$ km!

**The Fractional Speed Trick**
"Walking at 3/4 of his usual speed, a man is 20 minutes late."
Time taken = Inverse of Speed = 4/3 of usual time.
Extra time = $4/3 - 1 = 1/3$ of usual time.
$1/3$ of Usual Time = 20 mins $\implies$ Usual Time = 60 mins.

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "A goes to B at X and returns at Y" | Equal Distances. | Avg Speed = $2xy / (x+y)$. |
| "If he walks at 5 km/hr... misses train by 7 min" | Early/Late pattern. | $\Delta T \times (S_1 \times S_2) / \Delta S$. |
| "Walking at 5/6 of usual speed" | Speed ratio 5:6. Time ratio 6:5. | Time gap = 1 unit. |
| "Two trains leave at same time... after meeting take 4 hr and 9 hr" | Post-meeting time formula. | $S_1 / S_2 = \sqrt{T_2 / T_1}$. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach:**
1.  **Check Units First:** Make sure Distances are in meters if Time is in seconds. Convert km/hr to m/s immediately.
2.  **Identify the Constant:** Is Distance equal? (Use $S_1 T_1 = S_2 T_2$). Is Time equal?
3.  **Apply Ratio:** If Distance is constant, the ratio of speeds is the inverse of the ratio of times.

**Comparison of Methods:**
*Example: A student goes to school at 2.5 km/hr and reaches 6 minutes late. If he travels at 3 km/hr, he is 10 minutes early. Find the distance.*
*   **Traditional Method:**
    Let distance be $D$. Let exact time be $T$.
    $D / 2.5 = T + 6/60$.
    $D / 3 = T - 10/60$.
    Subtract: $D/2.5 - D/3 = 16/60$.
    $D(3 - 2.5)/7.5 = 16/60 \implies D(0.5)/7.5 = 16/60 \implies D = (16/60) \times 15 = 4$ km.
*   **Placement Shortcut (Formula):**
    $D = \frac{2.5 \times 3}{3 - 2.5} \times \frac{16}{60} = \frac{7.5}{0.5} \times \frac{16}{60} = 15 \times \frac{16}{60} = \frac{240}{60} = 4$ km. (10 seconds!).

> [!WARNING]
> **When NOT to use the $\frac{2xy}{x+y}$ formula:**
> Do NOT use this if the time traveled at each speed is equal instead of the distance. If you travel 1 hour at 40 km/hr and 1 hour at 60 km/hr, the average speed IS $(40+60)/2 = 50$ km/hr.

---

## 7. High Quality Practice Questions

**Q1. (Basic Conversion)** An athlete runs 200 meters in 24 seconds. His speed in km/hr is:
*   **Answer:** 30 km/hr
*   **Detailed Solution:** Speed in m/s = $200 / 24 = 25 / 3$ m/s.
    Speed in km/hr = $(25 / 3) \times (18 / 5) = 5 \times 6 = 30$ km/hr.
*   **Fastest Shortcut:** Use $18/5$ multiplier.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (Fractional Speed)** Walking at 3/4 of his usual speed, a man is $1 \frac{1}{2}$ hours late. His usual time to cover the journey is:
*   **Answer:** 4.5 hours
*   **Detailed Solution:** Speed Ratio = 3 : 4 (New : Usual).
    Time Ratio = 4 : 3 (New : Usual).
    Difference in parts = $4 - 3 = 1$ part.
    1 part = 1.5 hours.
    Usual time = 3 parts = $3 \times 1.5 = 4.5$ hours.
*   **Fastest Shortcut:** $Usual Time = \frac{Numerator}{Denominator - Numerator} \times \text{Late Time} = \frac{3}{4-3} \times 1.5 = 3 \times 1.5 = 4.5$.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Infosys

**Q3. (Early/Late Trick)** If a boy walks from his house to school at the rate of 4 km/hr, he reaches the school 10 minutes earlier than the scheduled time. However, if he walks at 3 km/hr, he reaches 10 minutes late. Find the distance of his school from his house.
*   **Answer:** 4 km
*   **Detailed Solution:** $D = \frac{S_1 S_2}{S_1 - S_2} \times \frac{\Delta T}{60}$.
    $\Delta T = 10 \text{ early} + 10 \text{ late} = 20$ mins.
    $D = \frac{4 \times 3}{4 - 3} \times \frac{20}{60} = 12 \times \frac{1}{3} = 4$ km.
*   **Fastest Shortcut:** Just plug into the formula.
*   **Common Mistake:** Subtracting the times ($10 - 10 = 0$) instead of adding the gap.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Wipro

**Q4. (Average Speed Equal Distances)** A car travels from P to Q at 30 km/hr and returns from Q to P at 40 km/hr. Find its average speed for the entire journey.
*   **Answer:** 34.28 km/hr
*   **Detailed Solution:** Avg Speed = $2xy / (x+y)$.
    $= 2(30)(40) / (30+40) = 2400 / 70 = 240 / 7 = 34.28$ km/hr.
*   **Fastest Shortcut:** $2xy / (x+y)$.
*   **Common Mistake:** $(30+40)/2 = 35$ km/hr.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q5. (Average Speed Different Distances)** A man travels 600 km by train at 80 km/hr, 800 km by ship at 40 km/hr, 500 km by plane at 400 km/hr and 100 km by car at 50 km/hr. What is the average speed?
*   **Answer:** $65 \frac{5}{11}$ km/hr
*   **Detailed Solution:** Total Distance = $600 + 800 + 500 + 100 = 2000$ km.
    Total Time = $(600/80) + (800/40) + (500/400) + (100/50)$.
    Total Time = $7.5 + 20 + 1.25 + 2 = 30.75$ hours.
    Avg Speed = $2000 / 30.75 = 200000 / 3075 = 8000 / 123 = 65.04$ km/hr.
    Wait, let's use fractions for clean division.
    Time = $15/2 + 20 + 5/4 + 2 = (30 + 80 + 5 + 8) / 4 = 123 / 4$.
    Speed = $2000 / (123/4) = 8000 / 123 = 65 \frac{5}{123}$ km/hr.
*   **Fastest Shortcut:** Calculate exact fractional times. Total Distance / Total Time.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** Capgemini

**Q6. (Meeting Point / Stoppages)** Excluding stoppages, the speed of a bus is 54 km/hr and including stoppages, it is 45 km/hr. For how many minutes does the bus stop per hour?
*   **Answer:** 10 minutes
*   **Detailed Solution:** Distance covered in 1 hr without stopping = 54 km.
    Distance covered in 1 hr with stopping = 45 km.
    Loss in distance = $54 - 45 = 9$ km.
    Time taken to cover 9 km at original speed = $9 / 54 = 1/6$ hour.
    $1/6$ hour = 10 minutes.
*   **Fastest Shortcut:** $\text{Stoppage Time/hr} = \frac{\text{Fast} - \text{Slow}}{\text{Fast}} \times 60 \text{ mins}$.
    $(54 - 45) / 54 \times 60 = (9 / 54) \times 60 = 10$ mins.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Deloitte

**Q7. (Police and Thief)** A thief is spotted by a policeman from a distance of 100 meters. When the policeman starts the chase, the thief also starts running. If the speed of the thief be 8 km/hr and that of the policeman 10 km/hr, how far will the thief have run before he is overtaken?
*   **Answer:** 400 meters
*   **Detailed Solution:** Relative Speed = $10 - 8 = 2$ km/hr = $2 \times (5/18) = 5/9$ m/s.
    Time to catch = Distance / Relative Speed = $100 / (5/9) = 180$ seconds.
    Thief's speed in m/s = $8 \times (5/18) = 20/9$ m/s.
    Distance thief ran = Speed $\times$ Time = $(20/9) \times 180 = 20 \times 20 = 400$ meters.
*   **Fastest Shortcut:** Ratio of Speeds = $10 : 8 = 5 : 4$.
    Since time is constant, Distance Ratio = $5 : 4$.
    Difference = 1 part = 100 meters.
    Thief's distance = 4 parts = 400 meters. (Solved in 3 seconds!).
*   **Common Mistake:** Converting to m/s when a direct ratio solves it instantly.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Medium
*   **Company:** TCS NQT Advanced

**Q8. (Meeting and Continuing)** Two trains A and B start from stations X and Y towards each other. After meeting, they take 4 hours and 9 hours to reach Y and X respectively. What is the ratio of their speeds?
*   **Answer:** 3:2
*   **Detailed Solution:** $S_A / S_B = \sqrt{T_B / T_A}$.
    $S_A / S_B = \sqrt{9 / 4} = 3 / 2$.
    Ratio = 3 : 2.
*   **Fastest Shortcut:** Inverse the times and take the square root. Pure formula application.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** IBM

**Q9. (Gunfire / Sound)** Two guns are fired from the same place at an interval of 6 minutes. A person approaching the place in a car hears the second shot 5 minutes 52 seconds after the first. Find the speed of the car if the speed of sound is 330 m/s.
*   **Answer:** 7.5 m/s or 27 km/hr
*   **Detailed Solution:**
    Difference in time = $6 \text{ mins} - 5 \text{ min } 52 \text{ secs} = 8$ seconds.
    The distance sound would travel in 8 seconds is covered by the car in 5 min 52 secs (352 seconds).
    $D_{\text{sound}} = D_{\text{car}}$.
    $S_{\text{sound}} \times 8 = S_{\text{car}} \times 352$.
    $330 \times 8 = S_{\text{car}} \times 352 \implies S_{\text{car}} = (330 \times 8) / 352 = 330 / 44 = 15 / 2 = 7.5$ m/s.
*   **Fastest Shortcut:** $S_{\text{car}} / S_{\text{sound}} = \text{Time Gap} / \text{Time Heard}$.
    $S_{\text{car}} / 330 = 8 / 352 \implies S_{\text{car}} = 330 \times (8/352) = 7.5$.
*   **Common Mistake:** Multiplying 330 by the 6 minutes.
*   **Expected Time:** 25 seconds
*   **Difficulty:** Hard
*   **Company:** Cognizant

**Q10. (Walking both ways)** A man takes 6 hours 15 minutes in walking a distance and riding back to the starting place. He could walk both ways in 7 hours 45 minutes. The time taken by him to ride both ways is:
*   **Answer:** 4 hours 45 minutes
*   **Detailed Solution:** Let $W$ = time to walk one way. Let $R$ = time to ride one way.
    $W + R = 6 \text{ hrs } 15 \text{ mins}$.
    $2W = 7 \text{ hrs } 45 \text{ mins} \implies W = 3 \text{ hrs } 52.5 \text{ mins}$.
    $R = (6 \text{ hrs } 15 \text{ mins}) - (3 \text{ hrs } 52.5 \text{ mins}) = 2 \text{ hrs } 22.5 \text{ mins}$.
    $2R = 4 \text{ hrs } 45 \text{ mins}$.
*   **Fastest Shortcut:** $2 \times (\text{Walk + Ride}) = 2W + 2R$.
    $2 \times (6 \text{ hrs } 15) = 12 \text{ hrs } 30 \text{ mins}$.
    $2R = 12 \text{ hrs } 30 \text{ mins} - 2W = 12 \text{ hrs } 30 \text{ mins} - 7 \text{ hrs } 45 \text{ mins} = 4 \text{ hrs } 45 \text{ mins}$.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** Tech Mahindra

**Q11. (Distance covered in parts)** A man travels a certain distance at 10 km/hr and returns at 15 km/hr. If the total time taken is 5 hours, find the total distance covered.
*   **Answer:** 60 km
*   **Detailed Solution:** Let one way distance be $D$.
    $D/10 + D/15 = 5$.
    $3D/30 + 2D/30 = 5 \implies 5D/30 = 5 \implies D/6 = 1 \implies D = 30$.
    Total distance = $2D = 60$ km.
*   **Fastest Shortcut:** $D = \frac{S_1 S_2}{S_1 + S_2} \times \text{Total Time}$.
    $D = \frac{10 \times 15}{10 + 15} \times 5 = \frac{150}{25} \times 5 = 6 \times 5 = 30$ km.
    Total = $2 \times 30 = 60$ km.
*   **Common Mistake:** Finding $D=30$ and marking it as the answer. The question asks for TOTAL distance covered.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** LTIMindtree

**Q12. (Monkey climbing greased pole)** A monkey climbs a 60-meter high pole. In the first minute, he climbs 6 meters and slips down 3 meters in the next minute. How much time will he take to reach the top?
*   **Answer:** 37 minutes
*   **Detailed Solution:** Net climb in 2 mins = $6 - 3 = 3$ meters.
    Subtract final positive jump: $60 - 6 = 54$ meters.
    Time for 54 meters = $(54 / 3) \times 2 = 18 \times 2 = 36$ minutes.
    In the 37th minute, he climbs 6 meters and reaches the top (60m). He doesn't slip down.
*   **Fastest Shortcut:** $\text{Time} = \frac{\text{Total} - \text{Jump}}{\text{Net}} \times 2 + 1 = \frac{60-6}{3} \times 2 + 1 = \frac{54}{3} \times 2 + 1 = 36 + 1 = 37$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Hard
*   **Company:** HCL

**Q13. (Relative speed meeting)** A train leaves Delhi at 6 AM and reaches Agra at 10 AM. Another train leaves Agra at 8 AM and reaches Delhi at 11:30 AM. At what time do the two trains cross each other?
*   **Answer:** 8:56 AM
*   **Detailed Solution:** Train 1 (D to A) takes 4 hours. Train 2 (A to D) takes 3.5 hours.
    Assume distance = LCM(4, 3.5) = 28 km.
    $S_1 = 28 / 4 = 7$ km/hr.
    $S_2 = 28 / 3.5 = 8$ km/hr.
    Train 1 starts at 6 AM. By 8 AM (when Train 2 starts), Train 1 has traveled $2 \times 7 = 14$ km.
    Remaining distance = $28 - 14 = 14$ km.
    Relative speed = $7 + 8 = 15$ km/hr.
    Time to meet = $14 / 15$ hours = $(14/15) \times 60 = 56$ minutes.
    Meeting time = 8 AM + 56 mins = 8:56 AM.
*   **Fastest Shortcut:** Pure LCM trick logic. Treat it exactly like a "Pipes and Cisterns" problem where distance is the Capacity.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** EY

**Q14. (Increasing Speed)** A car completes a journey in 10 hours. If it covers half the distance at 21 km/hr and the rest at 24 km/hr, find the total distance.
*   **Answer:** 224 km
*   **Detailed Solution:** Let half distance be $D$.
    $D/21 + D/24 = 10$.
    LCM(21, 24) = 168.
    $8D/168 + 7D/168 = 10 \implies 15D/168 = 10 \implies D = 1680 / 15 = 112$.
    Total distance = $2D = 224$ km.
*   **Fastest Shortcut:** $\frac{2xy}{x+y} \times T = \frac{2 \times 21 \times 24}{45} \times 10 = \frac{1008}{45} \times 10 = 22.4 \times 10 = 224$.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** PwC

**Q15. (Fog and Visibility)** A man walking at 3 km/hr crosses a carriage in fog. He can see it for 4 minutes up to a distance of 100 meters. Find the speed of the carriage.
*   **Answer:** 4.5 km/hr
*   **Detailed Solution:** Both are moving in the same direction.
    Relative Speed = $S_{\text{carriage}} - S_{\text{man}}$.
    Distance = 100m = 0.1 km. Time = 4 mins = 4/60 hrs = 1/15 hrs.
    Rel Speed = Distance / Time = $0.1 / (1/15) = 1.5$ km/hr.
    $S_c - 3 = 1.5 \implies S_c = 4.5$ km/hr.
*   **Fastest Shortcut:** Keep all units in km and hours.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** TCS NQT Advanced

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Early/Late:** Direct formula application.
2.  **Stoppages:** Formula $(F - S)/F \times 60$.
3.  **Thief and Police:** Relative speed with same direction.

**Latest trend:**
*   Adding logical traps like "Monkey climbing" or "Firing two guns". Focus on the relative time difference rather than the absolute speeds.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **Early/Late** | $D = \frac{xy}{x \sim y} \times \Delta T$. |
| **Police/Thief** | $D_{\text{thief}} = \frac{S_{\text{thief}}}{\text{Rel Speed}} \times \text{Initial Gap}$. |
| **Avg Speed (Half Dists)** | $Avg = 2xy / (x+y)$. |
| **Stoppage Time** | $\frac{Fast - Slow}{Fast} \times 60$ mins. |
| **Post-Meeting Times** | $S_1/S_2 = \sqrt{T_2/T_1}$. |
