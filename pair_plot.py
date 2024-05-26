import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///stock_etf.db')
data = pd.read_sql_query("SELECT * FROM stockData", engine, parse_dates="Date")


results = pd.read_sql_query("""SELECT * FROM Dividend_watchlist WHERE Correlation <= -0.9 AND Correlation >= -1  """, engine)
print(results.tail(5))

def pair_plot(results :pd.DataFrame):

    for index, row in results.iterrows():
        
        buy_ticker = row['Long']
        sell_ticker = row['Short']
       
        pair_data = pd.read_sql_query(
                    f"SELECT Date, {buy_ticker}, {sell_ticker} FROM stockData", engine, parse_dates="Date")
        
        data = pd.DataFrame(
                            {
                                'Date': pair_data["Date"],
                                'ratio': (pair_data[buy_ticker] / pair_data[sell_ticker]),
                                'spread': (pair_data[buy_ticker] - pair_data[sell_ticker]).round(2)
                            }
                        )
    
        fig, axes = plt.subplots(
        3, figsize=(15, 15), sharex=True)
        axes[0].set_title(f"{buy_ticker} // {sell_ticker}")
        sns.lineplot(data=pair_data, x="Date", y=buy_ticker, ax=axes[0], label=buy_ticker)
        sns.lineplot(data=pair_data, x="Date", y=sell_ticker, ax=axes[0], label=sell_ticker)
        axes[1].set_title(f"Ratio")
        sns.lineplot(data=data, x="Date", y="ratio", ax=axes[1])
        axes[2].set_title(f"Spread")
        sns.lineplot(data=data, x="Date", y="spread", ax=axes[2])
        plt.tight_layout(pad=1)

        fig.savefig(r'd://StockMarket/corr_-0.9_-1/'+f"{buy_ticker}__{sell_ticker}")
        plt.close()
        
pair_plot(results)