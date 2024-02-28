import sqlalchemy
import pandas as pd
import numpy as np
from indicators import beta
engine = sqlalchemy.create_engine('sqlite:///stock_etf.db')
index_data = pd.read_sql_query("SELECT * FROM ETF", engine, parse_dates="Date")


def money_division(buy_ticker, sell_ticker, value, longPrice, shortPrice, entry_date='2022-1-1', long_qty=0, short_qty=0, long_div=0, short_div=0):

    dataframe = pd.read_sql_query(
        f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

    data = pd.DataFrame({
        'Date': dataframe["Date"],
        'ratio': (dataframe[buy_ticker]/dataframe[sell_ticker]),
        'spread': (dataframe[buy_ticker]-dataframe[sell_ticker]).round(2)
    })
    
    position_vol = pd.DataFrame({
        f'{buy_ticker}': ((dataframe[buy_ticker] - dataframe[buy_ticker].shift(1)) / dataframe[buy_ticker].shift(1))*100,
        f'{sell_ticker}': ((dataframe[sell_ticker] - dataframe[sell_ticker].shift(1)) / dataframe[sell_ticker].shift(1))*100,
        'Ratio': ((data['ratio']-data['ratio'].shift(1)) / data['ratio'].shift(1)) * 100
    })
    
    long_beta = beta(dataframe[buy_ticker], buy_ticker)
    short_beta = beta(dataframe[sell_ticker], sell_ticker)
    long_STD_weight = position_vol[buy_ticker].std() / (position_vol[buy_ticker].std() + position_vol[sell_ticker].std()),
    short_STD_weight = position_vol[sell_ticker].std() / (position_vol[buy_ticker].std() + position_vol[sell_ticker].std())
    
    
    beta_weight = pd.DataFrame({
        'long_beta_weight': long_beta/(long_beta + short_beta),
        'short_beta_weight': short_beta/(long_beta + short_beta),
        }, index=[0])


    # Position size

    long_pos_size = value * ((beta_weight['short_beta_weight'] + short_STD_weight )/2)
    short_pos_size = value * ((beta_weight['long_beta_weight'] + long_STD_weight)/2)
    

    money_division = pd.DataFrame({
        buy_ticker: {
            'Date': entry_date,
            'Beta': long_beta.round(2),
            'ATR%': position_vol.iloc[-1, 0].round(2),
            'Size_in_$': long_pos_size.round(0),
            'Rec_shrs_qty': (long_pos_size/longPrice).round(0),
            'REAL_shrs_qty': long_qty,
            'REAL amount': long_qty * longPrice,
            'Div_in_$': long_div * long_qty
        },
        sell_ticker: {
            'Date': entry_date,
            'Beta': short_beta.round(2),
            'ATR%': position_vol.iloc[-1, 1].round(2),
            'Size_in_$': short_pos_size.round(0),
            'Shrs_qty': (short_pos_size/shortPrice).round(0),
            'REAL_shrs_qty': short_qty,
            'REAL amount': short_qty * shortPrice,
            'Div_in_$': short_div * short_qty
        }
    }).T
    
    return money_division


    # Entry = longPrice / shortPrice
    # stop_loss = Entry - \
    #     (Entry * ((money_division.iloc[0, 2] + money_division.iloc[1, 2])/2))
    # Target = Entry+((stop_loss*0.2)*3)

    # print(
    #     f"Entry: {np.round(Entry, 2)}  SL: {np.round(stop_loss, 2)}  Target: {np.round(Target, 2)}  RATIO: {np.round(data.iloc[-1, 5], 2)}  Value: {np.round(data.iloc[-1, 5]/Entry, 2)}")



money_division(entry_date='2024-1-30', buy_ticker="BRO", sell_ticker="EXR",
              value=7000, longPrice=80.33, shortPrice=142.6, long_qty=45, short_qty=25, long_div=0.52, short_div=6.48)