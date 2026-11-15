from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum
from typing import Callable

from billing.invoices import Invoice, Invoices
from billing.plans import price_of

TRIAL_DAYS = 14
PERIOD_DAYS = 30
MAX_FAILED = 3


class State(str, Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"


class SubscriptionError(Exception):
    pass


@dataclass
class Subscription:
    id: str
    customer: str
    plan: str
    state: State
    period_end: date
    failed: int = 0


class Subscriptions:
    def __init__(self, invoices: Invoices, charge: Callable[[str, object], bool]):
        self._subs: dict[str, Subscription] = {}
        self._invoices = invoices
        self._charge = charge
        self._n = 0

    def get(self, sub_id: str) -> Subscription:
        if sub_id not in self._subs:
            raise SubscriptionError(f"no subscription {sub_id}")
        return self._subs[sub_id]

    def start(self, customer: str, plan: str, today: date) -> Subscription:
        price_of(plan)
        self._n += 1
        sub = Subscription(f"sub_{self._n}", customer, plan, State.TRIAL, today + timedelta(days=TRIAL_DAYS))
        self._subs[sub.id] = sub
        return sub

    def renew(self, sub_id: str, today: date) -> Invoice | None:
        sub = self.get(sub_id)
        if sub.state == State.CANCELED:
            raise SubscriptionError(f"{sub_id} is canceled")
        if today < sub.period_end:
            return None
        inv = self._invoices.create(sub.customer, sub.plan, sub.period_end, sub.period_end + timedelta(days=PERIOD_DAYS))
        if self._charge(sub.customer, inv.total):
            self._invoices.mark_paid(inv.id)
            sub.state = State.ACTIVE
            sub.period_end += timedelta(days=PERIOD_DAYS)
            sub.failed = 0
        else:
            sub.failed += 1
            sub.state = State.CANCELED if sub.failed >= MAX_FAILED else State.PAST_DUE
        return inv

    def change_plan(self, sub_id: str, plan: str) -> None:
        price_of(plan)
        sub = self.get(sub_id)
        if sub.state == State.CANCELED:
            raise SubscriptionError(f"{sub_id} is canceled")
        sub.plan = plan

    def cancel(self, sub_id: str) -> None:
        self.get(sub_id).state = State.CANCELED
