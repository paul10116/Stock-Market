import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

sns.set_style("darkgrid")
sns.set(font_scale=1.7)


def pair(buy_ticker, sell_ticker):

    ticker1 = yf.Ticker(buy_ticker)
    ticker2 = yf.Ticker(sell_ticker)

    dataFrame1 = ticker1.history(
        start='2018-1-1', actions=True, rounding=True)
    dataFrame2 = ticker2.history(
        start='2018-1-1', actions=True, rounding=True)

    ratio = dataFrame1.Close / dataFrame2.Close
    spread = dataFrame1.Close - dataFrame2.Close

    # CHART
    chart = fig, axes = plt.subplots(3, figsize=(18, 12))
    axes[0].set_title(
        f"{buy_ticker} // {sell_ticker}")
    sns.lineplot(data=dataFrame1, x="Date", y="Close",
                 ax=axes[0], label=buy_ticker)
    sns.lineplot(data=dataFrame2, x="Date", y="Close",
                 ax=axes[0], label=sell_ticker)
    axes[1].set_title(f"Ratio {buy_ticker} / {sell_ticker}")
    sns.lineplot(data=ratio, ax=axes[1])
    axes[2].set_title(f"Spread {buy_ticker} / {sell_ticker}")
    sns.lineplot(data=spread, ax=axes[2])
    plt.tight_layout(pad=1)

    return chart
