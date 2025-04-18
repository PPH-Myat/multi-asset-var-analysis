import numpy as np
from .swap_pricing import calculate_swap_pv

def historical_var_full(allriskfactors, base_rates, base_pv, notional, strike, tenors, matching_tenors):
    pnl = []
    for _, row in allriskfactors.iterrows():
        shocked = base_rates + row[matching_tenors].values
        pv = calculate_swap_pv(shocked, tenors, notional, strike)
        stock_pnl = (row[["AAPL daily return", "MSFT daily return", "F daily return", "BAC daily return"]].values * 1_000_000).sum()
        pnl.append(pv - base_pv + stock_pnl)
    return np.abs(np.percentile(pnl, 5))

def historical_var_sensitivity(allriskfactors, ak_sensitivity, relevant_factors):
    pnl = allriskfactors[relevant_factors].values @ ak_sensitivity
    return np.abs(np.percentile(pnl, 5))
