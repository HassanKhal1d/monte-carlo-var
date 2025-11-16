# backend/app/simulator.py
"""
Simulator: GBM + Merton jump-diffusion.
All functions return numpy arrays; documented and simple.
"""
import numpy as np
import pandas as pd

def estimate_parameters_from_csv(csv_path="backend/app/data/spy.csv"):
    df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    adj = df['Adj Close'].dropna()
    log_ret = np.log(adj / adj.shift(1)).dropna()
    mu = float(log_ret.mean() * 252)         # annualized drift
    sigma = float(log_ret.std(ddof=1) * (252**0.5))  # annualized vol
    s0 = float(adj.iloc[-1])
    return {"mu": mu, "sigma": sigma, "s0": s0, "log_ret": log_ret}

def simulate_gbm_paths(s0, mu, sigma, horizon_days, n_sims, seed=None):
    if seed is not None:
        np.random.seed(seed)
    dt = 1.0 / 252.0
    steps = horizon_days
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * (dt**0.5)
    paths = np.zeros((n_sims, steps + 1))
    paths[:, 0] = s0
    Z = np.random.normal(size=(n_sims, steps))
    for t in range(steps):
        paths[:, t+1] = paths[:, t] * np.exp(drift + diffusion * Z[:, t])
    return paths

def simulate_jump_diffusion(s0, mu, sigma, horizon_days, n_sims,
                            jump_lambda=0.02, jump_mu=-0.02, jump_sigma=0.05, seed=None):
    if seed is not None:
        np.random.seed(seed)
    dt = 1.0 / 252.0
    steps = horizon_days
    paths = np.zeros((n_sims, steps + 1))
    paths[:, 0] = s0
    Z = np.random.normal(size=(n_sims, steps))
    for t in range(steps):
        Nj = np.random.poisson(lam=jump_lambda, size=n_sims)
        J = np.zeros(n_sims)
        idx = Nj > 0
        if idx.any():
            # sum Nj normal draws for each sim with Nj>0
            for i in np.where(idx)[0]:
                J[i] = np.random.normal(loc=jump_mu, scale=jump_sigma, size=Nj[i]).sum()
        kappa = np.exp(jump_mu + 0.5 * jump_sigma**2) - 1.0
        drift = (mu - 0.5 * sigma**2 - jump_lambda * kappa) * dt
        diffusion = sigma * (dt**0.5) * Z[:, t]
        paths[:, t+1] = paths[:, t] * np.exp(drift + diffusion + J)
    return paths

