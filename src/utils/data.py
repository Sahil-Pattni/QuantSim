import datetime
import pandas as pd
from abc import ABC, abstractmethod


class Data(ABC):
    @abstractmethod
    def __init__(self, source: str) -> None:
        """
        Iinitialize the data object.

        Args:
            source (str): The source of the data.
        """
        self.source = source
        self.data = self.load_data()
        self.preprocess_data()

    @abstractmethod
    def load_data(self):
        """
        Load the data from the source.

        Returns:
            pd.DataFrame: The data from the source.
        """
        pass

    @abstractmethod
    def get_data(
        self, start_date: datetime = None, end_date: datetime = None
    ) -> pd.DataFrame:
        """
        Get the data within the specified range.

        Args:
            start_date (datetime, optional): The start date of the range. Defaults to None.
            end_date (datetime, optional): The end date of the range. Defaults to None.

        Returns:
            pandas.DataFrame: The preprocessed data within the specified range.
        """
        pass

    @abstractmethod
    def preprocess_data(self):
        """
        Preprocess the data.

        Returns:
            pandas.DataFrame: The preprocessed data.
        """
        pass

    @abstractmethod
    def get_all_tickers(self):
        """
        Get all the unique tickers in the data.
        """
        pass
