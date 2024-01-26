import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy
from indicators import beta
from tickers import mid_cap_and_above,  xlb, xle, xli, xlu, xlk, xly, xlp, xlv, xlf, xlre, xlc

sns.set_style("darkgrid")
sns.set(font_scale=1.7)

engine = sqlalchemy.create_engine('sqlite:///stock_etf.db')


def pair(longs: str, shorts: str) -> None:
    long_array = longs.split()
    short_array = shorts.split()

    for buy_ticker in long_array:

        for sell_ticker in short_array:

            if buy_ticker != sell_ticker:
                dataframe = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")
                long_beta = beta(dataframe[buy_ticker], buy_ticker).round(2)
                short_beta = beta(dataframe[sell_ticker], sell_ticker).round(2)
                beta_bullish = long_beta > short_beta

                corr_check = pd.concat(
                    [dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr(method='spearman').iloc[0, 1].round(2)

                if -0.4 >= corr_check or corr_check >= 0.4:
                    if beta_bullish == True:

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
                            print(
                                f"{buy_ticker} / {sell_ticker} CORR = {corr_check}")

                            data['spreadMA200'] = data.spread.ewm(
                                span=200, adjust=False).mean()
                            data["ratioEMA"] = data.ratio.ewm(
                                span=200, adjust=False).mean()
                            ratio_bullish = data.iloc[-1,
                                                      4] > data.iloc[-60, 4]
                            spread_bullish = data.iloc[-1,
                                                       3] > data.iloc[-60, 3]

                            if spread_bullish == True and ratio_bullish == True:
                                data["ratioMin"] = data.ratio.rolling(60).min()
                                data["ratioMax"] = data.ratio.rolling(60).max()
                                data["ratioATR"] = data.ratioMax - \
                                    data.ratioMin
                                data["ratioATR%"] = (
                                    (data.ratioATR+data.ratioATR.shift())/2)/data.ratioMax

                                ratio_ATR = data.iloc[-1, 8] > 0.3

                                if ratio_ATR == True:
                                    print(data.tail(1))

                                    fig, axes = plt.subplots(
                                        3, figsize=(15, 15), sharex=True)
                                    axes[0].set_title(
                                        f"{buy_ticker} // {sell_ticker}")
                                    sns.lineplot(data=dataframe, x="Date", y=buy_ticker,
                                                 ax=axes[0], label=buy_ticker)
                                    sns.lineplot(data=dataframe, x="Date", y=sell_ticker,
                                                 ax=axes[0], label=sell_ticker)
                                    axes[1].set_title(
                                        f"Ratio")
                                    sns.lineplot(
                                        data=data, x="Date", y="ratio", ax=axes[1])
                                    sns.lineplot(
                                        data=data, x="Date", y="ratioEMA", ax=axes[1])
                                    axes[2].set_title(
                                        f"Spread")
                                    sns.lineplot(
                                        data=data, x="Date", y="spread", ax=axes[2])
                                    sns.lineplot(
                                        data=data, x="Date", y="spreadMA200", ax=axes[2])
                                    plt.tight_layout(pad=1)

                                    fig.savefig(
                                        r'd://StockMarket/Bullish/'+f"{buy_ticker}__{sell_ticker}")
                                    plt.close()


pair(mid_cap_and_above, mid_cap_and_above)
