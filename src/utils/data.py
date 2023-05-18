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
    def get_data(self, start_date: datetime, end_date: datetime):
        """
        Retrieve data from the source within the specified range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            pandas.DataFrame: The data within the specified range.
        """
        # TODO: Add logic for retrieving data from source.
        pass

    @abstractmethod
    def preprocess_data(self):
        """
        Preprocess the data.

        Returns:
            pandas.DataFrame: The preprocessed data.
        """
        # TODO: Add logic for preprocessing data.
        pass
