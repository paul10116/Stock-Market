import sqlalchemy
import pandas as pd
import numpy as np
from plotly import tools
import plotly as py
import plotly.graph_objs as go
from indicators import beta
py.offline.init_notebook_mode(connected=True)
engine = sqlalchemy.create_engine('sqlite:///database.db')


def open_position(buy_ticker, sell_ticker, value, longPrice, shortPrice, entry_date='2022-1-1', long_qty=0, short_qty=0, long_div=0, short_div=0):

    dataframe = pd.read_sql_query(
        f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

    data = pd.DataFrame({
        'Date': dataframe["Date"],
        'long_max': dataframe[buy_ticker].rolling(30).max(),
        'long_min': dataframe[buy_ticker].rolling(30).min(),
        'short_max': dataframe[sell_ticker].rolling(30).max(),
        'short_min': dataframe[sell_ticker].rolling(30).min(),
        'ratio': (dataframe[buy_ticker]/dataframe[sell_ticker]),
        'spread': (dataframe[buy_ticker]-dataframe[sell_ticker]).round(2)
    })

    position_ATR = pd.DataFrame({
        'long_ATR': data.long_max - data.long_min,
        'short_ATR': data.short_max - data.short_min
    })
    position_vol = pd.DataFrame({
        'long_ATR%': ((position_ATR.long_ATR + position_ATR.long_ATR.shift())/2)/data.long_max,
        'short_ATR%': ((position_ATR.short_ATR + position_ATR.short_ATR.shift())/2)/data.short_max,
        'long_beta': beta(dataframe[buy_ticker], buy_ticker).round(2),
        'short_beta': beta(dataframe[sell_ticker], sell_ticker).round(2)
    })

    position_weights = pd.DataFrame({
        'long_beta_weight': position_vol["long_beta"]/(position_vol["long_beta"] + position_vol["short_beta"]),
        'long_ATR_weight': position_vol["long_ATR%"] / (position_vol["long_ATR%"] + position_vol["short_ATR%"]),
        'short_beta_weight': position_vol["short_beta"]/(position_vol["long_beta"] + position_vol["short_beta"]),
        'short_ATR_weight': position_vol["short_ATR%"] / (position_vol["long_ATR%"] + position_vol["short_ATR%"]),
    })

    # # Position size

    long_pos_size = value * \
        ((position_weights.iloc[-1, 2] +
         position_weights.iloc[-1, 3])/2)
    short_pos_size = value * \
        ((position_weights.iloc[-1, 0] +
         position_weights.iloc[-1, 1])/2)

    money_division = pd.DataFrame({
        buy_ticker: {
            'Date': entry_date,
            'Beta': position_vol.iloc[-1, 2].round(2),
            'ATR%': position_vol.iloc[-1, 0].round(2),
            'Size_in_$': long_pos_size.round(0),
            'Shrs_qty': (long_pos_size/longPrice).round(0),
            'REAL_shrs_qty': long_qty,
            'REAL amount': long_qty * longPrice,
            'Div_in_$': long_div * long_qty
        },
        sell_ticker: {
            'Date': entry_date,
            'Beta': position_vol.iloc[-1, 3].round(2),
            'ATR%': position_vol.iloc[-1, 1].round(2),
            'Size_in_$': short_pos_size.round(0),
            'Shrs_qty': (short_pos_size/shortPrice).round(0),
            'REAL_shrs_qty': short_qty,
            'REAL amount': short_qty * shortPrice,
            'Div_in_$': short_div * short_qty
        }
    }).T

    money_division.to_sql("open_positions", engine,
                          if_exists='append', index=True)

    # money_division.iloc[0].to_sql(
    #     "Long_positions", engine, if_exists='append', index=True)
    # money_division.iloc[1].to_sql(
    #     "Short_positions", engine, if_exists='append', index=True)

    print(money_division)

    # # Technical Chart:
    Entry = longPrice / shortPrice
    stop_loss = Entry - \
        (Entry * ((money_division.iloc[0, 2] + money_division.iloc[1, 2])/2))
    Target = Entry+((stop_loss*0.2)*3)

    print(
        f"Entry: {np.round(Entry, 2)}  SL: {np.round(stop_loss, 2)}  Target: {np.round(Target, 2)}  RATIO: {np.round(data.iloc[-1, 5], 2)}  Value: {np.round(data.iloc[-1, 5]/Entry, 2)}")

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

    if data.iloc[-1, 5] < Entry:
        sub_fig.update_layout(
            height=700, width=1700, paper_bgcolor="tomato")
        sub_fig.show()
    else:
        sub_fig.update_layout(height=700, width=1700)
        sub_fig.show()
