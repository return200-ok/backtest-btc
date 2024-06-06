import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Sử dụng backend Agg để vẽ đồ thị mà không cần giao diện đồ họa
import matplotlib.pyplot as plt
import backtrader as bt

# Chuyển đổi dữ liệu từ Unix timestamp sang datetime
df = pd.read_csv('crypto_data.csv', header=None)
df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
df.to_csv('crypto_data_converted.csv', index=False)

class MACDStrategy(bt.Strategy):
    params = (
        ('macd1', 12),
        ('macd2', 26),
        ('signal', 9),
    )

    def __init__(self):
        self.macd = bt.indicators.MACDHisto(
            self.data.close,
            period_me1=self.params.macd1,
            period_me2=self.params.macd2,
            period_signal=self.params.signal
        )

    def next(self):
        if self.macd.macd[0] > self.macd.signal[0] and self.macd.macd[-1] <= self.macd.signal[-1]:
            self.buy()
        elif self.macd.macd[0] < self.macd.signal[0] and self.macd.macd[-1] >= self.macd.signal[-1]:
            self.sell()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MACDStrategy)

    data = bt.feeds.GenericCSVData(
        dataname='crypto_data_converted.csv',
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        high=2,
        low=3,
        open=1,
        close=4,
        volume=5,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.001)

    print('Vốn ban đầu: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Vốn cuối cùng: %.2f' % cerebro.broker.getvalue())

    # Lưu biểu đồ dưới dạng file ảnh
    fig = cerebro.plot()[0][0]
    fig.savefig('backtest_result.png')
