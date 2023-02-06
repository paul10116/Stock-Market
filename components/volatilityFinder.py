import pandas as pd
from plotly import tools
import plotly.graph_objs as go
from tickers import *
import sqlite3
import sqlalchemy
from indicators import beta

engine = sqlalchemy.create_engine('sqlite:///database.db')
data = pd.read_sql_query(
    "SELECT * FROM stockData", engine, parse_dates="Date")


def pair(longs, shorts):

    longArray = longs.split()
    shortArray = shorts.split()

    for buy_ticker in longArray:

        for sell_ticker in shortArray:

            if buy_ticker != sell_ticker:
                dataframe = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")

                long_beta = beta(dataframe[buy_ticker], buy_ticker).round(2)
                short_beta = beta(dataframe[sell_ticker], sell_ticker).round(2)
                beta_bearish = long_beta < short_beta

                corr_check = pd.concat(
                    [dataframe[buy_ticker], dataframe[sell_ticker]], axis=1).corr().iloc[0, 1].round(2)

                print(
                    f"{buy_ticker} / {sell_ticker} CORR = {corr_check}")

                if corr_check > 0.3 or corr_check < -0.3:
                    if beta_bearish == True:

                        data = pd.DataFrame({
                            'ratio': (dataframe[buy_ticker]/dataframe[sell_ticker]),
                            'spread': (dataframe[buy_ticker]-dataframe[sell_ticker]).round(2)
                        })

                        ratio_lower = data.iloc[-1, 0] > 0.4
                        ratio_upper = data.iloc[-1, 0] < 3

                        if ratio_lower == True and ratio_upper == True:

                            data['spreadMA200'] = data.spread.ewm(
                                span=200, adjust=False).mean()
                            data["ratioEMA"] = data.ratio.ewm(
                                span=200, adjust=False).mean()
                            ratio_bullish = data.iloc[-1,
                                                      3] > data.iloc[-60, 3]
                            spread_bullish = data.iloc[-1,
                                                       2] > data.iloc[-60, 2]

                            if spread_bullish == True and ratio_bullish == True:
                                data["ratioMin"] = data.ratio.rolling(60).min()
                                data["ratioMax"] = data.ratio.rolling(60).max()
                                data["ratioATR"] = data.ratioMax - \
                                    data.ratioMin
                                data["ratioATR%"] = (
                                    (data.ratioATR+data.ratioATR.shift())/2)/data.ratioMax

                                ratio_ATR = data.iloc[-1, 7] > 0.3

                                if ratio_ATR == True:
                                    print(data.tail(1))

                                    sub_trace1 = go.Scatter(x=dataframe.Date,
                                                            y=dataframe[buy_ticker], mode='lines', name=buy_ticker)
                                    sub_trace2 = go.Scatter(x=dataframe.Date,
                                                            y=dataframe[sell_ticker], mode='lines', name=sell_ticker)
                                    sub_trace3 = go.Scatter(x=dataframe.Date,
                                                            y=data.ratio, mode='lines', name='Ratio')
                                    sub_trace4 = go.Scatter(x=dataframe.Date,
                                                            y=data.spreadMA200, mode='lines', name='SpreadMA200')
                                    sub_trace5 = go.Scatter(x=dataframe.Date,
                                                            y=data.spread, mode='lines', name='Spread')
                                    sub_trace6 = go.Scatter(x=dataframe.Date,
                                                            y=data.ratioEMA, mode='lines', name='ratioEMA')
                                    sub_trace7 = go.Scatter(x=dataframe.Date,
                                                            y=data.ratioMin, mode='lines', name='ratioMin')
                                    sub_trace8 = go.Scatter(x=dataframe.Date,
                                                            y=data.ratioMax, mode='lines', name='ratioMax')

                                    sub_fig = tools.make_subplots(rows=2, cols=2, subplot_titles=[
                                        buy_ticker, 'Ratio', sell_ticker, "Spread"], shared_xaxes=True, x_title=f"Correlation: {corr_check}")
                                    sub_fig.append_trace(sub_trace1, 1, 1)
                                    sub_fig.append_trace(sub_trace2, 2, 1)
                                    sub_fig.append_trace(sub_trace3, 1, 2)
                                    sub_fig.append_trace(sub_trace4, 2, 2)
                                    sub_fig.append_trace(sub_trace5, 2, 2)
                                    sub_fig.append_trace(sub_trace6, 1, 2)
                                    sub_fig.append_trace(sub_trace7, 1, 2)
                                    sub_fig.append_trace(sub_trace8, 1, 2)

                                    sub_fig.show()


pair('ABB', 'OMF ORA ORCL ORI OSK OSW OTEX OUT OVV OXY OZK PAAS PACW PAG PAGP PB PBF PBR PCH PDCE PDCO PEG PFE PFGC PFS PG PGR PH PHG PII PINC PK PKG PKI PLD PLNT PM PNC PNFP PNM PNR PNW POR POST POWI PRA PRGO PRQR PRU PSA PSTG PSX PVH PWR PXD QDEL QSR QTWO RAD')
