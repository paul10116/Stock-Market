import yfinance as yf
import pandas as pd
import numpy as np


def beta(data, ticker):

    beta_ticker = yf.Ticker("SPY")
    spy = beta_ticker.history(start='2020-1-1', actions=False, rounding=True)

    spy_ticker1 = pd.concat(
        [spy.Close[-500::], data[-500::]], axis=1)
    spy_ticker1.columns = ["SPY", ticker]
    long_data_pct = np.log(spy_ticker1/spy_ticker1.shift())
    ticker1_cov = long_data_pct.cov().iloc[0, 1]
    ticker1_var = long_data_pct["SPY"].var()
    long_beta = ticker1_cov/ticker1_var

    return long_beta
