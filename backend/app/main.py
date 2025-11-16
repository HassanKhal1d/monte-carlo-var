# backend/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import numpy as np

from simulator import estimate_parameters_from_csv, simulate_jump_diffusion, simulate_gbm_paths
from risk import terminal_returns_from_paths, var_cvar, summary_stats
from backtest import ks_test_sim_vs_hist

app = FastAPI(title="Monte Carlo VaR API")

class SimRequest(BaseModel):
    s0: Optional[float] = None
    horizon_days: int = 1
    n_sims: int = 20000
    jump_lambda: float = 0.02
    jump_mu: float = -0.02
    jump_sigma: float = 0.05
    seed: Optional[int] = None
    use_jump: bool = True

@app.post("/simulate")
def simulate(req: SimRequest):
    params = estimate_parameters_from_csv()
    s0 = req.s0 or params["s0"]
    mu = params["mu"]
    sigma = params["sigma"]
    if req.use_jump:
        paths = simulate_jump_diffusion(s0=s0, mu=mu, sigma=sigma,
                                        horizon_days=req.horizon_days, n_sims=req.n_sims,
                                        jump_lambda=req.jump_lambda, jump_mu=req.jump_mu,
                                        jump_sigma=req.jump_sigma, seed=req.seed)
    else:
        paths = simulate_gbm_paths(s0=s0, mu=mu, sigma=sigma,
                                   horizon_days=req.horizon_days, n_sims=req.n_sims, seed=req.seed)
    returns = terminal_returns_from_paths(paths)
    risk = var_cvar(returns, alpha=0.95)
    stats = summary_stats(returns)
    # send back a small sample of paths for plotting
    sample_idx = np.random.choice(paths.shape[0], size=min(200, paths.shape[0]), replace=False)
    sample_paths = paths[sample_idx, :].tolist()
    return {"n_sims": req.n_sims, "horizon_days": req.horizon_days, "risk": risk, "stats": stats, "paths": sample_paths}

@app.post("/ks_test")
def ks_test(sim_returns: list, hist_returns: list):
    return ks_test_sim_vs_hist(sim_returns, hist_returns)

