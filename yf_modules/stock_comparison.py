import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import linear_model
sns.set_style("darkgrid")
sns.set(font_scale=1.7)


class Beta:

    def __init__(self, buy_ticker, sell_ticker, start_date):
        self.buy_ticker = buy_ticker
        self.sell_ticker = sell_ticker
        self.start_date = start_date
        beta_ticker = yf.Ticker("SPY")
        spy = beta_ticker.history(
            start=self.start_date, actions=False, rounding=True)
        if self.buy_ticker == None:

            ticker2 = yf.Ticker(self.sell_ticker)
            dataFrame2 = ticker2.history(
                start=self.start_date, actions=False, rounding=True)
            spy_ticker2 = pd.concat(
                [spy.Close[-500::], dataFrame2.Close[-500::]], axis=1)
            spy_ticker2.columns = ["SPY", self.sell_ticker]
            short_data_pct = np.log(spy_ticker2/spy_ticker2.shift())
            ticker2_cov = short_data_pct.cov().iloc[0, 1]
            ticker2_var = short_data_pct["SPY"].var()
            short_beta = ticker2_cov/ticker2_var
            print("Short BETA:", np.round(short_beta, 2))

        if self.sell_ticker == None:

            ticker1 = yf.Ticker(self.buy_ticker)
            dataFrame1 = ticker1.history(
                start=self.start_date, actions=False, rounding=True)

            spy_ticker1 = pd.concat(
                [spy.Close[-500::], dataFrame1.Close[-500::]], axis=1)
            spy_ticker1.columns = ["SPY", self.buy_ticker]
            long_data_pct = np.log(spy_ticker1/spy_ticker1.shift())
            ticker1_cov = long_data_pct.cov().iloc[0, 1]
            ticker1_var = long_data_pct["SPY"].var()
            long_beta = ticker1_cov/ticker1_var
            print("Long BETA:", np.round(long_beta, 2))


class chart(Beta):

    def pair_chart(self):

        ratio = dataFrame1.Close / dataFrame2.Close
        spread = dataFrame1.Close - dataFrame2.Close

        chart = fig, axes = plt.subplots(3, figsize=(18, 12))
        axes[0].set_title(f"{self.buy_ticker} / {self.sell_ticker}")
        sns.lineplot(data=dataFrame1, x="Date", y="Close",
                     ax=axes[0], label=self.buy_ticker)
        sns.lineplot(data=dataFrame2, x="Date", y="Close",
                     ax=axes[0], label=self.sell_ticker)
        axes[1].set_title(f"{self.buy_ticker} / {self.sell_ticker}")
        sns.lineplot(data=ratio, ax=axes[1])
        axes[2].set_title(f"{self.buy_ticker} / {self.sell_ticker}")
        sns.lineplot(data=spread, ax=axes[2])
        plt.tight_layout(pad=1)

        return chart
