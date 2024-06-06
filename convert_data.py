import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('crypto_data.csv', header=None)

# Đặt tên cho các cột
df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

# Chuyển đổi Unix timestamp sang datetime
df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

# Sắp xếp lại các cột để datetime ở vị trí đầu tiên
df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]

# Lưu lại dữ liệu đã chuyển đổi
df.to_csv('crypto_data_converted.csv', index=False)
