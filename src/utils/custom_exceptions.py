import datetime


class InvalidTradeException(Exception):
    """
    Raised when a trade is invalid.

    Attributes:
        ticker (str): The ticker of the trade.
        amt (str): The amount of the trade.
        buy (bool): Whether or not the trade was a buy.
    """

    def __init__(self, ticker: str, amt: str, buy: bool) -> None:
        trade_type = "BUY" if buy else "SELL"

        message = f"Invalid trade: {trade_type} {ticker} {amt}"
        super().__init__(self, message)


class InvalidDateRangeException(Exception):
    """
    Raised when the date range is invalid.

    Attributes:
        start_date (datetime): The start date of the range.
        end_date (datetime): The end date of the range.
    """

    def __init__(self, start_date: datetime, end_date: datetime) -> None:
        message = f"Invalid date range: {start_date} - {end_date}"
        super().__init__(self, message)
