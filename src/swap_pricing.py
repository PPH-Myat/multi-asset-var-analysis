import numpy as np

def calculate_swap_pv(rates, tenors, notional, strike):
    discount_factors = np.exp(-rates * tenors)
    float_leg = notional * (1 - discount_factors[-1])
    fixed_cashflows = notional * strike
    fix_leg = np.sum(fixed_cashflows * discount_factors)
    return float_leg - fix_leg

