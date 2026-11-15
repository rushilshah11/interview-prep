from decimal import ROUND_HALF_UP, Decimal
from wallet.money import CENT, to_positive_money, validate_currency
from wallet.errors import InsufficientFundsError
from wallet.wallet import Wallet
FEE_RATE = Decimal('0.005')
MIN_FEE = Decimal('0.01')

def calculate_fee(amount: Decimal) -> Decimal:
    fee = (amount * FEE_RATE).quantize(CENT, rounding=ROUND_HALF_UP)
    return max(fee, MIN_FEE)

def transfer(sender: Wallet, receiver: Wallet, fees: Wallet, currency: str, amount) -> Decimal:
    validate_currency(currency)
    value = to_positive_money(amount)
    fee = calculate_fee(value)
    total = value + fee
    if total > sender.balance(currency):
        raise InsufficientFundsError(f'{sender.owner} has {sender.balance(currency)} {currency}, needs {total} ({value} + {fee} fee)')
    sender.withdraw(currency, value, kind='transfer_out')
    receiver.deposit(currency, value, kind='transfer_in')
    sender.withdraw(currency, fee, kind='fee')
    fees.deposit(currency, fee, kind='fee')
    return fee
