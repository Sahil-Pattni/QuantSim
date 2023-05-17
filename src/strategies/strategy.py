from abc import ABC, abstractmethod

from utils.data import Data


class Strategy(ABC):
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
