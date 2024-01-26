import pandas as pd
import  sqlalchemy
import numpy as np
from tickers import mid_cap_and_above,  xlb, xle, xli, xlu, xlk, xly, xlp, xlv, xlf, xlre, xlc

engine = sqlalchemy.create_engine('sqlite:///stock_etf.db')


dataframe = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

corr_check = pd.concat(
                    [dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr(method='spearman').iloc[0, 1].round(2)