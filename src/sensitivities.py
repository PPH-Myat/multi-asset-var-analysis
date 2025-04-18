import numpy as np
import pandas as pd
from .swap_pricing import calculate_swap_pv

def calculate_swap_sensitivity(rates, notional, strike, matching_tenors, tenors):
    original_price_df = pd.DataFrame(index=rates.index, columns=['Swap Base Price'])
    sensitivity_swap_factor = {}
    for start_date in rates.index:
        base_rates = rates.loc[start_date, matching_tenors].astype(float).values
        original_price_df.loc[start_date, 'Swap Base Price'] = calculate_swap_pv(base_rates, tenors, notional, strike)
        sensitivity = pd.Series(0.0, index=matching_tenors)
        for tenor in matching_tenors:
            shifted = rates.loc[start_date].copy()
            shifted[tenor] += 0.0001
            bumped_pv = calculate_swap_pv(shifted[matching_tenors].values, tenors, notional, strike)
            sensitivity[tenor] = (bumped_pv - original_price_df.loc[start_date, 'Swap Base Price']) / 0.0001 * 10000
        sensitivity_swap_factor[start_date] = sensitivity
    return pd.DataFrame.from_dict(sensitivity_swap_factor, orient='index'), original_price_df
