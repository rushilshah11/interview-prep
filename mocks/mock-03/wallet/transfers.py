"""Moving money between wallets, with a fee paid by the sender."""

from decimal import ROUND_HALF_UP, Decimal

from wallet.money import CENT, to_positive_money, validate_currency

from wallet.errors import InsufficientFundsError

from wallet.wallet import Wallet

FEE_RATE = Decimal("0.005")  # 0.5%
MIN_FEE = Decimal("0.01")


def calculate_fee(amount: Decimal) -> Decimal:
    """Fee is 0.5% of the amount, rounded half up to cents, and never less than MIN_FEE."""
    fee = (amount * FEE_RATE).quantize(CENT, rounding=ROUND_HALF_UP)
    return max(fee, MIN_FEE)


def transfer(sender: Wallet, receiver: Wallet, fees: Wallet, currency: str, amount) -> Decimal:
    """Move `amount` from sender to receiver. The sender also pays the fee, which goes
    to the `fees` wallet. Must be all-or-nothing. Returns the fee charged."""
    validate_currency(currency)
    value = to_positive_money(amount)
    fee = calculate_fee(value)

    total = value + fee
    if total > sender.balance(currency):
        raise InsufficientFundsError(
            f"{sender.owner} has {sender.balance(currency)} {currency}, needs {total} "
            f"({value} + {fee} fee)"
        )

    sender.withdraw(currency, value, kind="transfer_out")
    receiver.deposit(currency, value, kind="transfer_in")
    sender.withdraw(currency, fee, kind="fee")
    fees.deposit(currency, fee, kind="fee")
    return fee
