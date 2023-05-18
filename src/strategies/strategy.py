from abc import ABC, abstractmethod
from utils.data import Data


class Strategy(ABC):
    """
    An abstract class for backtesting strategies.
    """

    @abstractmethod
    def __init__(self, data) -> None:
        """
        Initialize the strategy with data.

        Args:
            data (iterable): Data to be used in the strategy.
        """
        self.data = Data(data)

    @abstractmethod
    def execute(self):
        """
        Execute the backtesting strategy.

        This method should be implemented by some concrete strategy class.
        It defines the logic for executing the strategy on the historical data.

        Yields:
            tuple: A tuple containing the iteration index and the strategy result.
        """
        pass

    @abstractmethod
    def process_data(self, datum):
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

    @abstractmethod
    def buy(self, ticker: str, amount: float):
        """
        Buy a certain amount of a ticker.

        Args:
            ticker (str): The ticker to buy.
            amount (float): The amount to buy.

        Raises:
            InvalidTradeException: If the trade is invalid.
        """
        pass

    @abstractmethod
    def sell(self, ticker: str, amount: float):
        """
        Sell a certain amount of a ticker.

        Args:
            ticker (str): The ticker to sell.
            amount (float): The amount to sell.

        Raises:
            InvalidTradeException: If the trade is invalid.
        """
        pass
