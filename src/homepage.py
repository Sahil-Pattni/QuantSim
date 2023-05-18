# %%
from utils.crypto_data_download import CryptoDataDownload
from strategies import strategy
from strategies.drunk_monkey import DrunkMonkey
import datetime

# %%
PATH = "../data/Binance_BTCUSDT_1h.csv"
START_DATE = datetime.datetime(2018, 1, 1)
END_DATE = datetime.datetime(2023, 5, 15)

strategy = DrunkMonkey(data_source=PATH, data_type=CryptoDataDownload)
gen = strategy.execute(START_DATE, END_DATE)
for idx in gen:
    print(f"{idx}: {strategy.assets}")

# %%
