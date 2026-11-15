from __future__ import annotations

from decimal import Decimal

from split.allocate import allocate


def split_bill(subtotal, tip_percent, diners: dict[str, int]) -> dict[str, Decimal]:
    names = list(diners)
    total = Decimal(str(subtotal)) * (1 + Decimal(str(tip_percent)) / 100)
    shares = allocate(total, [diners[n] for n in names])
    return dict(zip(names, shares))
