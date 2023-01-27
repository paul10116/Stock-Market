import yfinance as yf
from datetime import date
import pandas as pd
from plotly import tools
import plotly.graph_objs as go
from tickers import *
import sqlite3
import sqlalchemy
from indicators import beta

start_date = date.fromisoformat("2015-01-03")
engine = sqlalchemy.create_engine('sqlite:///database.db')
data = pd.read_sql_query(
    "SELECT * FROM stockData", engine, parse_dates="Date")


def pair(longs, shorts):

    longArray = longs.split()
    shortArray = shorts.split()

    for buy_ticker in longArray:

        for sell_ticker in shortArray:

            if buy_ticker != sell_ticker:
                dataframe = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

                corr_check = pd.concat(
                    [dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr().iloc[0, 1].round(2)

                print(
                    f"{buy_ticker} / {sell_ticker} CORR = {corr_check}")
                if corr_check > 0.3 or corr_check < -0.3:
                    data = pd.DataFrame({
                        'ratio': (dataframe[buy_ticker]/dataframe[sell_ticker]).round(3),
                        'spread': (dataframe[buy_ticker]-dataframe[sell_ticker]).round(2)
                    })

                    if data.iloc[-1, 0] > 0.4 or data.iloc[-1, 0] < 3:
                        data['spreadMA200'] = data['spread'].rolling(
                            200).mean().round(2)
                        data['ratioMA200'] = data['ratio'].rolling(
                            200).mean().round(2)

                        if data.iloc[-1, 0] > data.iloc[-1, 2] and data.iloc[-1, 1] > data.iloc[-1, 3]:

                            data["spreadMA60"] = data.spread.rolling(
                                60).mean().round(2)
                            data["spreadMA20"] = data.spread.rolling(
                                20).mean().round(2)

                            if data.iloc[-1, 5] < data.iloc[-1, 4]:

                                sub_trace1 = go.Scatter(x=dataframe.Date,
                                                        y=dataframe[buy_ticker], mode='lines', name=buy_ticker)
                                sub_trace2 = go.Scatter(x=dataframe.Date,
                                                        y=dataframe[sell_ticker], mode='lines', name=sell_ticker)
                                sub_trace3 = go.Scatter(x=dataframe.Date,
                                                        y=data.ratio, mode='lines', name='Ratio')
                                sub_trace5 = go.Scatter(x=dataframe.Date,
                                                        y=data.spread, mode='lines', name='Spread')
                                sub_trace6 = go.Scatter(x=dataframe.Date,
                                                        y=data.spreadMA200, mode='lines', name='Spread MA 200')
                                sub_trace7 = go.Scatter(x=dataframe.Date,
                                                        y=data.spreadMA60, mode='lines', name='Spread MA 60')
                                sub_trace8 = go.Scatter(x=dataframe.Date,
                                                        y=data.spreadMA20, mode='lines', name='Spread MA 20')

                                sub_fig = tools.make_subplots(rows=2, cols=2, subplot_titles=[
                                    buy_ticker, 'Ratio', sell_ticker, "Spread"], shared_xaxes=True, x_title=f"Correlation: {corr_check}")
                                sub_fig.append_trace(sub_trace1, 1, 1)
                                sub_fig.append_trace(sub_trace2, 2, 1)
                                sub_fig.append_trace(sub_trace3, 1, 2)
                                sub_fig.append_trace(sub_trace5, 2, 2)
                                sub_fig.append_trace(sub_trace6, 2, 2)
                                sub_fig.append_trace(sub_trace7, 2, 2)
                                sub_fig.append_trace(sub_trace8, 2, 2)

                                sub_fig.show()
                                print(data.tail(2))


pair(all_tickers, all_tickers)
