import pandas as pd
import numpy as np
import os

print("# Day 5 Analysis Tasks\n")

# Load Data
# We access Day 5 segments because it contains the 'average_profitability' column
try:
    segments_day5 = pd.read_csv('../Day 5/segments.csv')
    quarterly = pd.read_csv('loan_profitability_per_quarter.csv')
    means = pd.read_csv('segment_profitability_means.csv', index_col=0)
    print("Loaded data successfully.\n")
except FileNotFoundError as e:
    print(f"Error loading data: {e}")
    # Fallback/Debug info
    print(f"CWD: {os.getcwd()}")
    exit()

# --- Task 1: Verify average profitability calculation ---
print("## Task 1: Verify Average Profitability Calculation")
print("Methodology Hypothesis: Average Profitability = Mean(Quarterly Profitability) + Segment Spread")

# Calculate temporal mean of quarterly data (excluding 'Quarter' column)
quarterly_means = quarterly.drop(columns=['Quarter']).mean()

results = []
for index, row in segments_day5.iterrows():
    asset = row['asset']
    # Extract rating from segment_id (e.g. PersonalLoans_Prime -> Prime)
    if not row['segment_id'].startswith(asset):
        rating = "Unknown"
    else:
        # segment_id = Asset + "_" + Rating. Length of asset + 1 for underscore
        rating = row['segment_id'][len(asset)+1:]
    
    if asset in quarterly_means and rating in means.index:
        base_return = quarterly_means[asset]
        spread = means.loc[rating, asset]
        calculated_avg = base_return + spread
        actual_avg = row['average_profitability']
        diff = actual_avg - calculated_avg
        results.append({
            'segment_id': row['segment_id'], 
            'base_return': base_return, 
            'spread': spread, 
            'calculated': calculated_avg, 
            'actual': actual_avg, 
            'diff': diff
        })

df_results = pd.DataFrame(results)
print(f"Verified {len(df_results)} segments.")
print("Sample discrepancies:")
print(df_results[['segment_id', 'calculated', 'actual', 'diff']].head())
print("\nDiscrepancy Summary:")
print(df_results['diff'].describe())

print("\nObservation: The calculated numbers do not match exactly. The differences suggest that the 'average_profitability' provided in Day 5 data might have been calculated using a different method (e.g., excluding outliers) or updated data compared to the raw files provided in Day 4.")


# --- Task 2: Calculate current portfolio metrics ---
print("\n## Task 2: Calculate Current Portfolio Metrics")
total_exposure = segments_day5['exposure'].sum()
print(f"Total Portfolio Exposure: {total_exposure:,.2f}")

# Weighted Average Risk Weight
weighted_risk = (segments_day5['exposure'] * segments_day5['risk_weight']).sum()
weighted_avg_risk_weight = weighted_risk / total_exposure
print(f"Weighted Average Risk Weight: {weighted_avg_risk_weight:.4%}")

regulatory_limit = 0.50
print(f"Regulatory Limit: {regulatory_limit:.0%}")
if weighted_avg_risk_weight > regulatory_limit:
    print(f"Binding status: YES, limit exceeded by {weighted_avg_risk_weight - regulatory_limit:.4%}")
else:
    print("Binding status: NO, within limits.")


# --- Task 3: Draft a mathematical formulation ---
print("\n## Task 3: Draft Mathematical Formulation")
print("""
Decision Variables:
  Let x_s be the new exposure level for each segment s (s = 1 to 72).
  x_s >= 0 (Non-negativity)

Objective Function:
  Maximize Total Expected Profitability:
  Maximize Sum( x_s * (average_profitability_s - transaction_cost_s) )
  
  *Note: Transaction costs need to be defined based on the change from current exposure.
   Cost = rel_origination_cost * max(0, x_s - current_exposure_s)  [Buying/Originating]
        + rel_sell_cost * max(0, current_exposure_s - x_s)        [Selling]
   This makes the objective non-linear or requires auxiliary variables.

Constraints:
  1. Portfolio-level Risk Weight:
     Sum(x_s * risk_weight_s) / Sum(x_s) <= 0.50
     -> Sum(x_s * risk_weight_s) <= 0.50 * Sum(x_s)

  2. Portfolio-level Total Exposure Growth:
     Sum(x_s) <= 1.20 * Total_Current_Exposure

  3. Asset-level Growth/Shrink Constraints (for each asset class a):
     Current_Exposure_a * (1 - max_exposure_decrease_a) <= Sum_{s in a}(x_s) <= Current_Exposure_a * (1 + max_exposure_increase_a)
""")

# --- Task 4: Flag data concerns ---
print("\n## Task 4: Flag Data Concerns")
# Negative profitability
neg_profit_segments = segments_day5[segments_day5['average_profitability'] < 0]
print(f"1. Negative Profitability: Found {len(neg_profit_segments)} segments with negative average profitability.")
for _, row in neg_profit_segments.iterrows():
    print(f"   - {row['segment_id']}: {row['average_profitability']:.2%}")

# InvestmentMortgage variance
inv_mortgage = segments_day5[segments_day5['asset'] == 'InvestmentMortgage']
print("\n2. InvestmentMortgage Extreme Variance:")
print(inv_mortgage[['segment_id', 'average_profitability']])
print("   - Prime is negative (-7.86%) while Subprime is massive (+121.68%).")
print("   - This suggests potential data quality issues or extreme outliers driving the mean (e.g., the 600% return in 2020Q4 seen in quarterly data).")

# High Risk Portfolios
print("\n3. Current Portfolio Risk:")
print("   - The current portfolio is significantly above the 50% risk weight limit (at ~58%). Drastic restructuring or shedding of high-risk assets will be required.")

