# -----------------------------------------------------------
# TRENDPULSE AI – PHASE 4: EXPLORATORY DATA ANALYSIS (EDA)
# -----------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load preprocessed data
df = pd.read_csv("C:/trenspulseai1/data/trends_processed.csv")

print("Data Loaded for EDA:")
print(df.head())

# Set style
sns.set(style="whitegrid")

# -----------------------------------------------------------
# 1. MULTI-LINE TREND CHART (All Technologies)
# -----------------------------------------------------------
plt.figure(figsize=(14, 6))
for tech in df["Technology"].unique():
    temp = df[df["Technology"] == tech]
    plt.plot(temp["Date"], temp["Interest"], label=tech)

plt.title("Technology Search Interest Over Time (Trend Comparison)", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Search Interest")
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# 2. INDIVIDUAL TECHNOLOGY TRENDS
# -----------------------------------------------------------
unique_tech = df["Technology"].unique()

for tech in unique_tech:
    temp = df[df["Technology"] == tech]

    plt.figure(figsize=(12, 5))
    plt.plot(temp["Date"], temp["Interest"], label="Interest", color="blue")
    plt.plot(temp["Date"], temp["MA7"], label="MA7", linestyle="--")
    plt.plot(temp["Date"], temp["MA30"], label="MA30", linestyle="--")

    plt.title(f"{tech} – Trend with Moving Averages", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Search Interest")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------------------------------------
# 3. VOLATILITY PLOT
# -----------------------------------------------------------
plt.figure(figsize=(14, 6))
for tech in unique_tech:
    temp = df[df["Technology"] == tech]
    plt.plot(temp["Date"], temp["Volatility"], label=tech)

plt.title("Volatility of Technologies Over Time", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.legend()
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# 4. PERCENT CHANGE DISTRIBUTION
# -----------------------------------------------------------
plt.figure(figsize=(14, 6))
sns.boxplot(data=df, x="Technology", y="Pct_Change")
plt.title("Distribution of Percent Change by Technology", fontsize=14)
plt.xlabel("Technology")
plt.ylabel("Percent Change")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# 5. CORRELATION HEATMAP
# -----------------------------------------------------------
pivot_df = df.pivot_table(values="Interest", index="Date", columns="Technology")
corr_matrix = pivot_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Between Technologies", fontsize=14)
plt.tight_layout()
plt.show()

# -----------------------------------------------------------
# 6. TREND DIRECTION COUNTS
# -----------------------------------------------------------
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="Technology", hue="Trend_Direction")
plt.title("Trend Direction Distribution", fontsize=14)
plt.xlabel("Technology")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n🎉 EDA COMPLETE!")
