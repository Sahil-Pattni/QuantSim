import datetime
import random
from typing import List
from typing_extensions import override
from strategies.strategy import Strategy, Trades
from utils.data import Data
from utils.trade import Trade


class DrunkMonkey(Strategy):
    """
    A strategy that randomly buys and sells.
    """

    def __init__(
        self, data_source: str, data_type: Data, capital: float = 100000.0
    ) -> None:
        """
        Initialize the strategy with data.

        Args:
            data_source (str): Data source to be used in the strategy.
            data_type (Data): The type of data to use.
            capital (float, optional): The amount of capital to start with. Defaults to 100000.0.
        """
        super().__init__(data_source, data_type, capital)

    @override
    def process_datum(self, datum) -> List[Trade]:
        """
        Process a single datum.

        This method should be implemented by some concrete strategy class.
        It defines the logic for processing a single datum.

        Args:
            datum (any): A single datum from the data.

        Returns:
            List[Trade]: A list of trades to be executed.
        """
        trades = []
        # Randomly choose to buy or sell
        if random.random() < 0.5:
            # Attempt to buy
            if self.assets["BASE"] > 0:
                asset = self.random_asset()
                # Randomly choose an amount to buy
                amount = (random.random() * self.assets["BASE"]) / datum["Close"]
                # Place the buy order on the close
                self.buy(asset, datum["Close"], amount)
                trades.append(
                    Trade(
                        ticker=asset,
                        action=Trades.BUY.value,
                        price=datum["Close"],
                        amount=amount,
                        time=datum["Date"],
                    )
                )
        else:
            # Attempt to sell for each non-base asset
            for ticker, amount in self.assets.items():
                if ticker == "BASE":
                    continue
                # Randomly choose an amount to sell
                amount = random.random() * amount
                # Place the sell order on the close
                self.sell(ticker, datum["Close"], amount)
                trades.append(
                    Trade(
                        ticker=ticker,
                        action=Trades.SELL.value,
                        price=datum["Close"],
                        amount=amount,
                        time=datum["Date"],
                    )
                )

        # Update the net worth
        super().process_datum(datum)

        return trades, datum["Date"]

    def random_asset(self):
        """
        Get a random asset from the assets dictionary.

        Returns:
            str: The random asset.
        """
        tickers = self.data.get_all_tickers()

        return random.choice(tickers)
