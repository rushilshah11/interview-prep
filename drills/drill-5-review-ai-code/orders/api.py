from orders.refunds import refund_order


def handle_refund_request(payload: dict) -> dict:
    refunded = refund_order(order_id=payload["order_id"], amount=payload.get("amount"))
    return {"ok": True, "refunded": str(refunded)}
