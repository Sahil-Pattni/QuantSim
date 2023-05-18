import datetime
import random
from typing_extensions import override
from strategies.strategy import Strategy, Trades
from utils.data import Data


class DrunkMonkey(Strategy):
    """
    A strategy that randomly buys and sells.
    """

    def __init__(self, data_source: str, data_type: Data) -> None:
        """
        Initialize the strategy with data.

        Args:
            data_source (str): Data source to be used in the strategy.
        """
        super().__init__(data_source, data_type)

    @override
    def process_datum(self, datum):
        """
        Process a single datum.

        This method should be implemented by some concrete strategy class.
        It defines the logic for processing a single datum.

        Args:
            datum (any): A single datum from the data.
        """
        if random.random() < 0.5:
            # Attempt to buy
            if self.assets["BASE"] > 0:
                # Randomly choose an amount to buy
                asset = self.random_asset(exclude_base=True)
                # Randomly choose an amount to buy
                amount = (random.random() * self.assets["BASE"]) / datum["Close"]
                # Place the buy order on the close
                self.buy(asset, datum["Close"], amount)
        else:
            # Attempt to sell for each non-base asset
            for ticker, amount in self.assets.items():
                # Skip the base asset
                if ticker == "BASE":
                    continue
                # Randomly choose an amount to sell
                amount = random.random() * amount
                # Place the sell order on the close
                self.sell(ticker, datum["Close"], amount)

    def random_asset(self, exclude_base=False):
        """
        Get a random asset from the assets dictionary.

        Returns:
            str: The random asset.
        """
        tickers = self.data.get_all_tickers()

        return random.choice(tickers)
