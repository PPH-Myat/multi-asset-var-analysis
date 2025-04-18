import numpy as np
from statistics import NormalDist
from .swap_pricing import calculate_swap_pv

def generate_correlated_normals(n_sim, mu, sigma, corr_mat):
    uniforms = np.random.uniform(size=(n_sim, len(mu)))
    snorms = np.array([[NormalDist().inv_cdf(u) for u in row] for row in uniforms])
    factor_loadings = np.linalg.cholesky(corr_mat)
    correlated = np.dot(snorms, factor_loadings.T)
    return mu + sigma * correlated

def pnl1d_full(sim_data, base_rates, tenors, notional, strike, base_pv):
    stock_cols = ["AAPL daily return", "MSFT daily return", "F daily return", "BAC daily return"]
    stock_pnl = (sim_data[stock_cols].values * 1_000_000).sum(axis=1)
    swap_pnl = np.array([
        calculate_swap_pv(
            base_rates + sim_data.iloc[i][tenors].values,
            np.arange(1, 11),  # map '1Y'...'10Y' to 1...10
            notional,
            strike
        ) - base_pv for i in range(len(sim_data))
    ])
    return stock_pnl + swap_pnl
