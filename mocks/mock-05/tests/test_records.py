from decimal import Decimal

import pytest

from settlement.records import InvalidRecord, parse
from tests.helpers import rec


def test_parses_valid_record():
    t = parse(rec(amount="12.50"))
    assert t.amount == Decimal("12.50") and t.type == "sale"


@pytest.mark.parametrize("over", [
    {"merchant_id": ""},
    {"type": "payout"},
    {"currency": "GBP"},
    {"amount": "abc"},
    {"amount": "-5"},
    {"amount": "0"},
])
def test_rejects_bad_records(over):
    with pytest.raises(InvalidRecord):
        parse(rec(**over))
