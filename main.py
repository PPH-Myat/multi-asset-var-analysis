import numpy as np
import pandas as pd

from src.load_data import load_data
from src.preprocessing import preprocess_stock_data, preprocess_sofr
from src.swap_pricing import calculate_swap_pv
from src.sensitivities import calculate_swap_sensitivity
from src.parametric_var import compute_parametric_var
from src.montecarlo_var import generate_correlated_normals, pnl1d_full
from src.historical_var import historical_var_full, historical_var_sensitivity

# Load and preprocess data
sofr_raw, AAPL, MSFT, F, BAC = load_data()
stock_returns = preprocess_stock_data(AAPL, MSFT, F, BAC)
sofr, sofr_diff = preprocess_sofr(sofr_raw)

# Construct risk factor matrix
allriskfactors = pd.concat([stock_returns, sofr_diff], axis=1).loc['2022-10-31':'2023-10-30']
allriskfactors = allriskfactors.interpolate(method='linear', limit_direction='both')

# Setup parameters
matching_tenors = ['1Y', '2Y', '3Y', '4Y', '5Y', '6Y', '7Y', '8Y', '9Y', '10Y']
tenors = np.arange(1, 11)
base_rates = sofr.loc['2023-10-30', matching_tenors].astype(float).values
swap_notional = 100e6
strike = 0.042

# Base swap PV
base_pv = calculate_swap_pv(base_rates, tenors, swap_notional, strike)

# Sensitivities
sofr_sensitivity, _ = calculate_swap_sensitivity(sofr, swap_notional, strike, matching_tenors, tenors)
stock_sensitivity = np.array([1e6] * 4)
ak_sensitivity = np.concatenate([sofr_sensitivity[matching_tenors].mean() / 10000, stock_sensitivity])
relevant_factors = ['AAPL daily return', 'MSFT daily return', 'F daily return', 'BAC daily return'] + matching_tenors

# Parametric VaR
mean_swap = (sofr_sensitivity[matching_tenors].shift(1) / 10000 * sofr_diff[matching_tenors]).sum(axis=1).mean()
mean_stock = np.dot(stock_sensitivity, allriskfactors[relevant_factors[:4]].mean())
portfolio_mean = mean_swap + mean_stock

cov_stocks = allriskfactors[relevant_factors[:4]].cov()
cov_swap = allriskfactors[matching_tenors].cov()
var_stock = stock_sensitivity @ cov_stocks @ stock_sensitivity.T
var_swap = (sofr_sensitivity[matching_tenors].mean() / 10000) @ cov_swap @ (sofr_sensitivity[matching_tenors].mean() / 10000).T
portfolio_variance = var_stock + var_swap

parametric_var = compute_parametric_var(portfolio_mean, portfolio_variance)

# Monte Carlo VaR (Full)
mu_all = allriskfactors.mean().values
sigma_all = allriskfactors.std().values
corr_mat = allriskfactors.corr().values

simulated_returns = generate_correlated_normals(10_000, mu_all, sigma_all, corr_mat)
simulated_df = pd.DataFrame(simulated_returns, columns=allriskfactors.columns)
simulated_pnl = pnl1d_full(simulated_df, base_rates, matching_tenors, swap_notional, strike, base_pv)
mc_var_full = np.abs(np.percentile(simulated_pnl, 5))

# Monte Carlo VaR (Sensitivity-based)
cov_total = np.block([
    [cov_stocks, np.zeros((4, len(matching_tenors)))],
    [np.zeros((len(matching_tenors), 4)), cov_swap]
])
simulated_shocks = np.random.randn(10_000, len(ak_sensitivity)) @ np.linalg.cholesky(cov_total).T
mc_var_sen = np.abs(np.percentile(simulated_shocks @ ak_sensitivity, 5))

# Historical VaR (Full and Sensitivity-based)
hist_var_full = historical_var_full(allriskfactors, base_rates, base_pv, swap_notional, strike, tenors, matching_tenors)
hist_var_sen = historical_var_sensitivity(allriskfactors, ak_sensitivity, relevant_factors)

# Output
print("----- 1-Day 95% Value at Risk (VaR) Summary -----")
print(f"Parametric VaR: ${parametric_var:,.2f}")
print(f"Monte Carlo VaR (Full Revaluation): ${mc_var_full:,.2f}")
print(f"Monte Carlo VaR (Sensitivity-Based): ${mc_var_sen:,.2f}")
print(f"Historical VaR (Full Revaluation): ${hist_var_full:,.2f}")
print(f"Historical VaR (Sensitivity-Based): ${hist_var_sen:,.2f}")
