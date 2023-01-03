import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

sns.set_style("darkgrid")
sns.set(font_scale=1.7)


def correlation(corr_data):
    corr_data.split()
    inputs = yf.Tickers(corr_data)
    simbol_data = inputs.history(
        start='2017-1-1', actions=False, rounding=True)

    corr_matrix = simbol_data["Close"].corr().round(2)
    positive_corr = corr_matrix > 0.3
    negative_corr = corr_matrix < -0.3

    plt.figure()
    plt.title("Correlation over 30%")
    sns.heatmap(corr_matrix[positive_corr], linewidths=2, linecolor="white",
                cmap='Greens', annot=True, annot_kws={"size": 20}, cbar=False)

    plt.figure()
    plt.title("Correlation below -30%")
    sns.heatmap(corr_matrix[negative_corr], linewidths=2, linecolor="white",
                cmap='Reds', annot=True, annot_kws={"size": 20}, cbar=False)

    plt.show()
