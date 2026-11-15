from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum


class Status(str, Enum):
    CREATED = "created"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    CANCELED = "canceled"
    REFUNDED = "refunded"


TRANSITIONS = {
    Status.CREATED: {Status.AUTHORIZED, Status.CANCELED},
    Status.AUTHORIZED: {Status.CAPTURED, Status.CANCELED},
    Status.CAPTURED: {Status.REFUNDED},
    Status.CANCELED: set(),
    Status.REFUNDED: set(),
}


@dataclass
class Event:
    intent_id: str
    from_status: Status
    to_status: Status
    amount: Decimal | None = None


@dataclass
class PaymentIntent:
    id: str
    merchant_id: str
    amount: Decimal
    currency: str
    status: Status = Status.CREATED
    captured: Decimal = Decimal("0")
    refunded: Decimal = Decimal("0")

    @property
    def refundable(self) -> Decimal:
        """Return the amount still available to refund (captured minus already refunded)."""
        return self.captured - self.refunded
