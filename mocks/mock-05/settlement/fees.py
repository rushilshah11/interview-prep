from __future__ import annotations

from decimal import ROUND_DOWN, Decimal

from settlement.records import Txn

CENT = Decimal("0.01")

SCHEDULE = {
    "sale": (Decimal("0.029"), Decimal("0.30")),
    "refund": (Decimal("0"), Decimal("0")),
    "chargeback": (Decimal("0"), Decimal("15.00")),
}


def fee_for(txn: Txn) -> Decimal:
    pct, fixed = SCHEDULE[txn.type]
    return (txn.amount * pct + fixed).quantize(CENT, rounding=ROUND_DOWN)
