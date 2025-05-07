import sqlalchemy
import pandas as pd
from indicators import beta, EMA
from tickers import over_2_B, sectorsTickers

engine = sqlalchemy.create_engine('sqlite:///stock_etf.db')


def pair(longs: str, shorts: str) -> None:
    long_array = longs.split()
    short_array = shorts.split()

    for buy_ticker in long_array:

        for sell_ticker in short_array:

            if buy_ticker != sell_ticker:
                print(f"{buy_ticker}, {sell_ticker}")        
                dataframe = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")
                
                long_beta = beta(dataframe[buy_ticker], buy_ticker).round(2)
                short_beta = beta(dataframe[sell_ticker], sell_ticker).round(2)
                beta_check = long_beta / short_beta
                corr_check = pd.concat([dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr(method='spearman').iloc[0, 1].round(2)
                
                if corr_check >= 0.6:

                    data = pd.DataFrame(
                            {
                                'Date': dataframe["Date"],
                                'ratio': (dataframe[buy_ticker] / dataframe[sell_ticker]),
                                'spread': (dataframe[buy_ticker] - dataframe[sell_ticker]).round(2)
                            }
                        )

                    ratio_lower = data.iloc[-1, 1] > 0.3
                    ratio_upper = data.iloc[-1, 1] < 3

                    if ratio_lower == True and ratio_upper == True:
                        data["C_C_returns"] = ((data.ratio - data.ratio.shift(1)) / data.ratio.shift(1))*100
                        
                        pair_statistics = pd.DataFrame({
                            f'{buy_ticker}/{sell_ticker}': {
                                'Long': buy_ticker,
                                'Short': sell_ticker,
                                'Beta': beta_check.round(2),
                                'Ratio': data.iloc[-1, 1].round(2),
                                'Variance': data['ratio'].var().round(2),
                                'Correlation': corr_check.round(2),                                   
                                'Mean': data['C_C_returns'].mean().round(3),
                                'STD': data['C_C_returns'].std().round(2),
                                'Z_Score': ((data['C_C_returns'].iloc[-1] - data['C_C_returns'].mean()) / data['C_C_returns'].std()).round(2),
                                'Kurtosis': data['C_C_returns'].kurtosis().round(2),
                                'Skewness': data['C_C_returns'].skew().round(2),
                                'Min': data['C_C_returns'].min().round(2),
                                'Max': data['C_C_returns'].max().round(2)                            
                                }
                            }).T
                        
                        variance = pair_statistics['Variance'].iloc[-1] < 5
                        correlation = pair_statistics['Correlation'].iloc[-1] > 0.6
                        Standard_deviation = pair_statistics['STD'].iloc[-1] < 7
                        min = pair_statistics['Min'].iloc[-1] > -30
                        max = pair_statistics['Max'].iloc[-1] < 30
                        
                        if variance == True and correlation == True and Standard_deviation == True and min == True and max == True:
                        
                            print(pair_statistics.tail(1))
                            
                            pair_statistics.to_sql('Without_div_watchlist', engine, if_exists='append', index=False)


pair(over_2_B, over_2_B)
