import datetime
from functools import lru_cache
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
    def preprocess_data(self) -> None:
        """
        Preprocess the data.
        """
        self.data["Date"] = pd.to_datetime(self.data["Date"])
        # Sort ascending by date
        self.data.sort_values(by=["Date"], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    @override
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

        # If no start date is specified, set it to the first date in the data
        if start_date is None:
            start_date = self.data["Date"].iloc[0]
        # If no end date is specified, set it to the last date in the data
        if end_date is None:
            end_date = self.data["Date"].iloc[-1]

        return self.data[
            (self.data["Date"] >= start_date) & (self.data["Date"] <= end_date)
        ]

    @override
    @lru_cache(maxsize=1)
    def get_all_tickers(self) -> list:
        """
        Get all the unique tickers in the data.
        """
        return list(self.data["Symbol"].unique())
