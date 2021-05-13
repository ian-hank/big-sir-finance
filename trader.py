import os, sys, argparse
import datetime as dt
import backtrader as bt
from backtrader import cerebro
from strategies.TestStrategy import TestStrategy

# Constants
STARTING_CASH = 10000.00
STARTING_DATE = dt.datetime(2020, 1, 1)
ENDING_DATE = dt.date(2021, 12, 31)

# Strategy Dictionary
strategies = {
    "test_strategy": TestStrategy
}

# Argument Parser (CMD)
parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="which trading strategy to use", type=str)
args = parser.parse_args()

if not args.strategy in strategies:
    print("invalid strategy, must be one of {}".format(strategies.keys()))
    sys.exit(0)

# Yahoo Data Feed
data = bt.feeds.YahooFinanceCSVData(
    dataname = ("data/AAPL.csv"),

    # Range of data being used
    fromdate = STARTING_DATE, # Starting Date of Data Feed
    todate = ENDING_DATE, # Ending Date of Data Feed

    # Yahoo's head() of data is the oldest
    reverse = False
)

# Intitializing Cerebro and Params
cerebro = bt.Cerebro()
cerebro.broker.set_cash(STARTING_CASH)
cerebro.adddata(data)
cerebro.addstrategy(strategies[args.strategy]) # arg parser to go in here
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