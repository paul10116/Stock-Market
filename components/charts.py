import sqlalchemy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly import tools
import plotly as py
import plotly.graph_objs as go
# from indicators import beta
py.offline.init_notebook_mode(connected=True)
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


def open_position(entry_date, buy_ticker, sell_ticker, value, longPrice, shortPrice, long_qty=0, short_qty=0, long_div=0, short_div=0):

    dataframe = pd.read_sql_query(
        f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

    data = pd.DataFrame({
        'Date': dataframe["Date"],
        'ratio': (dataframe[buy_ticker]/dataframe[sell_ticker]),
        'spread': (dataframe[buy_ticker]-dataframe[sell_ticker]).round(2)
    })
    
    atrp = pd.DataFrame({
        f'{buy_ticker}': (dataframe[buy_ticker].rolling(30).max() - dataframe[buy_ticker].rolling(30).min()) / dataframe[buy_ticker].rolling(30).max() * 100,
        f'{sell_ticker}': (dataframe[sell_ticker].rolling(30).max() - dataframe[sell_ticker].rolling(30).min()) / dataframe[sell_ticker].rolling(30).max() * 100,
        'ratio': (data['ratio'].rolling(30).max() - data['ratio'].rolling(30).min()) / data['ratio'].rolling(30).max()
    })
    
    long_beta = beta(dataframe[buy_ticker], buy_ticker)
    short_beta = beta(dataframe[sell_ticker], sell_ticker)
    
    position_weights = pd.DataFrame({
        'long_beta_weight': long_beta/(long_beta + short_beta),
        'short_beta_weight': short_beta/(long_beta + short_beta),
        'long_atrp_weight': atrp[buy_ticker].iloc[-1] / (atrp[buy_ticker].iloc[-1] + atrp[sell_ticker].iloc[-1]),
        'short_atrp_weight': atrp[sell_ticker].iloc[-1] / (atrp[buy_ticker].iloc[-1] + atrp[sell_ticker].iloc[-1]),
        }, index=[0])

    # Position size

    long_pos_size = value * ((position_weights['short_beta_weight'] + position_weights['short_atrp_weight'])/2)
    short_pos_size = value * ((position_weights['long_beta_weight'] + position_weights['long_atrp_weight'])/2)

    money_division_table = pd.DataFrame({
        buy_ticker: {
            'Date': entry_date,
            'Beta': long_beta.round(2),
            'ATR%': atrp.iloc[-1, 0].round(2),
            'Rec_size_in_$': long_pos_size.iloc[-1].round(0),
            'Rec_shrs_qty': (long_pos_size.iloc[-1]/longPrice).round(0),
            'REAL amount': long_qty * longPrice,
            'REAL_shrs_qty': long_qty,
            'Div_in_$': long_div * long_qty
        },
        sell_ticker: {
            'Date': entry_date,
            'Beta': short_beta.round(2),
            'ATR%': atrp.iloc[-1, 1].round(2),
            'Rec_size_in_$': short_pos_size.iloc[-1].round(0),
            'Rec_shrs_qty': (short_pos_size.iloc[-1]/shortPrice).round(0),
            'REAL amount': short_qty * shortPrice,
            'REAL_shrs_qty': short_qty,
            'Div_in_$': short_div * short_qty
        }
    }).T
    
    risk_control = pd.DataFrame({
        'Entry': longPrice / shortPrice,
        'SL': ((longPrice / shortPrice) - ((longPrice / shortPrice) * atrp.iloc[-1,2])).round(2),
        'Target': ((longPrice / shortPrice) + (((longPrice / shortPrice) * atrp.iloc[-1, 2])*3)).round(2),
        'Ratio_ATRP': (atrp.iloc[-1, 2] * 100).round(2)
        }, index=[0])
    
    print(money_division_table)

    print(
        f"""Entry: {np.round(risk_control.iloc[-1, 0], 2)}  
            SL: {risk_control.iloc[-1, 1]}  
            Target: {risk_control.iloc[-1, 2]}  
            Gain/Loss: {(((data.iloc[-1, 1] - risk_control.iloc[-1, 0]) / risk_control.iloc[-1, 0]) * 100).round(2)}%
            Ratio_ATR_%: {np.round(risk_control.iloc[-1, 3], 2)}%""")

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
    sub_trace5 = go.Bar(x=dataframe['Date'], y=risk_control['SL'], name='Stop Loss')

    sub_fig.append_trace(sub_trace1, 1, 1)
    sub_fig.append_trace(sub_trace2, 2, 1)
    sub_fig.append_trace(sub_trace3, 1, 2)
    sub_fig.append_trace(sub_trace4, 2, 2)
    sub_fig.append_trace(sub_trace5, 1, 2)

    sub_fig.update_layout(height=800, width=1400)
    sub_fig.show()

    # return money_division_table


# WATCHLIST CHART

def watchlist_chart(buy_ticker: str, sell_ticker: str):

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
    sub_fig.update_layout(height=800, width=1400)

    sub_fig.show()
    


# Correlation Chart

def heatmap_chart(variable: str):
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.heatmap(variable, annot=True, annot_kws={"size": 12},vmin=-1, vmax=1, cmap="vlag", linewidths=1, linecolor="white",robust=True)
    
    plt.show()