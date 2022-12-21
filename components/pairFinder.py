import yfinance as yf
from plotly import tools
import plotly.graph_objs as go


def pair(longs, shorts):

    longArray = longs.split()
    shortArray = shorts.split()
    for buy_ticker in longArray:

        ticker1 = yf.Ticker(buy_ticker)
        for sell_ticker in shortArray:

            ticker2 = yf.Ticker(sell_ticker)

            if buy_ticker != sell_ticker:
                dataframe1 = ticker1.history(
                    start="2013-01-01", interval="1d", actions=False, rounding=True)
                dataframe2 = ticker2.history(
                    start="2013-01-01", interval="1d", actions=False, rounding=True)
                ratio = dataframe1.Close/dataframe2.Close
                spread = dataframe1.Close-dataframe2.Close

                sub_trace1 = go.Scatter(
                    y=dataframe1.Close, mode='lines', name=buy_ticker)
                sub_trace2 = go.Scatter(
                    y=dataframe2.Close, mode='lines', name=sell_ticker)
                sub_trace3 = go.Scatter(
                    y=ratio, mode='lines', name='Ratio')
                sub_trace4 = go.Scatter(
                    y=spread, mode='lines', name='Spread')

                sub_fig = tools.make_subplots(rows=2, cols=2, subplot_titles=[
                    buy_ticker, sell_ticker, 'Ratio', "Spread"], shared_xaxes=True)
                sub_fig.append_trace(sub_trace1, 1, 1)
                sub_fig.append_trace(sub_trace2, 1, 2)
                sub_fig.append_trace(sub_trace3, 2, 1)
                sub_fig.append_trace(sub_trace4, 2, 2)

                sub_fig.show()
