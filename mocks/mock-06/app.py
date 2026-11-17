"""Thin FastAPI routes. All logic lives in PaymentsService."""

from fastapi import Depends, FastAPI, status

from errors import register_exception_handlers
from models import PaymentIn, PaymentOut
from service import PaymentsService

app = FastAPI(title="Payments Service")
register_exception_handlers(app)

_service = PaymentsService()


def get_service() -> PaymentsService:
    """Dependency so tests can swap in a fresh service via dependency_overrides."""
    return _service


@app.post("/payments", response_model=PaymentOut, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_in: PaymentIn, service: PaymentsService = Depends(get_service)
) -> PaymentOut:
    return service.create_payment(
        merchant_id=payment_in.merchant_id,
        amount=payment_in.amount,
        currency=payment_in.currency,
        idempotency_key=payment_in.idempotency_key,
    )


@app.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(
    payment_id: str, service: PaymentsService = Depends(get_service)
) -> PaymentOut:
    return service.get_payment(payment_id)
