# arima_model.py
import argparse
import pandas as pd
from pathlib import Path
import numpy as np
from sklearn.metrics import mean_squared_error

import pmdarima as pm

def run_arima(input_csv: str, out_csv: str, periods: int = 30):
    df = pd.read_csv(input_csv, parse_dates=['ds'])
    df = df.sort_values('ds')
    ts = df.set_index('ds')['y']

    if len(ts) > 30:
        train_ts = ts.iloc[:-14]
        holdout_ts = ts.iloc[-14:]
    else:
        train_ts = ts
        holdout_ts = None

    model = pm.auto_arima(train_ts, seasonal=False, error_action='ignore', suppress_warnings=True,
                          stepwise=True, max_p=5, max_q=5)
    print(model.summary())

    fc, conf_int = model.predict(n_periods=periods, return_conf_int=True)

    last_date = train_ts.index.max()
    idx = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=periods, freq='D')
    out_df = pd.DataFrame({'ds': idx, 'y_pred': fc, 'y_lower': conf_int[:, 0], 'y_upper': conf_int[:, 1]})

    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_path, index=False)
    print(f"ARIMA forecast saved to {out_path}")

    if holdout_ts is not None:
        in_sample_fc = model.predict(n_periods=len(holdout_ts))
        rmse = np.sqrt(mean_squared_error(holdout_ts.values, in_sample_fc))
        print(f"ARIMA RMSE on holdout: {rmse:.3f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Path to forecast_input.csv')
    parser.add_argument('--out', required=True, help='Path to save arima forecast csv')
    parser.add_argument('--periods', type=int, default=30)
    args = parser.parse_args()
    run_arima(args.input, args.out, periods=args.periods)
