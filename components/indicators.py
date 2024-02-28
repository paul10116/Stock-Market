import pandas as pd
import numpy as np
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///stock_etf.db')
index_data = pd.read_sql_query("SELECT * FROM ETF", engine, parse_dates="Date")


def beta(data: pd.DataFrame, ticker: str) -> float:

    spy_ticker1 = pd.concat(
        [index_data.SPY[-500::], data[-500::]], axis=1)
    spy_ticker1.columns = ["SPY", ticker]
    long_data_pct = np.log(spy_ticker1/spy_ticker1.shift())
    ticker1_cov = long_data_pct.cov().iloc[0, 1]
    ticker1_var = long_data_pct["SPY"].var()
    stock_beta = ticker1_cov/ticker1_var

    return stock_beta


def EMA(data: pd.DataFrame, period: int) -> pd.DataFrame:
    exp_moving_avg = data.ewm(span=period, adjust=False).mean()
    return exp_moving_avg
