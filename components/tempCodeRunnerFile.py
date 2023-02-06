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