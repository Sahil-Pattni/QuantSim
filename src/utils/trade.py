import datetime


class Trade:
    def __init__(
        self, ticker: str, action: str, price: float, amount: float, time: datetime
    ) -> None:
        """
        Initialize a trade.

        Args:
            ticker (str): The ticker of the asset.
            action (str): The action of the trade.
            price (float): The price of the asset.
            amount (float): The amount of the asset.
            time (datetime): The time of the trade.
        """
        self.action = action.upper()
        # Just to be safe, make sure the action is valid
        if self.action not in ["BUY", "SELL"]:
            raise ValueError(f"`action` must be either 'BUY' or 'SELL', not {action}")

        self.ticker = ticker
        self.price = price
        self.amount = amount
        self.time = time

    def __str__(self) -> str:
        """
        Get a string representation of the trade.

        Returns:
            str: The string representation of the trade.
        """
        return f"[{self.time}] {self.action} {self.amount:,.3f} {self.ticker:,.3f} @ ${self.price:.3f}"

    def to_list(self):
        """
        Get a list representation of the trade.

        Returns:
            list: The list representation of the trade.
        """
        return [self.action, self.amount, self.ticker, self.price, self.time]
