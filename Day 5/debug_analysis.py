import pandas as pd
import numpy as np
import os

# Load Data
base_dir = r"c:\Users\USER\Downloads\Advent of OR"
day4_dir = os.path.join(base_dir, "Day 4")
day5_dir = os.path.join(base_dir, "Day 5")

try:
    segments = pd.read_csv(os.path.join(day5_dir, "segments.csv"))
    assets = pd.read_csv(os.path.join(day5_dir, "assets.csv"))
    # Quarterly and Means are from Day 4
    quarterly = pd.read_csv(os.path.join(day4_dir, "loan_profitability_per_quarter.csv"))
    means = pd.read_csv(os.path.join(day4_dir, "segment_profitability_means.csv"), index_col=0)
except Exception as e:
    print(f"Error loading files: {e}")
    exit()

print("--- Task 1: Verify Average Profitability ---")

# Calculate temporal mean of quarterly data
quarterly_means = quarterly.drop(columns=['Quarter']).mean()
print("\nQuarterly Means (from loan_profitability_per_quarter.csv):")
print(quarterly_means.head())

print("\nTesting Hypothesis: segments.avg = quarterly_mean + segment_mean")
results = []
for index, row in segments.iterrows():
    asset = row['asset']
    if not row['segment_id'].startswith(asset):
        rating = "Unknown"
    else:
        rating = row['segment_id'][len(asset)+1:]
    
    if asset in quarterly_means and asset in means.columns and rating in means.index:
        q_mean = quarterly_means[asset]
        s_mean = means.loc[rating, asset]
        calc = q_mean + s_mean
        actual = row['average_profitability']
        diff = actual - calc
        results.append({'id': row['segment_id'], 'q_mean': q_mean, 's_mean': s_mean, 'calc': calc, 'actual': actual, 'diff': diff})

results_df = pd.DataFrame(results)
print(results_df.head(10))
if not results_df.empty:
    print("\nSummary of Diffs:")
    print(results_df['diff'].describe())

print("\n--- Task 2: Portfolio Metrics ---")
total_exposure = segments['exposure'].sum()
print(f"Total Exposure: {total_exposure:,.2f}")

weighted_risk_sum = (segments['exposure'] * segments['risk_weight']).sum()
weighted_avg_risk = weighted_risk_sum / total_exposure
print(f"Weighted Average Risk Weight: {weighted_avg_risk:.4f} (Constraint <= 0.50)")

if weighted_avg_risk <= 0.50:
    print("Regulatory constraint NOT binding (OK).")
else:
    print("Regulatory constraint IS binding (Violation).")

print("\n--- Task 4: Data Concerns ---")
# Check for negative average profitability
neg_profits = segments[segments['average_profitability'] < 0]
if not neg_profits.empty:
    print(f"\nFound {len(neg_profits)} segments with negative average profitability:")
    print(neg_profits[['segment_id', 'average_profitability']])

# Check for InvestmentMortgage variance
inv_mort = segments[segments['asset'] == 'InvestmentMortgage']
print("\nInvestmentMortgage stats:")
print(inv_mort[['segment_id', 'exposure', 'average_profitability', 'risk_weight']])

print("\nSpecific Check for InvestmentMortgage_Prime:")
# Check Calculation for InvestmentMortgage_Prime
if 'InvestmentMortgage' in quarterly_means:
    im_q_mean = quarterly_means['InvestmentMortgage']
    im_s_mean = means.loc['Prime', 'InvestmentMortgage']
    im_calc = im_q_mean + im_s_mean
    print(f"InvestmentMortgage_Prime Calc: {im_calc:.4f} (Q={im_q_mean:.4f}, S={im_s_mean:.4f})")
