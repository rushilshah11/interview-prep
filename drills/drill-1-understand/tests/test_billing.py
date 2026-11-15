from datetime import date
from decimal import Decimal

import pytest

from billing.invoices import Invoices
from billing.plans import UnknownPlan
from billing.subscriptions import State, SubscriptionError, Subscriptions

D0 = date(2026, 1, 1)


def make(charge_results):
    results = iter(charge_results)
    inv = Invoices()
    return Subscriptions(inv, lambda customer, amount: next(results)), inv


def test_trial_then_paid_renewal():
    subs, inv = make([True])
    s = subs.start("c1", "pro", D0)
    assert s.state == State.TRIAL
    assert subs.renew(s.id, date(2026, 1, 10)) is None
    bill = subs.renew(s.id, date(2026, 1, 15))
    assert bill.status == "paid" and bill.total == Decimal("31.57")
    assert s.state == State.ACTIVE and s.period_end == date(2026, 2, 14)


def test_three_failures_cancel():
    subs, inv = make([False, False, False])
    s = subs.start("c1", "basic", D0)
    for _ in range(3):
        subs.renew(s.id, date(2026, 1, 15))
    assert s.state == State.CANCELED
    with pytest.raises(SubscriptionError):
        subs.renew(s.id, date(2026, 1, 16))


def test_unknown_plan():
    subs, _ = make([])
    with pytest.raises(UnknownPlan):
        subs.start("c1", "gold", D0)
