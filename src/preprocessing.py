import pandas as pd

def preprocess_stock_data(AAPL, MSFT, F, BAC):
    AAPL = AAPL.rename(columns={'Adj Close': 'AAPL Adj Close'})
    MSFT = MSFT.rename(columns={'Adj Close': 'MSFT Adj Close'})
    F = F.rename(columns={'Adj Close': 'F Adj Close'})
    BAC = BAC.rename(columns={'Adj Close': 'BAC Adj Close'})

    allstockdata = pd.concat([AAPL, MSFT, F, BAC], axis=1)
    daily_return = allstockdata.pct_change().dropna()

    return daily_return.rename(columns={
        'AAPL Adj Close': 'AAPL daily return',
        'MSFT Adj Close': 'MSFT daily return',
        'F Adj Close': 'F daily return',
        'BAC Adj Close': 'BAC daily return'
    })

def preprocess_sofr(sofr_raw):
    sofr = sofr_raw.set_index("Tenor").transpose().drop("T")
    sofr.index = pd.to_datetime(sofr.index)
    sofr_change = sofr.diff().dropna()
    return sofr, sofr_change
