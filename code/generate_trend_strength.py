# generate_trend_strength.py
import pandas as pd
import numpy as np
from pathlib import Path

df = pd.read_csv("data/trends_processed.csv")
df['Date'] = pd.to_datetime(df['Date'])

scores=[]
for tech in df['Technology'].unique():
    t = df[df['Technology']==tech].sort_values("Date")
    y = t['Interest'].values
    if len(y) < 5:
        slope = 0.0
    else:
        slope = np.polyfit(np.arange(len(y)), y, 1)[0]
    stability = 1 / (t['Interest'].rolling(14).std().mean() + 1) if len(t) >= 14 else 1/(t['Interest'].std()+1)
    final_score = (slope*10) + (stability*50)
    scores.append([tech, round(final_score,2)])

scores_df = pd.DataFrame(scores, columns=['Technology','Trend_Strength'])
out = Path('outputs/trend_strength.csv')
out.parent.mkdir(parents=True, exist_ok=True)
scores_df.to_csv(out, index=False)
print("Saved:", out)
print(scores_df.to_string(index=False))
