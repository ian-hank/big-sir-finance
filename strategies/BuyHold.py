'''
The simplest strategy in the world! Buy and Hold forever.

BUYS: At start date it will buy as many shares as possible with 100% of available cash
SELL: Never!
'''
import backtrader as bt

class BuyHold(bt.Strategy):

    def next(self):
        if self.position.size == 0:
            # Currently holding 0 shares

            # Declaring as an int to not allow for fractional shares
            size = int(self.broker.getcash() / self.data)
            self.buy(size=size)