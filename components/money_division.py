import sqlalchemy
import pandas as pd
import numpy as np
# from indicators import beta
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


def money_division(buy_ticker, sell_ticker, value, longPrice, shortPrice, entry_date='2022-1-1', long_qty=0, short_qty=0, long_div=0, short_div=0):

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
    
    
    return money_division_table

    # Entry = longPrice / shortPrice
    # stop_loss = Entry - \
    #     (Entry * ((money_division.iloc[0, 2] + money_division.iloc[1, 2])/2))
    # Target = Entry+((stop_loss*0.2)*3)

    # print(
    #     f"Entry: {np.round(Entry, 2)}  SL: {np.round(stop_loss, 2)}  Target: {np.round(Target, 2)}  RATIO: {np.round(data.iloc[-1, 5], 2)}  Value: {np.round(data.iloc[-1, 5]/Entry, 2)}")



money_division(entry_date='2024-1-30', buy_ticker="BRO", sell_ticker="EXR",
              value=7000, longPrice=80.33, shortPrice=142.6, long_qty=45, short_qty=25, long_div=0.52, short_div=6.48)