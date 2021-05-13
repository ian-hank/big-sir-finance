import os, sys, argparse
import datetime as dt
import backtrader as bt
from backtrader import cerebro

# Constants
STARTING_CASH = 10000.00

# Yahoo Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname = ("data/AAPL.csv"),
    # Range of data being used
    fromdate = dt.datetime(2015, 1, 1), # Starting Date of Data Feed
    todate = dt.datetime(2021, 12, 31), # Ending Date of Data Feed
    # Yahoo's head() of data is the oldest
    reverse = False
)

# Intitializing Cerebro and Params
cerebro = bt.Cerebro()
cerebro.broker.set_cash(STARTING_CASH)
cerebro.adddata(data)
cerebro.addstrategy() # arg parser to go in here
cerebro.run()

# Final Output
gain_dollar = cerebro.broker.getvalue() - STARTING_CASH
gain_pct = gain_dollar / STARTING_CASH * 100
formatted_gain_dollar = "{:.2f}".format(gain_dollar)
formatted_gain_pct = "{:.2f}".format(gain_pct)


print("\nStarting Portfolio Value: $%.2f" % STARTING_CASH)
print("Ending Portfolio Value:   $%.2f" % cerebro.broker.getvalue())
print("Gain/Loss($): $" + str(formatted_gain_dollar))
print("Gain/Loss(%): " + str(formatted_gain_pct) + "%")

cerebro.plot()