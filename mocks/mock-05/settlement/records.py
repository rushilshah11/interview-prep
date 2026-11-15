from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

CURRENCIES = frozenset({"USD", "USDC", "EUR"})
TYPES = frozenset({"sale", "refund", "chargeback", "adjustment"})
REQUIRED = ("id", "merchant_id", "type", "amount", "currency", "timestamp")


class InvalidRecord(Exception):
    def __init__(self, record_id, reason):
        """Store the offending record id and the reason it failed validation."""
        super().__init__(f"{record_id}: {reason}")
        self.record_id = record_id
        self.reason = reason


@dataclass(frozen=True)
class Txn:
    id: str
    merchant_id: str
    type: str
    amount: Decimal
    currency: str
    timestamp: str


def parse(raw: dict) -> Txn:
    """Validate a raw record dict and convert it to a Txn, raising InvalidRecord on bad input."""
    rid = raw.get("id", "<no id>")
    missing = [k for k in REQUIRED if raw.get(k) in (None, "")]
    if missing:
        raise InvalidRecord(rid, f"missing {', '.join(missing)}")
    if raw["type"] not in TYPES:
        raise InvalidRecord(rid, f"unknown type {raw['type']!r}")
    if raw["currency"] not in CURRENCIES:
        raise InvalidRecord(rid, f"unsupported currency {raw['currency']!r}")
    try:
        amount = Decimal(str(raw["amount"]))
    except InvalidOperation:
        raise InvalidRecord(rid, f"bad amount {raw['amount']!r}")
    if amount == 0:
        raise InvalidRecord(rid, "amount must be non-zero")
    if amount < 0 and raw["type"] != "adjustment":
        raise InvalidRecord(rid, f"amount must be positive, got {amount}")
    return Txn(rid, raw["merchant_id"], raw["type"], amount, raw["currency"], raw["timestamp"])
