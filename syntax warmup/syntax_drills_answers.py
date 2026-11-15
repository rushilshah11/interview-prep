"""Answer key for syntax_drills.py. Only open this after you've tried every drill."""
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import heapq


def count_words(words):
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts


def group_by_currency(txns):
    groups = defaultdict(list)
    for currency, amount in txns:
        groups[currency].append(amount)
    return groups


def top_two(words):
    return [w for w, _ in Counter(words).most_common(2)]


def invert(d):
    return {v: k for k, v in d.items()}


def safe_lookup(balances, account_id):
    return balances.get(account_id, Decimal("0"))


def evens_squared(nums):
    return [n * n for n in nums if n % 2 == 0]


def missing_ids(ledger_ids, bank_ids):
    return sorted(set(bank_ids) - set(ledger_ids))


def sort_txns(txns):
    return sorted(txns, key=lambda t: (t["timestamp"], -t["amount"]))


def pairs_with_index(items):
    return [f"{i}: {item}" for i, item in enumerate(items)]


def apply_fee(amount):
    fee = amount * Decimal("0.029") + Decimal("0.30")
    return (amount - fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Status(Enum):
    CREATED = "created"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"


class InsufficientFunds(Exception):
    pass


@dataclass
class Account:
    account_id: str
    balance: Decimal = Decimal("0")
    history: list = field(default_factory=list)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds(f"{self.account_id} has {self.balance}, needs {amount}")
        self.balance -= amount
        self.history.append(("withdraw", amount))


def k_smallest(nums, k):
    return heapq.nsmallest(k, nums)
    # or: heapq.heapify(nums) then [heapq.heappop(nums) for _ in range(k)]


def process_queue(tasks):
    q = deque(tasks)
    done = []
    while q:
        done.append(q.popleft())
    return done
