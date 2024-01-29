from flask import Flask, render_template, Response
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy
from indicators import beta
from tickers import mid_cap_and_above,  xlb, xle, xli, xlu, xlk, xly, xlp, xlv, xlf, xlre, xlc

app = Flask(__name__)

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
                ratio_beta = long_beta / short_beta

                corr_check = pd.concat(
                    [dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr(method='spearman').iloc[0, 1].round(2)

                if -0.4 >= corr_check or corr_check >= 0.4:
                    if ratio_beta > 1:

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

                            data['spreadMA200'] = data.spread.ewm(
                                span=200, adjust=False).mean()
                            data["ratioEMA"] = data.ratio.ewm(
                                span=200, adjust=False).mean()
                            ratio_bullish = data.iloc[-1,
                                                      4] > data.iloc[-60, 4]
                            spread_bullish = data.iloc[-1,
                                                       3] > data.iloc[-60, 3]

                            if spread_bullish == True and ratio_bullish == True:
                                return render_template('plot.html', data=data, buy_ticker=buy_ticker, sell_ticker=sell_ticker)

@app.route('/')
def index():
    return pair(xlb, xlu)

if __name__ == '__main__':
    app.run(debug=True)