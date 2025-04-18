import pandas as pd

def load_data(filepath="data/hist_data.xlsm"):
    sofr = pd.read_excel(filepath, sheet_name="SofrCurve")
    AAPL = pd.read_excel(filepath, sheet_name="AAPL").set_index('Date')
    MSFT = pd.read_excel(filepath, sheet_name="MSFT").set_index('Date')
    F = pd.read_excel(filepath, sheet_name="F").set_index('Date')
    BAC = pd.read_excel(filepath, sheet_name="BAC").set_index('Date')
    return sofr, AAPL, MSFT, F, BAC
