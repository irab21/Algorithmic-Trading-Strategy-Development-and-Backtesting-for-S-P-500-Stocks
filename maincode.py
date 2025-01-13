import backtrader as bt
import pandas as pd
import datetime

# Define the Strategy
class MeanReversionStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),
        ('rsi_low', 30),
        ('rsi_high', 70),
        ('stake', 10),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

    def next(self):
        if not self.position:  # If not in position
            if self.rsi < self.params.rsi_low:  # Oversold condition
                self.buy(size=self.params.stake)
        else:
            if self.rsi > self.params.rsi_high:  # Overbought condition
                self.sell(size=self.params.stake)


# Load Historical Data
def load_data(symbol, start, end):
    # Example: Download data from Yahoo Finance
    import yfinance as yf
    data = yf.download(symbol, start=start, end=end)
    data['openinterest'] = 0  # Required by Backtrader
    return bt.feeds.PandasData(dataname=data)


# Main Function
def main():
    # Initialize the Backtrader engine
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MeanReversionStrategy)

    # Load data
    symbol = 'AAPL'  # Example stock
    start_date = '2020-01-01'
    end_date = '2022-12-31'
    data = load_data(symbol, start_date, end_date)

    cerebro.adddata(data)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    # Run backtest
    print("Starting backtest...")
    results = cerebro.run()
    strat = results[0]

    # Display performance metrics
    print(f"Sharpe Ratio: {strat.analyzers.sharpe.get_analysis()}")
    print(f"Drawdown: {strat.analyzers.drawdown.get_analysis()}")

    # Plot the results
    cerebro.plot()


if __name__ == '__main__':
    main()
