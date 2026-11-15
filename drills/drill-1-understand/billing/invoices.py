from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from billing.plans import price_of

TAX_RATE = Decimal("0.08875")
CENT = Decimal("0.01")


@dataclass
class Invoice:
    id: str
    customer: str
    plan: str
    period_start: date
    period_end: date
    subtotal: Decimal
    tax: Decimal
    status: str = "open"

    @property
    def total(self) -> Decimal:
        return self.subtotal + self.tax


class Invoices:
    def __init__(self):
        self._by_id: dict[str, Invoice] = {}
        self._n = 0

    def create(self, customer: str, plan: str, start: date, end: date) -> Invoice:
        subtotal = price_of(plan)
        tax = (subtotal * TAX_RATE).quantize(CENT, rounding=ROUND_HALF_UP)
        self._n += 1
        inv = Invoice(f"inv_{self._n}", customer, plan, start, end, subtotal, tax)
        self._by_id[inv.id] = inv
        return inv

    def mark_paid(self, invoice_id: str) -> None:
        self._by_id[invoice_id].status = "paid"

    def for_customer(self, customer: str) -> list[Invoice]:
        return [i for i in self._by_id.values() if i.customer == customer]
