import numpy as np
from scipy.stats import norm

def compute_parametric_var(mean, variance, confidence=0.95):
    z = norm.ppf(1 - confidence)
    return abs(mean + z * np.sqrt(variance))
