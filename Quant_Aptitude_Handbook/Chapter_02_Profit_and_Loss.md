# Chapter 02: Profit & Loss

## 1. Importance

**Why companies ask this topic:**
Profit & Loss is the direct application of Percentages into real-world business scenarios. Companies use these questions to check your ability to handle multiple variables (Cost Price, Selling Price, Marked Price, Discount) simultaneously under time pressure.

**Expected number of questions:**
2 to 3 questions. It is almost guaranteed in every placement paper.

**Difficulty level:**
Moderate to Hard. The complexity comes from tricky language like "False Weights" and "Markup Percentage."

**Companies asking this topic:**
TCS NQT, Infosys, Accenture, Cognizant, and Wipro heavily test this. It's a staple in banking and product-based companies as well.

---

## 2. Quick Revision

**Core Terminologies:**
*   **CP (Cost Price):** The price at which goods are bought. Always $100\%$ base.
*   **SP (Selling Price):** The price at which goods are sold.
*   **MP (Marked Price / MRP):** The price written on the tag.
*   **Discount:** Always given on MP.
*   **Profit / Loss:** Always calculated on CP (unless specifically mentioned otherwise).
*   **Markup:** The amount by which CP is increased to get MP.

**The Golden Chain:**
$\text{CP} \xrightarrow{+\text{Markup}\%} \text{MP} \xrightarrow{-\text{Discount}\%} \text{SP}$
$\text{CP} \xrightarrow{+\text{Profit}\% / -\text{Loss}\%} \text{SP}$

---

## 3. Formula Sheet

> [!TIP]
> **Highlight: The CP-MP Ratio Formula** is the ultimate time-saver. Memorize it!

| Concept | Formula / Shortcut | Memory Trick |
| :--- | :--- | :--- |
| **Profit %** | $\frac{\text{SP} - \text{CP}}{\text{CP}} \times 100$ | Always divide by CP. |
| **Loss %** | $\frac{\text{CP} - \text{SP}}{\text{CP}} \times 100$ | Always divide by CP. |
| **SP from CP & Profit%** | $\text{CP} \times (\frac{100+P}{100})$ | Multiplier is $> 1$. |
| **SP from MP & Discount%** | $\text{MP} \times (\frac{100-D}{100})$ | Multiplier is $< 1$. |
| **The Ultimate CP-MP Ratio** | $\frac{\text{CP}}{\text{MP}} = \frac{100 - D\%}{100 + P\%}$ | **Most important formula.** CP gets the minus, MP gets the plus. |
| **Successive Discount** | $D_1 + D_2 - \frac{D_1 \times D_2}{100}$ | Like successive %, but formula has a minus sign. |
| **False Weight Gain %** | $\frac{\text{Error}}{\text{True Value} - \text{Error}} \times 100$ | Error / Given Weight. |
| **Same SP, Same P% & L%** | Always a net Loss of $\frac{x^2}{100}\%$ | SP doesn't matter for the %. |

---

## 4. Fast Tricks

**The 100 Base Trick**
Whenever SP or CP is not given, always assume $\text{CP} = 100$. If a discount is given, assume $\text{MP} = 100$.

**Fraction Multipliers for Fast Calculation**
*   20% Profit $\implies \text{SP} = \text{CP} \times \frac{6}{5}$
*   25% Loss $\implies \text{SP} = \text{CP} \times \frac{3}{4}$
*   16.66% Profit $\implies \text{SP} = \text{CP} \times \frac{7}{6}$

**Free Goods = Discount Percentage**
"Buy 4, Get 1 Free" $\implies$ Total goods = 5. Free = 1.
Discount % = $\frac{\text{Free}}{\text{Total}} \times 100 = \frac{1}{5} \times 100 = 20\%$.

**The Dishonest Shopkeeper Shortcut**
Always write: $\text{Quantity} : \text{Price}$.
If he sells at CP but uses 800g instead of 1000g:
His CP is for 800g. His SP is for 1000g.
Profit % = $\frac{1000 - 800}{800} \times 100 = \frac{200}{800} \times 100 = 25\%$.

---

## 5. Question Recognition

| Keyword / Pattern | Hidden Clue | Immediate Shortcut to Apply |
| :--- | :--- | :--- |
| "A shopkeeper allows 10% discount and still makes 20% profit" | Connecting MP, Discount, CP, Profit. | **Ultimate CP-MP Ratio:** $\frac{\text{CP}}{\text{MP}} = \frac{100-D}{100+P}$. |
| "Two articles sold at same price, one at 20% profit, other at 20% loss" | Same SP, same magnitude of P/L%. | Net loss = $\frac{x^2}{100}\%$. |
| "Sells goods at cost price, but uses 900g weight" | Dishonest dealer. | Gain % = $\frac{\text{Error}}{\text{Given Weight}} \times 100$. |
| "Markup is 50%, discount is 20%" | Successive change from CP to MP to SP. | $A + B + \frac{AB}{100}$ (where A is +, B is -). |

---

## 6. Solving Framework

**Step-by-step fastest solving approach:**
1.  **Map the variables:** Are they giving CP, SP, MP, or just percentages?
2.  **Choose the base:** If no absolute values (like Rs. 500) are asked, assume 100 or use fractions.
3.  **Apply the golden chain:** Do not calculate intermediate values if not asked. Use chain multiplication.

**Comparison of Methods:**
*Example: MP is 40% above CP. Discount is 20%. Find Profit %.*
*   **Traditional Method:** Let CP = 100. MP = 140. Discount = 20% of 140 = 28. SP = 140 - 28 = 112. Profit = 112 - 100 = 12. Profit % = 12%.
*   **Fast Method:** Successive \% change. $+40 - 20 - \frac{40 \times 20}{100} = +20 - 8 = +12\%$.
*   **Placement Shortcut:** Mentally $1.4 \times 0.8 = 1.12 \implies 12\%$. (3 seconds).

> [!WARNING]
> **When NOT to use $x^2/100$ shortcut:**
> If the question says "Two articles BOUGHT at the same price" (Same CP) and sold at +x% and -x%. The net profit/loss is **0%**. The $x^2/100$ shortcut is ONLY for "Same SP".

---

## 7. High Quality Practice Questions

**Q1. (CP-MP Ratio)** A shopkeeper allows a discount of 10% on the marked price of an item but still makes a profit of 8%. If the marked price is Rs. 240, find the cost price.
*   **Answer:** Rs. 200
*   **Detailed Solution:** $\frac{\text{CP}}{\text{MP}} = \frac{100-10}{100+8} = \frac{90}{108}$. $\frac{\text{CP}}{240} = \frac{90}{108}$. $\text{CP} = \frac{90}{108} \times 240 = \frac{5}{6} \times 240 = 200$.
*   **Fastest Shortcut:** $\text{CP} : \text{MP} = (100-D) : (100+P) = 90 : 108 = 5 : 6$. Since $6 \text{ units} = 240$, $1 \text{ unit} = 40$. $5 \text{ units} = 200$.
*   **Common Mistake:** Applying 10% discount on 240 to get SP, then trying to find CP by calculating $SP \times (100/108)$, which is mathematically identical but prone to slow calculation.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** TCS NQT

**Q2. (Same SP)** A man sells two horses for Rs. 4000 each. On one he gains 20% and on the other he loses 20%. Find his overall gain or loss percentage.
*   **Answer:** 4% Loss
*   **Detailed Solution:** SP1 = 4000, Profit = 20% $\implies$ CP1 = 3333.33. SP2 = 4000, Loss = 20% $\implies$ CP2 = 5000. Total CP = 8333.33. Total SP = 8000. Loss% = $(333.33/8333.33) \times 100 = 4\%$.
*   **Fastest Shortcut:** Same SP, Same % $\implies$ Always loss of $\frac{x^2}{100} = \frac{20^2}{100} = 4\%$. Ignore the Rs. 4000 completely.
*   **Alternative Method:** Just remember $20\% \implies 4\%$ loss. $10\% \implies 1\%$ loss.
*   **Common Mistake:** Answering "No Profit No Loss".
*   **Expected Time:** 2 seconds
*   **Difficulty:** Easy
*   **Company:** Infosys

**Q3. (Dishonest Shopkeeper)** A dishonest dealer claims to sell his goods at cost price, but he uses a weight of 800 grams for a kg. Find his gain percent.
*   **Answer:** 25%
*   **Detailed Solution:** He charges for 1000g but gives 800g. His actual investment (CP) is for 800g. His return (SP) is for 1000g.
    Profit = $1000 - 800 = 200g$.
    Profit % = $(200 / 800) \times 100 = 25\%$.
*   **Fastest Shortcut:** $\frac{\text{Error}}{\text{Given Value}} \times 100 = \frac{200}{800} \times 100 = 25\%$.
*   **Common Mistake:** Dividing by 1000 and getting 20%. You divide by what he actually gives from his pocket.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Wipro

**Q4. (Successive Discounts)** Find the single equivalent discount for two successive discounts of 20% and 10%.
*   **Answer:** 28%
*   **Detailed Solution:** Let MP = 100.
    After 20% discount = 80.
    After 10% discount on 80 = $80 - 8 = 72$.
    Total discount = $100 - 72 = 28\%$.
*   **Fastest Shortcut:** $D_1 + D_2 - \frac{D_1 \times D_2}{100} = 20 + 10 - \frac{20 \times 10}{100} = 30 - 2 = 28\%$.
*   **Common Mistake:** Adding them up to 30%.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Accenture

**Q5. (Buy X Get Y Free)** A shopkeeper offers "Buy 3 Get 1 Free". What is the equivalent discount percentage?
*   **Answer:** 25%
*   **Detailed Solution:** Total articles customer takes home = 4. Customer pays for = 3.
    Free articles = 1.
    Discount is calculated on the TOTAL marked price of all goods.
    Discount % = $(1 / 4) \times 100 = 25\%$.
*   **Fastest Shortcut:** $\frac{\text{Free}}{\text{Total}} \times 100$.
*   **Common Mistake:** Doing $(1 / 3) \times 100 = 33.33\%$. The discount is on the total items given, not the paid ones.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** Capgemini

**Q6. (Cross Multiplication Trick)** A man bought pencils at 6 for Rs. 5 and sold them at 5 for Rs. 6. Find his gain percent.
*   **Answer:** 44%
*   **Detailed Solution:** CP of 1 pencil = $5/6$. SP of 1 pencil = $6/5$.
    Profit = $6/5 - 5/6 = (36-25)/30 = 11/30$.
    Profit % = $((11/30) / (5/6)) \times 100 = (11/30) \times (6/5) \times 100 = 44\%$.
*   **Fastest Shortcut:** Cross multiply:
    Buy: Qty=6, Rs=5
    Sell: Qty=5, Rs=6
    $\text{CP} = 5 \times 5 = 25$.
    $\text{SP} = 6 \times 6 = 36$.
    Profit = $36 - 25 = 11$. Gain% = $(11 / 25) \times 100 = 44\%$.
*   **Common Mistake:** Reversing the CP and SP products. Always multiply Item_Buy $\times$ Price_Sell to get SP.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Medium
*   **Company:** Cognizant

**Q7. (Profit calculated on SP)** A man calculates his profit percentage on the Selling Price and finds it to be 20%. What is his actual profit percentage?
*   **Answer:** 25%
*   **Detailed Solution:** Let SP = 100.
    Profit = 20% of SP = 20.
    Since $\text{SP} = \text{CP} + \text{Profit} \implies 100 = \text{CP} + 20 \implies \text{CP} = 80$.
    Actual Profit % (on CP) = $(20 / 80) \times 100 = 25\%$.
*   **Fastest Shortcut:** Fraction method. Profit = 20% = 1/5 of SP.
    Numerator (1) is Profit. Denominator (5) is SP.
    $\text{CP} = 5 - 1 = 4$.
    Actual % = $1/4 = 25\%$.
*   **Common Mistake:** Answering 20% or 16.66%.
*   **Expected Time:** 10 seconds
*   **Difficulty:** Medium
*   **Company:** Tech Mahindra

**Q8. (Mixing Articles)** A trader mixes 26 kg of rice at Rs. 20/kg with 30 kg of rice at Rs. 36/kg and sells the mixture at Rs. 30/kg. Find his profit%.
*   **Answer:** 5%
*   **Detailed Solution:** Total CP = $(26 \times 20) + (30 \times 36) = 520 + 1080 = 1600$.
    Total Quantity = $26 + 30 = 56 \text{ kg}$.
    Total SP = $56 \times 30 = 1680$.
    Profit = $1680 - 1600 = 80$.
    Profit % = $(80 / 1600) \times 100 = 5\%$.
*   **Fastest Shortcut:** Calculate difference between CP and SP directly per kg.
    Type 1: SP is +10 over CP (30-20). Total gain = $26 \times 10 = +260$.
    Type 2: SP is -6 under CP (30-36). Total loss = $30 \times (-6) = -180$.
    Net gain = $+260 - 180 = +80$.
    Total base CP = $520 + 1080 = 1600$. Gain% = $80/1600 = 5\%$.
*   **Common Mistake:** Making an arithmetic mistake multiplying $30 \times 36$.
*   **Expected Time:** 35 seconds
*   **Difficulty:** Hard
*   **Company:** Deloitte

**Q9. (Markup and Discount to Profit)** By selling an article at 80% of its marked price, a trader makes a loss of 10%. What will be the profit percentage if it is sold at 95% of its marked price?
*   **Answer:** 6.875%
*   **Detailed Solution:** Let MP = 100.
    Case 1: SP = 80. Loss = 10% $\implies \text{CP} \times 0.9 = 80 \implies \text{CP} = 800/9$.
    Case 2: SP = 95.
    Profit = $95 - 800/9 = (855 - 800)/9 = 55/9$.
    Profit % = $\frac{55/9}{800/9} \times 100 = \frac{55}{800} \times 100 = \frac{55}{8} = 6.875\%$.
*   **Fastest Shortcut:** Use ratio. $\frac{\text{SP}_1}{\text{SP}_2} = \frac{100 \pm P_1}{100 \pm P_2}$.
    $\frac{80}{95} = \frac{90}{100+P_2} \implies \frac{16}{19} = \frac{90}{100+P_2} \implies 1600 + 16P_2 = 1710 \implies 16P_2 = 110 \implies P_2 = 6.875\%$.
*   **Common Mistake:** Trying to calculate precise decimal values for CP and getting stuck.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** IBM

**Q10. (Dishonest Shopkeeper - Advanced)** A trader marks up his goods by 20% and gives 10% discount. Besides, he uses 900g weight instead of 1kg. Find his net profit%.
*   **Answer:** 20%
*   **Detailed Solution:** Let CP of 1000g = 1000.
    He uses 900g. His actual CP = 900.
    He marks up by 20% on 1000 $\implies$ MP = 1200.
    Discount 10% on 1200 $\implies$ SP = $1200 - 120 = 1080$.
    His CP is 900, his SP is 1080.
    Profit = 180. Profit % = $(180 / 900) \times 100 = 20\%$.
*   **Fastest Shortcut:** Successive chain rule. Let base CP = 1000.
    Multiplier = $\text{Markup} \times \text{Discount} \times \text{WeightCheat}$.
    SP/CP = $(1.2) \times (0.9) \times (1000/900) = 1.08 \times \frac{10}{9} = \frac{10.8}{9} = 1.2 = +20\%$.
*   **Common Mistake:** Applying the markup on the 900g instead of the advertised 1000g.
*   **Expected Time:** 45 seconds
*   **Difficulty:** Hard
*   **Company:** TCS NQT Advanced

**Q11. (Change in SP)** A mobile is sold at a profit of 20%. If both the CP and SP are decreased by Rs. 100, the profit would be 25%. Find the original CP.
*   **Answer:** Rs. 500
*   **Detailed Solution:** Let CP = $x$. SP = $1.2x$.
    New CP = $x - 100$. New SP = $1.2x - 100$.
    New SP = $1.25 \times \text{New CP}$.
    $1.2x - 100 = 1.25(x - 100) \implies 1.2x - 100 = 1.25x - 125 \implies 0.05x = 25 \implies x = 500$.
*   **Fastest Shortcut:** Ratio method.
    Initial CP:SP = $100:120 = 5:6$.
    Final CP:SP = $100:125 = 4:5$.
    Difference in parts for both is 1 unit ($5 \rightarrow 4$ and $6 \rightarrow 5$).
    $1 \text{ unit} = \text{Rs. } 100$.
    Original CP = $5 \text{ units} = 500$.
*   **Common Mistake:** Setting up the equation backward.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** HCL

**Q12. (Equation of SP)** If selling price is doubled, the profit triples. Find the original profit percentage.
*   **Answer:** 100%
*   **Detailed Solution:** Let CP = $C$, SP = $S$. Orig Profit = $S - C$.
    New SP = $2S$. New Profit = $2S - C$.
    $2S - C = 3(S - C) \implies 2S - C = 3S - 3C \implies S = 2C$.
    Profit = $2C - C = C$.
    Profit % = $(C/C) \times 100 = 100\%$.
*   **Fastest Shortcut:** Assume CP = 10. Check options.
    If profit is 100%, SP = 20. Profit = 10.
    Double SP to 40. Profit = 30.
    $30$ is indeed $3 \times 10$. Proved.
*   **Common Mistake:** Writing the equation as $2S = 3P$, forgetting to subtract C for the new profit.
*   **Expected Time:** 15 seconds
*   **Difficulty:** Easy
*   **Company:** Oracle

**Q13. (Cost Price equating)** 12 pens are bought for Rs. 10 and 10 pens are sold for Rs. 12. Profit %?
*   **Answer:** 44%
*   **Detailed Solution:** CP of 1 pen = 10/12. SP of 1 pen = 12/10.
    Profit% = $\frac{(12/10) - (10/12)}{10/12} \times 100 = \frac{144 - 100}{100} \times 100 = 44\%$.
*   **Fastest Shortcut:** Cross multiply trick! $10 \times 10 = 100$ (CP). $12 \times 12 = 144$ (SP). Profit = 44%.
*   **Expected Time:** 5 seconds
*   **Difficulty:** Easy
*   **Company:** LTIMindtree

**Q14. (Free goods and Discount)** A dealer offers 15% discount and also gives 1 article free on every purchase of 16 articles. What is the total discount %?
*   **Answer:** 20%
*   **Detailed Solution:** Total articles given = 17. Free = 1.
    Discount due to free article = $(1/17) \times 100 = 5.88\%$.
    Successive discount of 15% and 5.88%? Too complex!
*   **Fastest Shortcut:** Use CP/MP chain. Let MP of 1 article = 100.
    Customer pays for 16 articles at 15% discount.
    Amount paid = $16 \times 85 = 1360$.
    Total MP of goods received (17 articles) = 1700.
    Total discount = $1700 - 1360 = 340$.
    Discount % = $(340 / 1700) \times 100 = 20\%$.
*   **Common Mistake:** Adding 15% and $(1/16)\%$ incorrectly.
*   **Expected Time:** 30 seconds
*   **Difficulty:** Hard
*   **Company:** EY

**Q15. (Faulty Balance + Markup)** A grocer marks his goods 10% above CP and uses a faulty balance which reads 1000g for 800g. His actual profit % is:
*   **Answer:** 37.5%
*   **Detailed Solution:** Let base CP of 1000g = 1000.
    He uses 800g. Actual CP = 800.
    He marks up 10% on 1000 $\implies$ SP = 1100.
    Profit = $1100 - 800 = 300$.
    Profit % = $(300 / 800) \times 100 = 37.5\%$.
*   **Fastest Shortcut:** Successive chain: $+10\%$ (markup) and $+25\%$ (faulty weight $200/800$).
    $10 + 25 + \frac{10 \times 25}{100} = 35 + 2.5 = 37.5\%$.
*   **Common Mistake:** Taking the weight profit as $+20\%$ (i.e. $200/1000$) instead of $+25\%$.
*   **Expected Time:** 20 seconds
*   **Difficulty:** Medium
*   **Company:** PwC

---

## 8. Previous Year Pattern

**Repeated question types:**
1.  **CP-MP Ratio:** The formula $\frac{100-D}{100+P}$ appears in almost every test.
2.  **Same SP:** The $x^2/100$ loss trick is a favorite of Infosys and TCS.
3.  **Dishonest Shopkeeper:** Very frequent in Capgemini and Deloitte.

**Latest trend:**
*   Mixing 3 concepts together: Markup + Discount + Faulty Weight in a single question to consume candidate's time. Use the Successive Chain rule to beat it.

---

## 9. Chapter Summary

| Concept | The "Under 1 Minute" Rule |
| :--- | :--- |
| **MP vs CP** | Always use $\frac{\text{CP}}{\text{MP}} = \frac{100-D}{100+P}$ |
| **Same SP, Same %** | Always Loss of $\frac{x^2}{100}\%$. |
| **Dishonest Weight** | Profit % = $\frac{\text{Error}}{\text{Given out weight}} \times 100$. |
| **Buy X Get Y Free** | Discount % = $\frac{Y}{X+Y} \times 100$. |
| **Cross Multiply** | Buy Q1 at R1, Sell Q2 at R2. $\text{CP}=Q2 \times R1, \text{SP}=Q1 \times R2$. |
