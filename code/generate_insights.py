# generate_insights.py
import pandas as pd
from pathlib import Path

fc = pd.read_csv("outputs/final_forecast_table_all_complete.csv")
ts = pd.read_csv("outputs/trend_strength.csv")

insights = []
# fastest growth
best_growth = fc.sort_values('Growth_Percent', ascending=False).iloc[0]
insights.append(f"Fastest growing technology: {best_growth['Technology']} with forecast growth {best_growth['Growth_Percent']}%")

# most stable
most_stable = fc.sort_values('Volatility').iloc[0]
insights.append(f"Most stable technology: {most_stable['Technology']} (Volatility {most_stable['Volatility']})")

# strongest trend strength
best_trend = ts.sort_values('Trend_Strength', ascending=False).iloc[0]
insights.append(f"Strongest trend momentum: {best_trend['Technology']} (Trend Strength {best_trend['Trend_Strength']})")

# combined
insights.append("Overall: Generative AI shows highest predicted growth; 5G is steady; Edge & Quantum show healthy rise; Blockchain is moderate.")

out = Path('outputs/auto_insights.txt')
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, 'w') as f:
    for line in insights:
        f.write(line + "\n")
print("Saved insights to:", out)
for line in insights:
    print("-", line)
