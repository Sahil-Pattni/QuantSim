import datetime
from typing_extensions import override
import pandas as pd
from utils.data import Data


class CryptoDataDownload(Data):
    """
    A concrete implementation of the Data class.
    Implemented for the cryptodatadownload.com data source.
    """

    def __init__(self, source: str) -> None:
        super().__init__(source)
        # Read in as a pandas dataframe

    @override
    def load_data(self):
        """
        Load the data from the source.

        Returns:
            pd.DataFrame: The data from the source.
        """
        return pd.read_csv(self.source)

    @override
    def preprocess_data(self):
        """
        Preprocess the data.

        Returns:
            pandas.DataFrame: The preprocessed data.
        """
        # Convert the date column to a datetime object
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        # Sort ascending by date
        self.data.sort_values(by=["Date"], inplace=True)

    @override
    def get_data(self, start_date: datetime, end_date: datetime):
        """
        Get the data within the specified range.

        Args:
            start_date (datetime): The start date of the range.
            end_date (datetime): The end date of the range.

        Returns:
            pandas.DataFrame: The preprocessed data within the specified range.
        """

        return self.data[
            (self.data["Date"] >= start_date) & (self.data["Date"] <= end_date)
        ]
