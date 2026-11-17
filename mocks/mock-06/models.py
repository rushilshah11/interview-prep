"""Pydantic models for the payments API.

These describe the HTTP request/response shape only (required fields, JSON
types). Business rules (amount, currency) are enforced in PaymentsService so
every caller (HTTP, bulk, CSV import) gets the same checks.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, StrictInt, StrictStr


class PaymentStatus(str, Enum):
    PENDING = "pending"
    CAPTURED = "captured"
    FAILED = "failed"
    PARTIALLY_REFUNDED = "partially_refunded"
    REFUNDED = "refunded"


class Merchant(BaseModel):
    id: str
    name: str


class PaymentIn(BaseModel):
    """Request body for POST /payments. All four fields are required."""

    merchant_id: str
    # Strict so a JSON float like 10.0 is not silently coerced to int 10.
    amount: StrictStr | StrictInt
    currency: str
    idempotency_key: str


class PaymentOut(PaymentIn):
    """Response body: the request fields plus server-assigned fields."""

    # Normalized decimal string of the amount, e.g. "10.50" or "10".
    amount: str
    id: str
    status: PaymentStatus
    created_at: datetime
