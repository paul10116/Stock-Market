    if data.spread[-15] < data.spreadMA20[-15] and data.spread[-1] > data.spreadMA60[-1]:

                                    sub_trace1 = go.Scatter(
                                        y=dataframe1, mode='lines', name=buy_ticker)
                                    sub_trace2 = go.Scatter(
                                        y=dataframe2, mode='lines', name=sell_ticker)
                                    sub_trace3 = go.Scatter(
                                        y=data.ratio, mode='lines', name='Ratio')
                                    sub_trace5 = go.Scatter(
                                        y=data.spread, mode='lines', name='Spread')
                                    sub_trace6 = go.Scatter(
                                        y=data.spreadMA200, mode='lines', name='Spread MA 200')
                                    sub_trace7 = go.Scatter(
                                        y=data.spreadMA60, mode='lines', name='Spread MA 60')
                                    sub_trace8 = go.Scatter(
                                        y=data.spreadMA20, mode='lines', name='Spread MA 20')

                                    sub_fig = tools.make_subplots(rows=2, cols=2, subplot_titles=[
                                        buy_ticker, 'Ratio', sell_ticker, "Spread"], shared_xaxes=True, x_title=f"Correlation: {corr_check}")
                                    sub_fig.append_trace(sub_trace1, 1, 1)
                                    sub_fig.append_trace(sub_trace2, 2, 1)
                                    sub_fig.append_trace(sub_trace3, 1, 2)
                                    sub_fig.append_trace(sub_trace5, 2, 2)
                                    sub_fig.append_trace(sub_trace6, 2, 2)
                                    sub_fig.append_trace(sub_trace7, 2, 2)
                                    sub_fig.append_trace(sub_trace8, 2, 2)

                                    sub_fig.show()