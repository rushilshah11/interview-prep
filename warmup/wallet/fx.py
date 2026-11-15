from decimal import ROUND_HALF_UP, Decimal
from wallet.errors import InvalidAmountError, MissingRateError
from wallet.money import CENT, to_positive_money, validate_currency
from wallet.wallet import Wallet
DEFAULT_RATES: dict[tuple[str, str], Decimal] = {('USD', 'EUR'): Decimal('0.92'), ('EUR', 'USD'): Decimal('1.09'), ('USD', 'USDC'): Decimal('1'), ('USDC', 'USD'): Decimal('1'), ('USDC', 'EUR'): Decimal('0.92'), ('EUR', 'USDC'): Decimal('1.09')}

def convert(wallet: Wallet, from_currency: str, to_currency: str, amount, rates: dict[tuple[str, str], Decimal]=DEFAULT_RATES) -> Decimal:
    validate_currency(from_currency)
    validate_currency(to_currency)
    rate = rates.get((from_currency, to_currency))
    if rate is None:
        raise MissingRateError(f'No exchange rate for {from_currency} -> {to_currency}')
    value = to_positive_money(amount)
    credited = (value * rate).quantize(CENT, rounding=ROUND_HALF_UP)
    if credited <= 0:
        raise InvalidAmountError(f'{value} {from_currency} converts to less than one cent of {to_currency}')
    wallet.withdraw(from_currency, value, kind='convert_out')
    wallet.deposit(to_currency, credited, kind='convert_in')
    return credited
