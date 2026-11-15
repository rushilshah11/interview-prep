from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from payments.errors import InvalidAmount, UnsupportedCurrency

CURRENCIES = frozenset({"USD", "USDC", "EUR"})
CENT = Decimal("0.01")


def parse_amount(value) -> Decimal:
    """Convert a raw value to a positive, finite Decimal rounded half-up to cents, raising InvalidAmount otherwise."""
    if isinstance(value, bool):
        raise InvalidAmount(f"not a number: {value!r}")
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise InvalidAmount(f"not a number: {value!r}")
    if not d.is_finite():
        raise InvalidAmount(f"not finite: {value!r}")
    d = d.quantize(CENT, rounding=ROUND_HALF_UP)
    if d <= 0:
        raise InvalidAmount(f"must be positive: {value!r}")
    return d


def check_currency(code: str) -> str:
    """Return the currency code if it is supported, raising UnsupportedCurrency otherwise."""
    if code not in CURRENCIES:
        raise UnsupportedCurrency(code)
    return code
