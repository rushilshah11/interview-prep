from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

from settlement.fees import fee_for
from settlement.records import Txn

ZERO = Decimal("0")


@dataclass
class Totals:
    sales: Decimal = ZERO
    refunds: Decimal = ZERO
    chargebacks: Decimal = ZERO
    fees: Decimal = ZERO

    @property
    def gross(self) -> Decimal:
        return self.sales - self.refunds - self.chargebacks

    @property
    def net(self) -> Decimal:
        return self.gross - self.fees


_BUCKET = {"sale": "sales", "refund": "refunds", "chargeback": "chargebacks"}


def totals_by_merchant(txns: Iterable[Txn]) -> dict[tuple[str, str], Totals]:
    out: dict[tuple[str, str], Totals] = defaultdict(Totals)
    for t in txns:
        key = (t.merchant_id, "ALL")
        bucket = _BUCKET[t.type]
        setattr(out[key], bucket, getattr(out[key], bucket) + t.amount)
        out[key].fees += fee_for(t)
    return dict(out)
