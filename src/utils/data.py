import datetime
import pandas as pd


class Data:
    def __init__(self, source: str) -> None:
        """
        Iinitialize the data object.

        Args:
            source (str): The source of the data.
        """
        self.source = source
        # TODO: Add logic for loading data from source.

    def retrieve_data(self, start_date: datetime, end_date: datetime):
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

    def preprocess_data(self, data: pd.DataFrame):
        """
        Preprocess the data.

        Args:
            data (pandas.DataFrame): The data to be preprocessed.

        Returns:
            pandas.DataFrame: The preprocessed data.
        """
        # TODO: Add logic for preprocessing data.
        pass

    def get_data(self, start_date: datetime, end_date: datetime):
        """
        Get the data within the specified range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            pandas.DataFrame: The preprocessed data within the specified range.
        """
        raw_data = self.retrieve_data(start_date, end_date)
        return self.preprocess_data(raw_data)
