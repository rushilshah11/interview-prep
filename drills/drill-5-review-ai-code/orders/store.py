from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Order:
    id: str
    customer: str
    total: Decimal
    status: str = "pending"
    refunds: list = field(default_factory=list)


class OrderNotFound(Exception):
    pass


class RefundError(Exception):
    pass


ORDERS: dict[str, Order] = {}


def get_order(order_id: str) -> Order:
    if order_id not in ORDERS:
        raise OrderNotFound(order_id)
    return ORDERS[order_id]
