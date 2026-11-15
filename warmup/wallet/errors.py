class WalletError(Exception):
    pass

class InvalidAmountError(WalletError):
    pass

class UnsupportedCurrencyError(WalletError):
    pass

class InsufficientFundsError(WalletError):
    pass

class MissingRateError(WalletError):
    pass
