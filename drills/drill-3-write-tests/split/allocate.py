from __future__ import annotations

from decimal import ROUND_DOWN, Decimal, InvalidOperation

CENT = Decimal("0.01")


class AllocationError(ValueError):
    pass


def to_money(value) -> Decimal:
    try:
        d = Decimal(str(value))
    except InvalidOperation:
        raise AllocationError(f"not a number: {value!r}")
    if d <= 0:
        raise AllocationError(f"total must be positive, got {d}")
    return d.quantize(CENT, rounding=ROUND_DOWN)


def allocate(total, weights: list[int | Decimal]) -> list[Decimal]:
    amount = to_money(total)
    if not weights:
        raise AllocationError("need at least one weight")
    weight_sum = sum(Decimal(str(w)) for w in weights)
    return [(amount * Decimal(str(w)) / weight_sum).quantize(CENT, rounding=ROUND_DOWN) for w in weights]


def split_evenly(total, people: int) -> list[Decimal]:
    return allocate(total, [1] * people)
