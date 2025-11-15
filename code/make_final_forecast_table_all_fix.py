# make_final_forecast_table_all_fix.py
# Read per-tech ARIMA forecast CSVs (already saved) and build final table for Power BI.

import pandas as pd
from pathlib import Path
import numpy as np

DATA_PATH = Path('data/trends_processed.csv')
OUTPUT_DIR = Path('outputs')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = [c.strip() for c in df.columns]

if 'Technology' not in df.columns:
    raise ValueError("data/trends_processed.csv must have 'Technology' column")

techs = df['Technology'].unique().tolist()
final_rows = []

for tech in techs:
    safe_name = "".join(x if x.isalnum() else "_" for x in tech)[:40]
    per_path = OUTPUT_DIR / f"{safe_name}_arima_forecast.csv"
    if not per_path.exists():
        print(f"Warning: forecast file not found for {tech}: {per_path}")
        continue

    # read saved forecast csv
    fc = pd.read_csv(per_path, parse_dates=['ds'])
    if 'y_pred' not in fc.columns:
        print(f"Warning: 'y_pred' not in {per_path}, skipping")
        continue

    # pick the first forecasted day value robustly
    try:
        forecast_value = float(fc['y_pred'].iloc[0])
    except Exception:
        forecast_value = float(np.asarray(fc['y_pred']).ravel()[0])

    tdf = df[df['Technology'] == tech].sort_values('Date')
    tdf['Date'] = pd.to_datetime(tdf['Date'], errors='coerce')
    tdf = tdf.dropna(subset=['Date'])
    # current value = last available Interest
    current_value = float(tdf['Interest'].dropna().iloc[-1])

    growth_pct = ((forecast_value - current_value) / current_value) * 100 if current_value != 0 else np.nan
    trend_dir = "Up" if forecast_value > current_value else "Down" if forecast_value < current_value else "Stable"
    vol = float(tdf['Interest'].rolling(7).std().dropna().iloc[-1]) if len(tdf['Interest'])>=7 else float(tdf['Interest'].std())

    final_rows.append({
        'Technology': tech,
        'Current_Value': round(current_value,3),
        'Forecast_Value': round(forecast_value,3),
        'Growth_Percent': round(growth_pct,3),
        'Trend_Direction': trend_dir,
        'Volatility': round(vol,3)
    })

final_df = pd.DataFrame(final_rows)
final_df['Rank'] = final_df['Growth_Percent'].rank(ascending=False, method='min').astype(int)
final_df = final_df.sort_values('Rank')
out_path = OUTPUT_DIR / 'final_forecast_table_all.csv'
final_df.to_csv(out_path, index=False)
print("✅ Final forecast table saved:", out_path)
print(final_df.to_string(index=False))
