from decimal import Decimal


class AccountAlreadyExistsError(Exception):
    """Raised when creating an account whose ID is already registered."""


class AccountDoesntExistError(Exception):
    """Raised when operating on an account ID that isn't registered."""


class InvalidAmountError(ValueError):
    """Raised when an amount is not a positive, finite number."""


def to_decimal(value: int | float | Decimal) -> Decimal:
    """Convert an int, float, or Decimal to Decimal.

    Floats go through str() first so Decimal(0.1) doesn't become
    0.1000000000000000055511151231257827021181583404541015625.
    """
    if isinstance(value, bool):
        raise TypeError("bool is not a valid amount")
    if isinstance(value, Decimal):
        return value
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        return Decimal(str(value))
    raise TypeError(f"Unsupported amount type: {type(value).__name__}")


class Ledger:
    def __init__(self) -> None:
        self._balances: dict[str, Decimal] = {}

    def create_account(self, account_id: str) -> Decimal:
        """Register a new account with a zero balance."""
        if account_id in self._balances:
            raise AccountAlreadyExistsError(f"Account {account_id!r} already exists")
        self._balances[account_id] = Decimal("0")
        return self._balances[account_id]

    def deposit(self, account_id: str, amount: int | float | Decimal) -> Decimal:
        """Add money to an existing account."""
        if account_id not in self._balances:
            raise AccountDoesntExistError(f"Account {account_id!r} does not exist")
        amount = to_decimal(amount)
        if not amount.is_finite() or amount <= 0:
            raise InvalidAmountError(f"Deposit amount must be positive, got {amount}")
        cents = amount.quantize(Decimal("0.01"))
        if amount != cents:
            raise InvalidAmountError(
                f"Deposit amount can have at most 2 decimal places, got {amount}"
            )
        self._balances[account_id] += cents
        return self._balances[account_id]

    def get_balance(self, account_id: str) -> Decimal:
        """Return the account's current balance."""
        if account_id not in self._balances:
            raise AccountDoesntExistError(f"Account {account_id!r} does not exist")
        return self._balances[account_id]
