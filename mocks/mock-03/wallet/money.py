"""Helpers for turning caller input into safe money values."""

from decimal import ROUND_HALF_UP, Decimal

from wallet.errors import InvalidAmountError, UnsupportedCurrencyError

SUPPORTED_CURRENCIES = frozenset({"USD", "USDC", "EUR"})
CENT = Decimal("0.01")


def to_money(value: int | float | Decimal) -> Decimal:
    """Convert an int, float or Decimal into a Decimal rounded to cents (half up)."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise InvalidAmountError(f"Amount must be a number, got {type(value).__name__}")

    if isinstance(value, float):
        amount = Decimal(str(value))
    else:
        amount = Decimal(value)
    if not amount.is_finite():
        raise InvalidAmountError(f"Amount must be finite, got {value}")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def to_positive_money(value: int | float | Decimal) -> Decimal:
    """Like to_money, but also rejects zero and negative amounts."""
    amount = to_money(value)
    if amount <= 0:
        raise InvalidAmountError(f"Amount must be positive, got {amount}")
    return amount


def validate_currency(currency: str) -> None:
    """Raise UnsupportedCurrencyError unless the currency is supported."""
    if currency not in SUPPORTED_CURRENCIES:
        raise UnsupportedCurrencyError(f"Unsupported currency: {currency!r}")
