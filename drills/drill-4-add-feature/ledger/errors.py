class LedgerError(Exception):
    """Base class for every error the ledger raises."""


class UnknownAccount(LedgerError):
    """Raised when an account id is not in the ledger."""


class InvalidAmount(LedgerError):
    """Raised when an amount is a bool, not numeric, or not positive."""


class InsufficientFunds(LedgerError):
    """Raised when an amount exceeds the account balance."""


class DuplicateHold(LedgerError):
    """Raised when place_hold is called with a hold_id that is already active on the account."""
