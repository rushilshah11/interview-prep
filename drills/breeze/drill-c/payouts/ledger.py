from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from decimal import Decimal

MIN_PAYOUT = Decimal("1.00")


class PayoutError(Exception):
    def __init__(self, code: str, message: str, status: int):
        super().__init__(message)
        self.code, self.message, self.status = code, message, status


@dataclass
class Txn:
    id: str
    amount: Decimal
    status: str
    paid_out: bool = False


@dataclass
class Merchant:
    id: str
    txns: list[Txn] = field(default_factory=list)
    payouts: list[dict] = field(default_factory=list)


class Ledger:
    def __init__(self):
        self.merchants: dict[str, Merchant] = {}
        self._ids = itertools.count(1)

    def add_merchant(self, merchant_id: str) -> Merchant:
        m = Merchant(merchant_id)
        self.merchants[merchant_id] = m
        return m

    def add_txn(self, merchant_id: str, amount, status: str) -> Txn:
        t = Txn(f"t{next(self._ids)}", Decimal(str(amount)), status)
        self.merchants[merchant_id].txns.append(t)
        return t

    def create_payout(self, merchant_id: str) -> dict:
        m = self.merchants[merchant_id]
        due = [t for t in m.txns if t.status != "pending" and not t.paid_out]
        total = sum((t.amount for t in due), Decimal("0"))
        for t in due:
            t.paid_out = True
        if total < MIN_PAYOUT:
            raise PayoutError("below_minimum", f"payout {total} is below {MIN_PAYOUT}", 422)
        payout = {"id": f"po{len(m.payouts) + 1}", "merchant_id": merchant_id, "amount": float(total), "txn_ids": [t.id for t in due]}
        m.payouts.append(payout)
        return payout
