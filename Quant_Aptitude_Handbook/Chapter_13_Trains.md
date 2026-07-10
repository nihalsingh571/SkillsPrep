# Chapter 13: Trains

## 1. Importance

**Why companies ask this topic:**
Trains is a specialized subset of Time, Speed, and Distance. It specifically tests **Relative Speed** and **Relative Distance**. The key twist is that trains have their own significant lengths, which must be factored into the distance.

**Expected number of questions:**
1 to 2 questions.

**Difficulty level:**
Moderate. The concepts are simple, but mixing up units (km/hr vs meters) is the #1 reason candidates fail here.

**Companies asking this topic:**
TCS NQT, Infosys, Accenture, Wipro, Capgemini, IBM, Cognizant.

---

## 2. Quick Revision

**Core Concept:**
Everything from TSD applies. $D = S \times T$.
However, $D$ is now the **Total Length** to be crossed, and $S$ is the **Relative Speed**.

**Rules for Distance ($D$):**
*   **Crossing a point object** (Man, Pole, Tree): $D = \text{Length of Train} (L_T)$.
*   **Crossing a length object** (Platform, Bridge, Tunnel, Another Train): $D = \text{Length of Train} + \text{Length of Object} (L_T + L_O)$.
*   *Distance is ALWAYS ADDED, regardless of the direction of travel.*

**Rules for Relative Speed ($S$):**
*   **Opposite Direction:** Speeds are ADDED. $S_{\text{rel}} = S_1 + S_2$.
*   **Same Direction:** Speeds are SUBTRACTED. $S_{\text{rel}} = |S_1 - S_2|$.
*   **Stationary Object:** $S_{\text{rel}} = \text{Speed of Train}$.

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The Universal Train Equation** is the only formula you need for 90% of train problems.

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Universal Equation** | $T = \frac{L_1 + L_2}{S_1 \pm S_2}$ | Convert Speeds to m/s first! |
| **Opposite Direction** | Use $S_1 + S_2$ | Approaching each other = Faster crossing. |
| **Same Direction** | Use $S_1 - S_2$ | Chasing = Slower crossing. |
| **Crossing a platform** | $L_2 = L_{\text{platform}}$, $S_2 = 0$ | Platform doesn't move. |
| **Crossing a moving man** | $L_2 = 0$, $S_2 = S_{\text{man}}$ | Man has no length, but has speed. |

---

## 4. Fast Tricks

**The "Platform vs Pole" Trick**
If a train crosses a pole in 10 seconds and a 100m platform in 15 seconds.
*Logic:* The extra 5 seconds (15 - 10) were taken strictly to cross the EXTRA 100m of the platform.
Speed of Train = $100\text{m} / 5\text{s} = 20\text{ m/s}$.
Length of Train = Speed $\times$ Time to cross pole = $20 \times 10 = 200\text{m}$.
(Solved entirely mentally without simultaneous equations).

**The 18:5 Ratio for Trains**
Because train lengths are in meters and speeds are given in km/hr, you MUST convert instantly.
72 km/hr = 20 m/s.
90 km/hr = 25 m/s.
108 km/hr = 30 m/s.

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "Crosses a telegraph post" | Distance = Train Length ONLY. | $L = S \times T$. |
| "Crosses a bridge of 150m" | Distance = $L + 150$. | $L + 150 = S \times T$. |
| "Two trains parallel tracks same direction" | Relative Speed = $S_1 - S_2$. | $T = (L_1 + L_2) / (S_1 - S_2)$. |
| "Man sitting in the slower train" | Target is the MAN, not the train! | $D = L_{\text{Faster Train}}$ ONLY. |

---

## 6. Solving Framework

**Step-by-step fastest solving approach:**
1.  **Read Speed:** Immediately convert km/hr to m/s.
2.  **Determine Distance ($D$):** Is it $L$ or $L + P$ or $L_1 + L_2$?
3.  **Determine Relative Speed ($S$):** Is it $S$ or $S_1 + S_2$ or $S_1 - S_2$?
4.  **Plug into $D = S \times T$.**

**Comparison of Methods:**
*Example: A train 150m long is running at 72 km/hr. How long will it take to pass a man running at 9 km/hr in the opposite direction?*
*   **Traditional Method:**
    Train speed = $72 \times 5/18 = 20$ m/s.
    Man speed = $9 \times 5/18 = 2.5$ m/s.
    Rel Speed = $20 + 2.5 = 22.5$ m/s.
    Time = $150 / 22.5 = 1500 / 225 = 6.66$ seconds.
*   **Placement Shortcut (Add km/hr first):**
    Rel Speed in km/hr = $72 + 9 = 81$ km/hr.
    Convert to m/s = $81 \times (5/18) = 9 \times 5 / 2 = 45/2 = 22.5$ m/s.
    Time = $150 / (45/2) = 300 / 45 = 20/3 = 6.66$ secs.
    *(Always add/subtract the km/hr speeds BEFORE converting. It saves you from dealing with messy fractions twice).*

> [!WARNING]
> **The "Man in the Train" Trap:**
> "A faster train crosses a man sitting in a slower train."
> The length of the slower train is IRRELEVANT. The faster train is only crossing the MAN (a point object). So $D = L_{\text{Faster}}$ only. But relative speed still uses the speeds of BOTH trains.

---

## 7. High Quality Practice Questions

**Q1. (Basic Train vs Pole)** A train 150 m long is running at a speed of 68 km/hr. How much time will it take to pass a man who is running at 8 km/hr in the same direction in which the train is going?
*   **Answer:** 9 seconds
*   **Detailed Solution:** Same direction $\implies$ Relative Speed = $68 - 8 = 60$ km/hr.
    Convert to m/s: $60 \times (5/18) = 50/3$ m/s.
    Distance to cross man = Length of Train = 150m.
    Time = $D / S = 150 / (50/3) = (150 \times 3) / 50 = 3 \times 3 = 9$ seconds.
*   **Fastest Shortcut:** Do the relative speed in km/hr first, then convert.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** TCS NQT

**Q2. (Platform crossing)** A train 132 m long passes a telegraph pole in 6 seconds. Find the time it will take to cross a bridge 264 m long.
*   **Answer:** 18 seconds
*   **Detailed Solution:** Speed of train = $132 / 6 = 22$ m/s.
    Total distance to cross bridge = $L_{\text{train}} + L_{\text{bridge}} = 132 + 264 = 396$ m.
    Time = $396 / 22 = 18$ seconds.
*   **Fastest Shortcut:** Proportionality Trick!
    Bridge is exactly TWICE the length of the train ($264 = 2 \times 132$).
    Total distance = Train + 2(Train) = 3(Train).
    If 1 Train length takes 6 secs, 3 Train lengths take $3 \times 6 = 18$ secs. (Zero calculation needed).
*   **Expected Time:** 5 seconds
*   **Difficulty:** Medium
*   **Company:** Infosys

**Q3. (Two Trains Same Direction)** Two trains of length 120m and 90m are running in the same direction on parallel lines at 40 km/hr and 50 km/hr respectively. In what time will they pass each other?
*   **Answer:** 75.6 seconds
*   **Detailed Solution:** Distance = $120 + 90 = 210$ m. (Lengths are ALWAYS added).
    Relative Speed = $50 - 40 = 10$ km/hr.
    Convert to m/s: $10 \times (5/18) = 50/18 = 25/9$ m/s.
    Time = $210 / (25/9) = (210 \times 9) / 25 = 1890 / 25 = 75.6$ seconds.
*   **Fastest Shortcut:** Standard universal formula.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** Wipro

**Q4. (Finding Train Length)** A train moving at a speed of 54 km/hr crosses a bridge of length 100 meters in 15 seconds. Find the length of the train.
*   **Answer:** 125 meters
*   **Detailed Solution:** Speed = $54 \times (5/18) = 15$ m/s.
    Distance covered in 15 seconds = $15 \text{ m/s} \times 15\text{s} = 225$ meters.
    This total distance = $L_{\text{train}} + L_{\text{bridge}}$.
    $225 = L_{\text{train}} + 100 \implies L_{\text{train}} = 125$ meters.
*   **Fastest Shortcut:** Find total distance first, then subtract bridge.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q5. (The Extra Time Trick)** A train crosses a pole in 15 seconds and a 100m long platform in 25 seconds. Find its length.
*   **Answer:** 150 meters
*   **Detailed Solution:** Extra time = $25 - 15 = 10$ seconds.
    This 10 seconds is used to cross the EXTRA 100m.
    Speed = $100 / 10 = 10$ m/s.
    Length of train = Time to cross pole $\times$ Speed = $15 \times 10 = 150$ meters.
*   **Fastest Shortcut:** This IS the shortcut. Never use simultaneous equations here.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Medium
*   **Company:** Capgemini

**Q6. (Man in the Train Trap)** Two trains are moving in the same direction at 50 km/hr and 30 km/hr. The faster train crosses a man sitting in the slower train in 18 seconds. Find the length of the faster train.
*   **Answer:** 100 meters
*   **Detailed Solution:** Target is the MAN, not the slower train.
    Distance = Length of FASTER train only ($L_F$).
    Relative Speed = $50 - 30 = 20$ km/hr.
    $20 \text{ km/hr} \times (5/18) = 100/18 = 50/9$ m/s.
    Time = 18 seconds.
    Distance ($L_F$) = Speed $\times$ Time = $(50/9) \times 18 = 50 \times 2 = 100$ meters.
*   **Fastest Shortcut:** Just remember: Crossing a man $\implies$ only one train length matters.
*   **Common Mistake:** Trying to find the sum of both train lengths.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

**Q7. (Trains meeting midpoint)** Two stations A and B are 110 km apart on a straight line. One train starts from A at 7 AM and travels towards B at 20 km/hr. Another starts from B at 8 AM and travels towards A at 25 km/hr. At what time will they meet?
*   **Answer:** 10 AM
*   **Detailed Solution:** Make their start times equal.
    At 8 AM, Train A has travelled for 1 hour $\implies 20$ km.
    Remaining distance = $110 - 20 = 90$ km.
    Now, both are moving towards each other.
    Relative Speed = $20 + 25 = 45$ km/hr.
    Time to cover 90 km = $90 / 45 = 2$ hours.
    Meeting time = 8 AM + 2 hours = 10 AM.
*   **Fastest Shortcut:** Align start times mentally, find remaining distance, divide by sum of speeds.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** IBM

**Q8. (Two men walking)** A train overtakes two persons who are walking in the same direction in which the train is going, at the rate of 2 kmph and 4 kmph and passes them completely in 9 and 10 seconds respectively. The length of the train is:
*   **Answer:** 50 meters
*   **Detailed Solution:** Let speed of train be $S$ km/hr.
    Rel Speed 1 = $(S - 2) \times 5/18$ m/s. Time = 9s.
    Rel Speed 2 = $(S - 4) \times 5/18$ m/s. Time = 10s.
    Distance (Length of train) is same in both cases.
    $(S - 2) \times \frac{5}{18} \times 9 = (S - 4) \times \frac{5}{18} \times 10$.
    $(S - 2) \times 9 = (S - 4) \times 10$.
    $9S - 18 = 10S - 40 \implies S = 22$ km/hr.
    Length = $(22 - 2) \times \frac{5}{18} \times 9 = 20 \times \frac{5}{2} = 50$ meters.
*   **Fastest Shortcut:** Equating the $(S_{\text{rel}} \times T)$ directly without the $5/18$ factor initially to find $S$ in km/hr.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** Cognizant

**Q9. (Two trains crossing stationary object and each other)** Two trains of equal length take 10 seconds and 15 seconds respectively to cross a telegraph post. If the length of each train be 120 metres, in what time will they cross each other traveling in opposite direction?
*   **Answer:** 12 seconds
*   **Detailed Solution:** $S_1 = 120 / 10 = 12$ m/s.
    $S_2 = 120 / 15 = 8$ m/s.
    Opposite direction, Rel Speed = $12 + 8 = 20$ m/s.
    Total Distance = $120 + 120 = 240$ m.
    Time = $240 / 20 = 12$ seconds.
*   **Fastest Shortcut:** If lengths are equal and crossing a pole takes $T_1$ and $T_2$, time to cross each other in opposite direction = $\frac{2 T_1 T_2}{T_1 + T_2}$.
    $\frac{2 \times 10 \times 15}{10 + 15} = \frac{300}{25} = 12$ seconds. (Insanely fast trick).
*   **Expected Time:** 5 seconds
*   **Difficulty:** Medium
*   **Company:** Tech Mahindra

**Q10. (Crossing a bridge and a platform)** A train passes a 50m long platform in 14 seconds and a man standing on the platform in 10 seconds. The speed of the train is:
*   **Answer:** 45 km/hr
*   **Detailed Solution:** Crossing a man = 10 secs (This is crossing just its own length).
    Crossing 50m platform = 14 secs.
    Extra 4 secs to cross 50m.
    Speed = $50\text{m} / 4\text{s} = 12.5$ m/s.
    Convert to km/hr = $12.5 \times 18 / 5 = 2.5 \times 18 = 45$ km/hr.
*   **Fastest Shortcut:** Extra distance / Extra time = Speed. Then convert.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q11. (Trains without lengths given)** Two trains are running in opposite directions with the same speed. If the length of each train is 120 meters and they cross each other in 12 seconds, then the speed of each train is:
*   **Answer:** 36 km/hr
*   **Detailed Solution:** Total Length = $120 + 120 = 240$m.
    Time = 12s.
    Relative Speed = $240 / 12 = 20$ m/s.
    Since speeds are same and opposite direction: $S + S = 20 \implies 2S = 20 \implies S = 10$ m/s.
    Convert to km/hr: $10 \times 18/5 = 36$ km/hr.
*   **Fastest Shortcut:** Pure logic. If relative is 20, individual is 10. $10 \text{ m/s} = 36 \text{ km/hr}$.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Easy
*   **Company:** PwC

**Q12. (Relative distance gap)** A train traveling at 60 km/hr catches another train traveling in the same direction at 40 km/hr in 3 hours. What is the distance between the two trains at the start?
*   **Answer:** 60 km
*   **Detailed Solution:** Relative speed = $60 - 40 = 20$ km/hr.
    This is the speed at which the gap is closing.
    Distance gap = Rel Speed $\times$ Time = $20 \times 3 = 60$ km.
*   **Fastest Shortcut:** Direct multiplication.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** HCL

**Q13. (Without Train Speeds)** Two trains starting at the same time from 2 stations 200 km apart and going in opposite direction cross each other at a distance of 110 km from one of the stations. What is the ratio of their speeds?
*   **Answer:** 11:9
*   **Detailed Solution:** Distance covered by Train 1 = 110 km.
    Distance covered by Train 2 = $200 - 110 = 90$ km.
    Since time is constant (they started at same time and met), Ratio of Speeds = Ratio of Distances.
    Speed Ratio = $110 : 90 = 11 : 9$.
*   **Fastest Shortcut:** Just find the ratio of distances traveled.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q14. (Bird flying between trains)** Two trains 200 km apart are moving towards each other at speeds of 50 km/hr and 50 km/hr. A bird starts flying from one train to the other at 150 km/hr. It touches the second train, turns back and flies to the first, and so on until the trains collide. What is the total distance covered by the bird?
*   **Answer:** 300 km
*   **Detailed Solution:** Find time taken for trains to collide.
    Rel Speed of trains = $50 + 50 = 100$ km/hr.
    Time = Distance / Rel Speed = $200 / 100 = 2$ hours.
    The bird is flying continuously for 2 hours!
    Distance of bird = Bird Speed $\times$ Total Time = $150 \times 2 = 300$ km.
*   **Fastest Shortcut:** Never calculate the zigzag paths. Just find total time of flight.
*   **Common Mistake:** Trying to calculate distance for each turn.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q15. (Engine and Bogies)** A goods train has an engine and 10 identical bogies. The train crosses a pole in 22 seconds. If 3 bogies are removed, it crosses the pole in 16 seconds. Find the time taken by the engine alone to cross the pole.
*   **Answer:** 4 seconds
*   **Detailed Solution:** Let Engine length = E. Let 1 Bogie length = B.
    Case 1: Length = $E + 10B$. Time = 22s.
    Case 2: Length = $E + 7B$. Time = 16s.
    Difference in length = $3B$. Difference in time = $6s$.
    So, 3 Bogies take 6 seconds to cross.
    1 Bogie takes 2 seconds to cross.
    Total time = 22s. 10 Bogies take $10 \times 2 = 20$s.
    Remaining time for Engine = $22 - 20 = 2$ seconds? Wait. Let me re-read.
    *Self-Correction:* If 1 Bogie takes 2 seconds, 10 Bogies take 20s. The Engine takes the remaining $22 - 20 = 2$ seconds.
    Let's verify: $E = 2$ seconds. Case 2: $E + 7B \implies 2 + 7(2) = 16$. Yes.
    So time taken by Engine alone is 2 seconds.
    Wait, my initial answer said 4 seconds. Let's trace why I wrote 4.
    If the question was "5 bogies removed, takes 12 seconds". Then $5B = 10s \implies B=2s$. $10B = 20s$. $E = 22-20 = 2s$.
    Okay, the answer is 2 seconds.
    *Corrected Answer: 2 seconds*
*   **Fastest Shortcut:** Find time per bogie directly from the differences.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Hard
*   **Company:** EY

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **Platform vs Pole:** The "Extra Distance / Extra Time" shortcut solves 30% of all train questions.
2.  **Man in Slower Train:** Testing if you know to ignore the slower train's length.
3.  **Two trains opposite:** Using $\frac{2 T_1 T_2}{T_1 + T_2}$ for crossing each other.

**Latest trend:**
*   Mixing Time Speed Distance with variable bogie lengths to test pure logical deduction without specific speed values (like Q15).

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **Length Addition** | Lengths are ALWAYS ADDED. Never subtracted. |
| **Speed Conversion** | Convert km/hr to m/s BEFORE solving the main equation. |
| **Pole vs Platform** | Speed = Length of Platform / Extra Time Taken. |
| **Man in Train** | Distance = Length of the train passing the man. |
| **Equal Trains crossing** | Opposite direction time = $\frac{2 T_1 T_2}{T_1 + T_2}$. |
