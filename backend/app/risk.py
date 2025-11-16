# backend/app/risk.py
import numpy as np

def terminal_returns_from_paths(paths):
    # returns as simple returns terminal/S0 - 1
    s0 = paths[:, 0]
    terminal = paths[:, -1]
    returns = terminal / s0 - 1.0
    return returns

def var_cvar(returns, alpha=0.95):
    # returns = array of returns; losses = -returns
    losses = -returns
    var = float(np.percentile(losses, 100.0 * alpha))
    tail = losses[losses >= var]
    cvar = float(tail.mean()) if tail.size > 0 else var
    return {"VaR": var, "CVaR": cvar}

def summary_stats(returns):
    return {"mean": float(np.mean(returns)), "std": float(np.std(returns, ddof=1)),
            "quantiles": {"5%": float(np.quantile(returns, 0.05)), "95%": float(np.quantile(returns, 0.95))}}

