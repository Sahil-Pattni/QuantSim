from abc import ABC, abstractmethod
import datetime
from enum import Enum
from utils.custom_exceptions import InvalidTradeException
from utils.data import Data


class Trades(Enum):
    """
    An enum for the types of trades.
    """

    BUY = 0
    SELL = 1


class Strategy(ABC):
    """
    An abstract class for backtesting strategies.
    """

    def __init__(self, data_source: str, data_type: Data, capital: float) -> None:
        """
        Initialize the strategy with data.

        Args:
            data_source (str): Data source to be used in the strategy.
            data_type (Data): The type of data to use.
            capital (float): The starting capital.

        """
        self.data = data_type(data_source)
        # Initialize the assets
        self.assets = {
            "BASE": capital,
        }

    def execute(self, start_date: datetime, end_date: datetime):
        """
        Execute the backtesting strategy.

        This method should be implemented by some concrete strategy class.
        It defines the logic for executing the strategy on the historical data.

        Yields:
            tuple: A tuple containing the iteration index and the strategy result.
        """
        for i, datum in self.data.get_data(start_date, end_date).iterrows():
            yield i, self.process_data(datum)

    def buy(self, ticker: str, price: float, amount: float):
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

    def sell(self, ticker: str, price: float, amount: float):
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
    def process_datum(self, datum):
        """
        Process a single datum.

        This method should be implemented by some concrete strategy class.
        It defines the logic for processing a single datum.

        Args:
            datum (any): A single datum from the data.

        Returns:
            any: The result of processing the datum.
        """
        pass
