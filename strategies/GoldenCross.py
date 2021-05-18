'''
A strategy based on buying/selling crosses of the SMA's commonly called the "GoldenCross".
Uses SMA's of fast (50 day avg) and slow (200 day avg) to determine when to buy


BUYS: When Slow SMA crosses above Fast SMA
SELL: When Fast SMA crosses below Slow SMA
'''
import backtrader as bt
import math

class GoldenCross(bt.Strategy):
    params = (("fast", 50), ("slow", 200), ("order_percentage", 0.95), ('ticker', 'AAPL'))

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname="50 day moving average"
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname="200 day moving average"
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print("Buy {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
               print("Sell {} shares of {} at {}".format(self.size, self.params.ticker, self.data.close[0]))
               self.close()