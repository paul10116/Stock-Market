import pandas as pd
import numpy as np
import sqlite3
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///database.db')
index_data = pd.read_sql_query(
    "SELECT * FROM indexes", engine, parse_dates="Date")


def beta(data, ticker):

    spy_ticker1 = pd.concat(
        [index_data.SPY[-500::], data[-500::]], axis=1)
    spy_ticker1.columns = ["SPY", ticker]
    long_data_pct = np.log(spy_ticker1/spy_ticker1.shift())
    ticker1_cov = long_data_pct.cov().iloc[0, 1]
    ticker1_var = long_data_pct["SPY"].var()
    long_beta = ticker1_cov/ticker1_var

    # beta_ticker = yf.Ticker("SPY")
    # spy = beta_ticker.history(start='2020-1-1', actions=False, rounding=True)

    # spy_ticker1 = pd.concat(
    #     [spy.Close[-500::], data[-500::]], axis=1)
    # spy_ticker1.columns = ["SPY", ticker]
    # long_data_pct = np.log(spy_ticker1/spy_ticker1.shift())
    # ticker1_cov = long_data_pct.cov().iloc[0, 1]
    # ticker1_var = long_data_pct["SPY"].var()
    # long_beta = ticker1_cov/ticker1_var

    return long_beta
