# multi-asset-var-analysis
 Quantitative analysis of 1-day 95% Value-at-Risk (VaR) for a multi-asset portfolio using parametric, historical, and Monte Carlo simulation methods. Assets include a SOFR interest rate swap and equity positions in AAPL, MSFT, Ford, and Bank of America.

---

# Quantitative Risk Modeling: Portfolio VaR Estimation

This project calculates the 1-day 95% Value-at-Risk (VaR) of a mixed asset portfolio containing a SOFR swap and equity positions (AAPL, MSFT, F, BAC), using three major VaR methodologies:

## Methods Implemented

- Parametric VaR (Variance-Covariance)
- Monte Carlo VaR  
  - Full Revaluation  
  - Sensitivity-Based
- Historical VaR  
  - Full Revaluation  
  - Sensitivity-Based

## Portfolio Overview

- 10Y Payer SOFR Swap ($100M notional, 4.2% strike)
- Equity: $1M each in AAPL, MSFT, Ford, and Bank of America

## Data Used

- 1 year of historical SOFR curve data
- Stock price data (31/10/2022 - 30/10/2023)
- Provided Excel-based swap pricer for full revaluation

## How to Run

Coming soon — depends on your setup. Add instructions for:
- Notebooks
- Dependencies (`requirements.txt`)
- Any Excel files or macros if applicable

## Academic Context

> This project was submitted as part of the QF609 (AY2024-2025) group assignment at Singapore Managment University.

## Acknowledgements

> Baseline modeling references and data templates provided by course instructors and senior cohorts. Modified and extended by our team for educational use.
