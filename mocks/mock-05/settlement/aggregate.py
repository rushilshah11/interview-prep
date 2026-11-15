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
    adjustments: Decimal = ZERO

    @property
    def gross(self) -> Decimal:
        """Sales minus refunds and chargebacks, before fees."""
        return self.sales - self.refunds - self.chargebacks + self.adjustments

    @property
    def net(self) -> Decimal:
        """Gross amount minus fees."""
        return self.gross - self.fees


_BUCKET = {"sale": "sales", "refund": "refunds", "chargeback": "chargebacks", "adjustment": "adjustments"}


def totals_by_merchant(txns: Iterable[Txn]) -> dict[tuple[str, str], Totals]:
    """Sum amounts by transaction type, plus fees, for each (merchant, currency) key."""
    out: dict[tuple[str, str], Totals] = defaultdict(Totals)
    for t in txns:
        key = (t.merchant_id, t.currency)
        bucket = _BUCKET[t.type]
        setattr(out[key], bucket, getattr(out[key], bucket) + t.amount)
        out[key].fees += fee_for(t)
    return dict(out)
