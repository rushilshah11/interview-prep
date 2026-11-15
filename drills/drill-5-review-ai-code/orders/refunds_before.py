# The version BEFORE the AI's change. Kept for comparison; not imported anywhere.
from __future__ import annotations

from orders.store import RefundError, get_order


def refund_order(order_id: str):
    order = get_order(order_id)
    if order.status != "paid":
        raise RefundError(f"{order_id} is {order.status}, only paid orders can be refunded")
    order.refunds.append(order.total)
    order.status = "refunded"
    return order.total
