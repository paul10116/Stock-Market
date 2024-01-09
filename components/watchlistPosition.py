import pandas as pd
from plotly import tools
import plotly as py
import plotly.graph_objs as go
import sqlalchemy
py.offline.init_notebook_mode(connected=True)
engine = sqlalchemy.create_engine('sqlite:///database.db')


def pair(buy_ticker, sell_ticker):

    dataframe = pd.read_sql_query(
        f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

    data = pd.DataFrame({
        'Date': dataframe["Date"],
        'ratio': (dataframe[buy_ticker]/dataframe[sell_ticker]),
        'spread': (dataframe[buy_ticker]-dataframe[sell_ticker]).round(2)
    })

    # CHART

    sub_fig = tools.make_subplots(rows=2, cols=2, subplot_titles=[
        buy_ticker, "Ratio", sell_ticker, 'Spread'], shared_xaxes=True)

    sub_trace1 = go.Scatter(x=dataframe['Date'],
                            y=dataframe[buy_ticker], mode='lines', name=buy_ticker)
    sub_trace2 = go.Scatter(x=dataframe['Date'],
                            y=dataframe[sell_ticker], mode='lines', name=sell_ticker)
    sub_trace3 = go.Scatter(
        x=dataframe['Date'], y=data['ratio'], mode='lines', name='Ratio')
    sub_trace4 = go.Scatter(
        x=dataframe['Date'], y=data['spread'], mode='lines', name='Spread')

    sub_fig.append_trace(sub_trace1, 1, 1)
    sub_fig.append_trace(sub_trace2, 2, 1)
    sub_fig.append_trace(sub_trace3, 1, 2)
    sub_fig.append_trace(sub_trace4, 2, 2)
    sub_fig.update_layout(height=700, width=1700)

    sub_fig.show()
