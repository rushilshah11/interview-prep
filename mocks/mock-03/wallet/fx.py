"""Currency conversion inside a single wallet."""

from decimal import ROUND_HALF_UP, Decimal

from wallet.errors import InvalidAmountError, MissingRateError
from wallet.money import CENT, to_positive_money, validate_currency
from wallet.wallet import Wallet

# rates[(from_currency, to_currency)] = how many units of `to` you get for 1 unit of `from`
DEFAULT_RATES: dict[tuple[str, str], Decimal] = {
    ("USD", "EUR"): Decimal("0.92"),
    ("EUR", "USD"): Decimal("1.09"),
    ("USD", "USDC"): Decimal("1"),
    ("USDC", "USD"): Decimal("1"),
    ("USDC", "EUR"): Decimal("0.92"),
    ("EUR", "USDC"): Decimal("1.09"),
}


def convert(
    wallet: Wallet,
    from_currency: str,
    to_currency: str,
    amount,
    rates: dict[tuple[str, str], Decimal] = DEFAULT_RATES,
) -> Decimal:
    """Convert `amount` of from_currency into to_currency inside `wallet`.

    - Debits `amount` of from_currency and credits amount * rate of to_currency,
      rounded half up to 2 decimal places.
    - Records the debit as kind "convert_out" and the credit as kind "convert_in".
    - Rejects unsupported currencies, non-positive amounts, insufficient funds,
      and pairs missing from `rates` (MissingRateError).
    - All-or-nothing: if anything fails, no balance changes.
    - Returns the amount credited in to_currency.
    """
    # Check 1: both currencies must be supported.
    validate_currency(from_currency)
    validate_currency(to_currency)

    # Check 2: the currency pair must have a rate.
    rate = rates.get((from_currency, to_currency))
    if rate is None:
        raise MissingRateError(f"No exchange rate for {from_currency} -> {to_currency}")

    value = to_positive_money(amount)
    credited = (value * rate).quantize(CENT, rounding=ROUND_HALF_UP)
    if credited <= 0:
        # Catch this before the withdrawal, or deposit() would fail after money was debited.
        raise InvalidAmountError(
            f"{value} {from_currency} converts to less than one cent of {to_currency}"
        )

    # withdraw() checks funds before it changes anything, and the deposit can no longer fail.
    wallet.withdraw(from_currency, value, kind="convert_out")
    wallet.deposit(to_currency, credited, kind="convert_in")
    return credited


