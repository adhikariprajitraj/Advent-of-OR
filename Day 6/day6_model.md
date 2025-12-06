# Day 6: My Optimization Model

To get this optimizations process started, I think we need to focus on just the essential moving parts. Here is how I set up the initial model.

## 1. Decision Variables

For the primary decision, I believe we simply need to determine the **target exposure** for each segment in the coming quarter.
I'm denoting this as $x_s$ for every segment $s$.

To make the cost calculations easier (linear), I also defined two auxiliary variables to track the *change* in exposure:
*   $b_s$: Amount bought (new originations)
*   $\ell_s$: Amount sold

Basic balance equation:
$$x_s = E_s + b_s - \ell_s$$

Where:
*   $E_s$: Current exposure for segment $s$

## 2. Objective Function

My goal here is simple: **Maximize the total portfolio profit net of transaction costs.**
I think we just sum up the expected profit from the target positions and subtract the costs of getting there.

$$
\max \sum_{s \in S} \left( p_s x_s  - c^{	ext{orig}}_s b_s - c^{	ext{sell}}_s \ell_s \right)
$$


*   $p_s$: Expected return (profitability)
*   $c^{	ext{orig}}_s$: Cost rate for new originations
*   $c^{	ext{sell}}_s$: Cost rate for selling loans

## 3. Constraints

I think these are the three most critical constraints to enforce right now:

**A. Regulatory Risk Limit:** The risk-weighted assets cannot exceed 50% of the total exposure.

$$ \sum_{s} w_s x_s \le 0.50 \sum_{s} x_s $$

Where $w_s$ is the risk weight for segment $s$.

**B. Growth Cap:** I don't think we should grow the total portfolio by more than 20% in a single quarter.

$$\sum_{s} x_s \le 1.20 \sum_{s} E_s $$

**C. Asset-Level Guardrails:** For any specific asset type (like "Consumer Loans"), we shouldn't deviate too wildly from the current allocation.

$$ (1 - d_a) E_a \le \sum_{s \in S(a)} x_s \le (1 + u_a) E_a $$

Where:
*   $d_a, u_a$: Allowed decrease/increase percentage for asset $a$
*   $E_a$: Current total exposure for asset $a$
*   $S(a)$: Set of segments belonging to asset type $a$

## 4. List Model Assumptions

To make this first iteration solvable, I had to make a few simplifying assumptions:
1.  **Historical Profitability holds:** I'm assuming that past average returns are a perfect predictor of next quarter's returns.
2.  **Linear Costs:** I'm assuming transaction costs are purely proportional to volume, ignoring any fixed fees or economies of scale.
3.  **Liquidity:** I assume we can buy or sell any amount of these assets immediately without impacting the market price.
