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

## Project Workflow

1. **Preprocess the Market Data**
   - Compute daily returns for equities and daily changes for SOFR zero rates.
   - Merge into a unified dataset of 34 risk factors.
   - Interpolate missing data points linearly.

2. **Swap Pricing & Sensitivity**
   - Calculate present value of the 10Y payer SOFR swap.
   - Estimate the PV01 vector (rate sensitivities) using bump-and-reprice.

3. **Value-at-Risk Modeling**
   - Compute Parametric VaR based on portfolio variance and expected return.
   - Run Monte Carlo simulations:
     - Full revaluation: simulate future returns using a multivariate normal distribution; reprice the swap under each simulated scenario.
     - Sensitivity-based: estimate swap PnL using the dot product of PV01 and rate shocks.
   - Apply Historical VaR using actual past risk factor changes:
     - Full revaluation: shift the SOFR curve by historical deltas and reprice the swap.
     - Sensitivity-based: approximate PnL using PV01 × historical changes in zero rates.

4. **Compare Results**
   - Print all 1-day 95% VaR results across all models.
   - Evaluate consistency, model assumptions, and sensitivity of outcomes.

## Data Used

- 1 year of historical SOFR curve data
- Stock price data (31/10/2022 - 30/10/2023)
- Provided Excel-based swap pricer for full revaluation

## How to Run

Follow these steps to set up and run the project locally:

### 1. Clone the Repository

```bash
git clone https://github.com/PPH-Myat/multi-asset-var-analysis.git
cd multi-asset-var-analysis
```
### 2. Set Up Python Environment
Make sure you have Python 3.10+ installed. Then install all required dependencies:

```bash
pip install -r requirements.txt
```
### 3. Prepare the Excel File
Place the Excel file in the following path:

```bash
data/hist_data.xlsm
```
The file must include the following sheets:
- `SofrCurve` — daily SOFR curve (with tenor columns and date rows)
- `AAPL`, `MSFT`, `F`, and `BAC` — each with:
  - `Date` column  
  - `Adj Close` column (for adjusted closing prices)


### 4. Run the Main Script
From the root directory, execute:

```bash
python main.py
```
### 5. Output
You will see results printed in the terminal like this:

```bash
----- 1-Day 95% Value at Risk (VaR) Summary -----
Parametric VaR: $X,XXX,XXX.XX
Monte Carlo VaR (Full Revaluation): $X,XXX,XXX.XX
Monte Carlo VaR (Sensitivity-Based): $X,XXX,XXX.XX
Historical VaR (Full Revaluation): $X,XXX,XXX.XX
Historical VaR (Sensitivity-Based): $X,XXX,XXX.XX
```

## Academic Context

> This project was submitted as part of the QF609 (AY2024-2025) group assignment at Singapore Management University.

## Acknowledgements

> Baseline modeling references and data templates provided by the professor and senior cohorts. Modified and extended by our team for educational use.

