# Day 6: My Optimization Model

To get this optimization process started, I want the model to stay simple but expressive enough to reflect ABC Financial’s structure.  
Each asset contains multiple risk segments, so I index them as:

- Assets: $i = 1,\dots,18$
- Segments: $j = 1,\dots,4$

Each pair $(i,j)$ represents a single portfolio segment.

---

## 1. Decision Variables

The main decision is the **target exposure** next quarter:

$x_{ij}$ = target exposure for asset $i$ in segment $j$

To model changes linearly, I use:

- $b_{ij}$ = amount of exposure bought (new originations)
- $\ell_{ij}$ = amount of exposure sold

Exposure updates according to:

$$
x_{ij} = E_{ij} + b_{ij} - \ell_{ij}
$$

Where $E_{ij}$ is the current exposure.

---

## 2. Objective Function

The goal is to **maximize expected profit minus origination and selling costs**:

$$
\max \sum_{i=1}^{18} \sum_{j=1}^{4} \left(p_{ij} x_{ij} - c^{\text{orig}}_{ij} b_{ij}- c^{\text{sell}}_{ij} \ell_{ij}\right)
$$

Where:

- $p_{ij}$ = expected profitability  
- $c^{\text{orig}}_{ij}$ = origination cost rate  
- $c^{\text{sell}}_{ij}$ = selling cost rate  

---

## 3. Constraints

### **A. Regulatory Risk Limit**

The portfolio's weighted-average risk must not exceed $50\%$:

$$
\sum_{i=1}^{18} \sum_{j=1}^{4} w_{ij} x_{ij}
\le
0.50
\sum_{i=1}^{18} \sum_{j=1}^{4} x_{ij}
$$

---

### **B. Portfolio Growth Cap**

Total exposure should not grow by more than $20\%$:

$$
\sum_{i=1}^{18} \sum_{j=1}^{4} x_{ij}
\le
1.20
\sum_{i=1}^{18} \sum_{j=1}^{4} E_{ij}
$$

---

### **C. Asset-Level Guardrails**

For each asset $i$:

$$
(1 - d_i)
\sum_{j=1}^{4} E_{ij}
\le
\sum_{j=1}^{4} x_{ij}
\le
(1 + u_i)
\sum_{j=1}^{4} E_{ij}
$$

Where:

- $d_i$ = maximum allowed decrease  
- $u_i$ = maximum allowed increase  

---

### **D. Non-negativity**

$$
b_{ij} \ge 0, \quad
\ell_{ij} \ge 0, \quad
x_{ij} \ge 0
\quad \forall i,j
$$

---

## 4. Model Assumptions

1. Historical average profitability $p_{ij}$ is assumed to represent next quarter’s return.  
2. Transaction costs are linear in $b_{ij}$ and $\ell_{ij}$.  
3. The market is assumed liquid enough to buy/sell any amount.  
4. Risk weights $w_{ij}$ stay constant across the quarter.  
5. No interactions between segments are modeled in this version.

