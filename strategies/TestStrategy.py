'''
A test strategy partially provided by BackTraders QuickStart Guide.

BUYS: If close is less than previous close two days in a row
SELL: Once position has been open for 5 days, sell entire position
'''
import backtrader as bt

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        # Logging function for this strategy
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        
        print(len(self))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
            
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("BUY EXECUTED {}".format(order.executed.price))
            elif order.issell():
                self.log("SELL EXECUTED {}".format(order.executed.price))
            
            self.bar_executed = len(self)

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            # Order is already open (True)
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # Current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # Previous close less than the previous close

                    # Buy signal created (with all possible default parameters)
                    self.log('BUY CREATED, %.2f' % self.dataclose[0])
                    self.order = self.buy()
        else:
            if len(self) >= (self.bar_executed + 5):
                # Sell if position is open and it has been 5 days (yes this is a terrible strategy)

                self.log("SELL CREATED {}".format(self.dataclose[0]))
                self.order = self.sell()