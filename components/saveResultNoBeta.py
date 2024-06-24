import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy
from indicators import beta
from tickers import with_div, no_div, new_small_cap_and_above

sns.set_style("darkgrid")

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

                corr_check = pd.concat(
                    [dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr(method='spearman').iloc[0, 1].round(2)
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
                        data['EMA_50'] = data['ratio'].ewm(span=50, adjust=False).mean()
                        
                        ratio_check = data.iloc[-1, 1] > data.iloc[-1,4]
                                
                        print(data.tail(1))

                        fig, axes = plt.subplots(
                                        3, figsize=(15, 15), sharex=False)
                        axes[0].set_title(
                                        f"{buy_ticker} // {sell_ticker}")
                        sns.lineplot(data=dataframe, x="Date", y=buy_ticker,
                                                 ax=axes[0], label=buy_ticker)
                        sns.lineplot(data=dataframe, x="Date", y=sell_ticker,
                                                 ax=axes[0], label=sell_ticker)
                        axes[1].set_title("Ratio")
                        sns.lineplot(data=data, x="Date", y="EMA_50", ax=axes[1])
                        sns.lineplot(
                                        data=data, x="Date", y="ratio", ax=axes[1])
                        axes[2].set_title("Spread")
                        sns.lineplot(
                                        data=data, x="Date", y="spread", ax=axes[2])
                        plt.tight_layout(pad=1)

                        fig.savefig(
                                        r'd://StockMarket/COIN/'+f"{buy_ticker}__{sell_ticker}")
                        plt.close()


pair('AMD', new_small_cap_and_above)
