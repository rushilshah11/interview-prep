from __future__ import annotations

import itertools
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal

STATUSES = {"pending", "succeeded", "failed", "refunded"}


@dataclass
class Txn:
    id: str
    merchant_id: str
    amount: Decimal
    currency: str
    status: str
    created_at: datetime

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "currency": self.currency,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


class Store:
    def __init__(self):
        self._txns: dict[str, Txn] = {}
        self._ids = itertools.count(1)

    def add(self, merchant_id, amount, currency, status="pending", created_at=None) -> Txn:
        t = Txn(
            id=f"txn_{next(self._ids):04d}",
            merchant_id=merchant_id,
            amount=Decimal(str(amount)),
            currency=currency,
            status=status,
            created_at=created_at or datetime.now(timezone.utc),
        )
        self._txns[t.id] = t
        return t

    def get(self, txn_id: str) -> Txn | None:
        return self._txns.get(txn_id)

    def all(self) -> list[Txn]:
        return list(self._txns.values())


def seeded() -> Store:
    s = Store()
    start = datetime(2026, 11, 1, 9, 0, tzinfo=timezone.utc)
    merchants = ["m_acme", "m_bolt", "m_acme", "m_cora"]
    statuses = ["succeeded", "succeeded", "failed", "pending", "refunded"]
    for i in range(23):
        s.add(
            merchant_id=merchants[i % 4],
            amount=Decimal("10.00") + i,
            currency="USD" if i % 3 else "EUR",
            status=statuses[i % 5],
            created_at=start + timedelta(hours=5 * i),
        )
    return s
