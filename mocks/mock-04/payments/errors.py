class PaymentError(Exception):
    pass


class NotFound(PaymentError):
    pass


class InvalidAmount(PaymentError):
    pass


class UnsupportedCurrency(PaymentError):
    pass


class InvalidTransition(PaymentError):
    pass


class RefundTooLarge(PaymentError):
    pass


class IdempotencyConflict(PaymentError):
    pass
