"""Exceptions raised by the wallet core."""


class WalletError(Exception):
    """Base class for every wallet error."""


class InvalidAmountError(WalletError):
    """The amount is not a usable number, or is not positive."""


class UnsupportedCurrencyError(WalletError):
    """The currency is not one the wallet supports."""


class InsufficientFundsError(WalletError):
    """The wallet does not hold enough of a currency for the operation."""


class MissingRateError(WalletError):
    """There is no exchange rate for the requested currency pair."""
