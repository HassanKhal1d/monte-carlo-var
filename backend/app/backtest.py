# backend/app/backtest.py
import numpy as np
from scipy import stats
import pandas as pd

def ks_test_sim_vs_hist(simulated_returns, historical_returns):
    sim = np.asarray(simulated_returns).ravel()
    hist = np.asarray(historical_returns).ravel()
    stat, pvalue = stats.ks_2samp(sim, hist)
    return {"ks_stat": float(stat), "p_value": float(pvalue)}

def rolling_var_coverage(historical_prices, model_func, window_days=252, n_sims=5000, horizon_days=1):
    # historical_prices: pd.Series indexed by date
    results = []
    for i in range(window_days, len(historical_prices)-horizon_days):
        train = historical_prices.iloc[i-window_days:i]
        test = historical_prices.iloc[i:i+horizon_days]
        # Estimate
        log_ret = np.log(train / train.shift(1)).dropna()
        mu = float(log_ret.mean() * 252)
        sigma = float(log_ret.std(ddof=1) * (252**0.5))
        s0 = float(train.iloc[-1])
        paths = model_func(s0=s0, mu=mu, sigma=sigma, horizon_days=horizon_days, n_sims=n_sims)
        terminal_returns = paths[:, -1] / paths[:, 0] - 1.0
        # compute 95% VaR loss threshold
        var95 = float(np.percentile(-terminal_returns, 95.0))
        realized = float(test.iloc[-1] / s0 - 1.0)
        breach = 1 if (-realized) >= var95 else 0
        results.append({"date": test.index[-1], "realized": realized, "var95": var95, "breach": breach})
    return pd.DataFrame(results)

