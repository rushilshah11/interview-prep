"""Domain exceptions and the FastAPI handler that maps them to HTTP responses.

Request-shape errors (missing field, wrong JSON type, non-JSON body) use
FastAPI's built-in 422. Business-rule errors (bad amount, bad currency) are
raised by the service as InvalidPayment, also 422.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class PaymentError(Exception):
    """Base for all domain errors. Subclasses set the HTTP status code."""

    status_code: int = 500

    def __init__(self, detail: str):
        super().__init__(detail)
        self.detail = detail


class InvalidPayment(PaymentError):
    """Amount or currency breaks a business rule."""

    status_code = 422


class UnknownMerchant(PaymentError):
    status_code = 404


class PaymentNotFound(PaymentError):
    status_code = 404


class IdempotencyConflict(PaymentError):
    """Same (merchant_id, idempotency_key) reused with a different body."""

    status_code = 409


class InvalidTransition(PaymentError):
    """The payment's current status doesn't allow this action
    (e.g. refunding a pending or failed payment, capturing twice)."""

    status_code = 409


class RefundExceedsCaptured(PaymentError):
    """Refunded total would exceed the captured amount."""

    status_code = 422


async def payment_error_handler(request: Request, exc: PaymentError) -> JSONResponse:
    # Later: switch to structured JSON (code + message) here only.
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(PaymentError, payment_error_handler)
