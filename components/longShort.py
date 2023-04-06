import pandas as pd
from plotly import tools
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
from tickers import *
import sqlite3
import sqlalchemy
from indicators import beta

sns.set_style("darkgrid")
sns.set(font_scale=1.7)

engine = sqlalchemy.create_engine('sqlite:///database.db')


def pair(longs, shorts):

    longArray = longs.split()
    shortArray = shorts.split()

    for buy_ticker in longArray:

        for sell_ticker in shortArray:

            if buy_ticker != sell_ticker:
                longData = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker} FROM companiesToBuy", engine, parse_dates="Date")

                shortData = pd.read_sql_query(
                    f"SELECT Date, {sell_ticker} FROM companiesToShort", engine, parse_dates="Date")

                data = pd.DataFrame({
                    'Date': longData["Date"],
                    'ratio': (longData[buy_ticker]/shortData[sell_ticker]).round(3),
                    'spread': (longData[buy_ticker]-shortData[sell_ticker]).round(2)
                })

                ratio_lower = data.iloc[0, 1] > 0.3
                ratio_upper = data.iloc[0, 1] < 3

                if ratio_lower == True and ratio_upper == True:

                    print(f"{buy_ticker} / {sell_ticker}")
                    print(data.head(1))

                    fig, axes = plt.subplots(
                        3, figsize=(15, 15), sharex=True)
                    axes[0].set_title(
                        f"{buy_ticker} // {sell_ticker}")
                    sns.lineplot(data=longData, x="Date", y=buy_ticker,
                                 ax=axes[0], label=buy_ticker)
                    sns.lineplot(data=shortData, x="Date", y=sell_ticker,
                                 ax=axes[0], label=sell_ticker)
                    axes[1].set_title(
                        f"Ratio")
                    sns.lineplot(
                        data=data, x="Date", y="ratio", ax=axes[1])
                    axes[2].set_title(
                        f"Spread")
                    sns.lineplot(
                        data=data, x="Date", y="spread", ax=axes[2])
                    plt.tight_layout(pad=1)

                    fig.savefig(
                        r'd://Trading/longShort/'+f"{buy_ticker}__{sell_ticker}")
                    plt.close()


pair(tickers_for_longs, tickers_for_shorts)
