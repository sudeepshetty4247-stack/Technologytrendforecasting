# generate_sentiment.py
import pandas as pd
from pathlib import Path

sent = pd.DataFrame({
    'Technology': ['Generative AI','Blockchain','Quantum Computing','Edge Computing','5G'],
    'News_Sentiment': ['Positive','Neutral','Positive','Neutral','Positive']
})
out = Path('outputs/news_sentiment.csv')
out.parent.mkdir(parents=True, exist_ok=True)
sent.to_csv(out, index=False)
print("Saved:", out)
print(sent.to_string(index=False))
