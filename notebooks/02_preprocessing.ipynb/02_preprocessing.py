# -----------------------------------------------------------
# TRENDPULSE AI – PHASE 3: CLEAN + PREPROCESS (FINAL VERSION)
# -----------------------------------------------------------

import pandas as pd
import numpy as np

# STEP 1: LOAD RAW DATA
df = pd.read_csv("C:/trenspulseai1/data/trends_raw.csv")

df = df.rename(columns={"date": "Date", df.columns[1]: "Interest", "technology": "Technology"})
df["Date"] = pd.to_datetime(df["Date"])

# STEP 2: REMOVE FUTURE DATES & EMPTY VALUES
df = df.dropna(subset=["Interest"])  # Remove rows where Google Trends gave blank

max_valid_date = df["Date"].max()
df = df[df["Date"] <= max_valid_date]  # Keep only real valid dates

# STEP 3: SORT DATA
df = df.sort_values(by=["Technology", "Date"])

# STEP 4: FIX MISSING VALUES (Forward + Backward Fill)
df["Interest"] = df.groupby("Technology")["Interest"].transform(
    lambda x: x.ffill().bfill()
)

# STEP 5: FEATURE ENGINEERING
df["MA7"] = df.groupby("Technology")["Interest"].transform(lambda x: x.rolling(7, min_periods=1).mean())
df["MA30"] = df.groupby("Technology")["Interest"].transform(lambda x: x.rolling(30, min_periods=1).mean())

df["Pct_Change"] = df.groupby("Technology")["Interest"].pct_change(fill_method=None).fillna(0)

df["Volatility"] = df.groupby("Technology")["Interest"].transform(
    lambda x: x.rolling(7, min_periods=1).std()
)

df["Trend_Direction"] = df["Pct_Change"].apply(
    lambda x: "Up" if x > 0 else ("Down" if x < 0 else "Stable")
)

# STEP 6: DATE FEATURES
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Week"] = df["Date"].dt.isocalendar().week

# STEP 7: FINAL ORDER
df = df[
    ["Date", "Technology", "Interest",
     "MA7", "MA30", "Pct_Change", "Volatility", "Trend_Direction",
     "Year", "Month", "Week"]
]

# STEP 8: SAVE FINAL FILE
df.to_csv("C:/trenspulseai1/data/trends_processed.csv", index=False)

print("\n🎉 PREPROCESSING FIXED & COMPLETE!")
print("📁 Saved file: C:/trenspulseai1/data/trends_processed.csv")
print(df.tail())
