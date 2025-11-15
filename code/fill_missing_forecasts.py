# fill_missing_forecasts.py
# Add synthetic forecasts for technologies missing ARIMA output.

import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression

DATA = Path("data/trends_processed.csv")
OUT_DIR = Path("outputs")
ARIMA_DIR = Path("outputs")
OUT_FILE = OUT_DIR / "final_forecast_table_all_complete.csv"

df = pd.read_csv(DATA)
df["Date"] = pd.to_datetime(df["Date"])

techs = ["Generative AI", "Blockchain", "Quantum Computing", "Edge Computing", "5G"]

rows = []

for tech in techs:
    print("\nProcessing:", tech)

    df_t = df[df["Technology"] == tech].sort_values("Date").reset_index(drop=True)

    # current value
    current_value = float(df_t["Interest"].iloc[-1])

    # check if ARIMA forecast exists
    safe = "".join(x if x.isalnum() else "_" for x in tech)
    arima_path = OUT_DIR / f"{safe}_arima_forecast.csv"

    if arima_path.exists():
        # load ARIMA forecast
        fc = pd.read_csv(arima_path)
        forecast_value = float(fc["y_pred"].iloc[0])
        trend_dir = "Up" if forecast_value > current_value else "Down"
        growth_pct = ((forecast_value - current_value) / current_value) * 100
        print("✔ ARIMA forecast used")

    else:
        print("⚠ ARIMA missing → Using synthetic regression forecast")

        # use last 60 days for regression
        df_last = df_t.tail(60)
        df_last["t"] = np.arange(len(df_last)).reshape(-1, 1)

        model = LinearRegression()
        model.fit(df_last["t"].values.reshape(-1, 1), df_last["Interest"])

        future_t = np.array([[len(df_last) + 1]])
        forecast_value = float(model.predict(future_t)[0])

        trend_dir = "Up" if forecast_value > current_value else "Down"
        growth_pct = ((forecast_value - current_value) / current_value) * 100

    # volatility
    if len(df_t) > 7:
        vol = float(df_t["Interest"].rolling(7).std().dropna().iloc[-1])
    else:
        vol = float(df_t["Interest"].std())

    rows.append({
        "Technology": tech,
        "Current_Value": round(current_value, 3),
        "Forecast_Value": round(forecast_value, 3),
        "Growth_Percent": round(growth_pct, 3),
        "Trend_Direction": trend_dir,
        "Volatility": round(vol, 3)
    })

final_df = pd.DataFrame(rows)
final_df["Rank"] = final_df["Growth_Percent"].rank(ascending=False).astype(int)
final_df = final_df.sort_values("Rank")

final_df.to_csv(OUT_FILE, index=False)
print("\n✅ Final complete table saved to:", OUT_FILE)
print(final_df.to_string(index=False))
