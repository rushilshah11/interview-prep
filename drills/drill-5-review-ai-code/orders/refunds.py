from __future__ import annotations

from orders.notify import send_email
from orders.store import RefundError, get_order


def refund_order(id: str, amount=None):
    order = get_order(id)
    amount = float(order.total if amount is None else amount)
    if amount <= 0:
        raise RefundError("Refund amount must be positive")
    if amount > order.total:
        raise RefundError(f"Refund {amount} exceeds order total {order.total}")
    order.refunds.append(amount)
    order.status = "refunded"
    print(f"Refunded {amount} for {id}")
    send_email(order.customer, f"Your refund of ${amount} is on its way!")
    return amount
