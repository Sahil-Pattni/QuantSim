# %%
from utils.crypto_data_download import CryptoDataDownload
from strategies import strategy
from strategies.drunk_monkey import DrunkMonkey
import datetime

# %%
PATH = "../data/Binance_BTCUSDT_1h.csv"
data = CryptoDataDownload(PATH)

# %%
# define start and end dates
start_date = datetime.datetime(2018, 1, 1)
end_date = datetime.datetime(2023, 5, 15)


# %%
# Run the strategy
strategy = DrunkMonkey(data_source=PATH, data_type=CryptoDataDownload)
# %%
