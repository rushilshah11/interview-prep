from __future__ import annotations

from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from settlement.aggregate import totals_by_merchant
from settlement.records import InvalidRecord, parse

CENT = Decimal("0.01")


@dataclass
class Line:
    merchant_id: str
    currency: str
    sales: Decimal
    refunds: Decimal
    chargebacks: Decimal
    fees: Decimal
    payout: Decimal
    held: bool


@dataclass
class Report:
    lines: list[Line] = field(default_factory=list)
    errors: list[tuple[str, str]] = field(default_factory=list)

    def line(self, merchant_id: str, currency: str) -> Line:
        for ln in self.lines:
            if (ln.merchant_id, ln.currency) == (merchant_id, currency):
                return ln
        raise KeyError((merchant_id, currency))


def _q(d: Decimal) -> Decimal:
    return d.quantize(CENT, rounding=ROUND_HALF_UP)


def settle(raw_records: list[dict]) -> Report:
    report = Report()
    txns = []
    for raw in raw_records:
        try:
            txns.append(parse(raw))
        except InvalidRecord:
            continue

    for (merchant, currency), t in sorted(totals_by_merchant(txns).items()):
        held = t.gross < 0
        report.lines.append(
            Line(
                merchant_id=merchant,
                currency=currency,
                sales=_q(t.sales),
                refunds=_q(t.refunds),
                chargebacks=_q(t.chargebacks),
                fees=_q(t.fees),
                payout=Decimal("0.00") if held else _q(t.net),
                held=held,
            )
        )
    return report
