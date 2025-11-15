# preprocessing.py
import argparse
import pandas as pd
from pathlib import Path

def preprocess(input_path: str, output_path: str, create_holdout: bool = True, holdout_days: int = 14):
    input_path = Path(input_path)
    output_path = Path(output_path)
    # Auto-detect CSV or Excel
    if input_path.suffix.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path)

    # Expecting 'Date' and 'Interest'
    if 'Date' not in df.columns or 'Interest' not in df.columns:
        raise ValueError("Input file must contain 'Date' and 'Interest' columns.")

    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    # Keep only Date and Interest for forecasting
    df = df[['Date', 'Interest']].copy()
    df = df.sort_values('Date').drop_duplicates('Date')

    # Rename for Prophet convention
    df = df.rename(columns={'Date': 'ds', 'Interest': 'y'})

    # Ensure daily index from min to max
    full_idx = pd.date_range(start=df['ds'].min(), end=df['ds'].max(), freq='D')
    df = df.set_index('ds').reindex(full_idx).rename_axis('ds').reset_index()

    # If y missing, forward-fill then fill remaining with 0
    df['y'] = df['y'].ffill().fillna(0)

    # Save final input
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved forecasting input to {output_path}")

    # Optionally create a holdout file for evaluation (last N days)
    if create_holdout:
        holdout_path = output_path.parent / 'forecast_input_holdout.csv'
        if len(df) > holdout_days:
            train = df.iloc[:-holdout_days]
            holdout = df.iloc[-holdout_days:]
            train.to_csv(output_path, index=False)
            holdout.to_csv(holdout_path, index=False)
            print(f"Created holdout ({holdout_days} days) at {holdout_path}")
        else:
            print("Not enough data to create holdout; whole file saved as training input.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to trends_processed.xlsx or CSV')
    parser.add_argument('--out', required=True, help='Path to save forecast_input.csv')
    parser.add_argument('--no-holdout', action='store_true', help='Do not create holdout file')
    parser.add_argument('--holdout-days', type=int, default=14, help='Days in holdout')
    args = parser.parse_args()
    preprocess(args.input, args.out, create_holdout=not args.no_holdout, holdout_days=args.holdout_days)
