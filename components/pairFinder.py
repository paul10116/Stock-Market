import yfinance as yf
from datetime import date
import pandas as pd
from plotly import tools
import plotly.graph_objs as go
from tickers import *
from indicators import beta

start_date = date.fromisoformat("2015-01-03")


def pair(longs, shorts):

    longArray = longs.split()
    shortArray = shorts.split()

    for buy_ticker in longArray:

        ticker1 = yf.Ticker(buy_ticker)

        for sell_ticker in shortArray:
            ticker2 = yf.Ticker(sell_ticker)

            if buy_ticker != sell_ticker:
                dataframe1 = ticker1.history(
                    start=start_date, interval="1d", rounding=True, actions=False, auto_adjust=True).Close
                dataframe2 = ticker2.history(
                    start=start_date, interval="1d", rounding=True, actions=False, auto_adjust=True).Close

                corr_matrix = pd.concat(
                    [dataframe1, dataframe2], axis=1).corr().round(2)
                corr_check = corr_matrix.iloc[0, 1]

                print(f"{buy_ticker} / {sell_ticker} CORR = {corr_check}")
                if corr_check > 0.3 or corr_check < -0.3:

                    data = pd.DataFrame({
                        'ratio': (dataframe1/dataframe2).round(3),
                        'spread': (dataframe1-dataframe2).round(2)
                    })

                    if data.ratio[-1] > 0.4:
                        data['spreadMA200'] = data['spread'].rolling(
                            200).mean().round(2)
                        data['ratioMA200'] = data['ratio'].rolling(
                            200).mean().round(2)

                        if data.ratio[-1] > data.ratioMA200[-1] and data.spread[-1] > data.spreadMA200[-1]:

                            data["spreadMA60"] = data.spread.rolling(
                                60).mean().round(2)
                            data["spreadMA20"] = data.spread.rolling(
                                20).mean().round(2)

                            if data.spreadMA20[-1] < data.spreadMA60[-1]:

                                sub_trace1 = go.Scatter(
                                    y=dataframe1, mode='lines', name=buy_ticker)
                                sub_trace2 = go.Scatter(
                                    y=dataframe2, mode='lines', name=sell_ticker)
                                sub_trace3 = go.Scatter(
                                    y=data.ratio, mode='lines', name='Ratio')
                                sub_trace5 = go.Scatter(
                                    y=data.spread, mode='lines', name='Spread')
                                sub_trace6 = go.Scatter(
                                    y=data.spreadMA200, mode='lines', name='Spread MA 200')
                                sub_trace7 = go.Scatter(
                                    y=data.spreadMA60, mode='lines', name='Spread MA 60')
                                sub_trace8 = go.Scatter(
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


pair(all_tickers, all_tickers)
