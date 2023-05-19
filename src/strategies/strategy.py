from abc import ABC, abstractmethod
import datetime
from enum import Enum
from typing import List
from utils.custom_exceptions import InvalidTradeException
from utils.data import Data
from utils.trade import Trade


class Trades(Enum):
    """
    An enum for the types of trades.
    """

    BUY = "BUY"
    SELL = "SELL"


class Strategy(ABC):
    """
    An abstract class for backtesting strategies.
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
        self.data = data_type(data_source)
        self.initial_capital = capital
        # Initialize the assets
        self.assets = {
            "BASE": capital,
        }
        # Last value of the assets
        self.last_value = {}

        for ticker in self.data.get_all_tickers():
            self.assets[ticker] = 0.0
            self.last_value[ticker] = 0.0

    def execute(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> List[Trade]:
        """
        Execute the backtesting strategy.

        This method should be implemented by some concrete strategy class.
        It defines the logic for executing the strategy on the historical data.

        Args:
            start_date (datetime, optional): The start date of the backtest. Defaults to None.
            end_date (datetime, optional): The end date of the backtest. Defaults to None.

        Yields:
            int: The index of the current datum.
        """
        data = self.data.get_data(start_date, end_date)
        n = data.shape[0]
        for i, datum in data.iterrows():
            trades: List[Trade] = self.process_datum(datum)
            yield i, n, trades

        # Sell all assets at the end
        for ticker, amount in self.assets.items():
            if ticker == "BASE":
                continue
            self.sell(ticker, datum["Close"], amount)

    def buy(self, ticker: str, price: float, amount: float) -> None:
        """
        Buy a certain amount of a ticker.

        Args:
            ticker (str): The ticker to buy.
            price (float): The price to buy at.
            amount (float): The amount to buy.

        Raises:
            InvalidTradeException: If the trade is invalid.
        """
        base_equivalent = amount * price
        # If we don't have enough money, raise an exception
        if self.assets["BASE"] < base_equivalent:
            raise InvalidTradeException(ticker, amount, True)

        # Otherwise, execute the trade
        self.assets["BASE"] -= base_equivalent
        self.assets[ticker] += amount

    def sell(self, ticker: str, price: float, amount: float) -> None:
        """
        Sell a certain amount of a ticker.

        Args:
            ticker (str): The ticker to sell.
            price (float): The price to sell at.
            amount (float): The amount to sell.

        Raises:
            InvalidTradeException: If the trade is invalid.
        """
        # If we don't have enough of the ticker, raise an exception
        if self.assets[ticker] < amount:
            raise InvalidTradeException(ticker, amount, False)

        # Otherwise, execute the trade
        self.assets["BASE"] += amount * price
        self.assets[ticker] -= amount

    @abstractmethod
    def process_datum(self, datum) -> None:
        """
        Process a single datum.

        This method should be implemented by some concrete strategy class.
        It defines the logic for processing a single datum.

        Args:
            datum (any): A single datum from the data.
        """
        # Update last seen values
        self.update_last_values(datum)

    def update_last_values(self, datum):
        ticker = datum["Symbol"]
        self.last_value[ticker] = datum["Close"]

    def calculate_net_worth(self):
        """
        Update the net worth of the strategy.

        Returns:
            float: The net worth of the strategy so far.
        """
        net_worth = 0.0
        for ticker, amount in self.assets.items():
            # Base asset
            if ticker == "BASE":
                net_worth += amount
                continue
            else:
                # Update the last value of the asset
                net_worth += amount * self.last_value[ticker]

        return net_worth
