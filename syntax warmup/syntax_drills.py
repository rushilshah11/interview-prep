"""
Python syntax warm-up: the idioms that show up in payments-style mocks.

How to use (20-30 min):
  1. Fill in each function from memory. No AI, no autocomplete.
     If you blank on something, look it up in the Python docs, then retype it yourself.
  2. Run:  python syntax_drills.py
     Every drill prints PASS or FAIL. Fix the FAILs.
  3. Tomorrow morning, delete your answers and do it again, faster.
"""
from collections import defaultdict, Counter, deque
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
import heapq


# ---------- 1. Dictionaries ----------

def count_words(words):
    """Return a dict of word -> count, using a plain dict and .get()."""
    rtn = {}
    for word in words:
        rtn[word] = rtn.get(word, 0) + 1
    return rtn



def group_by_currency(txns):
    """txns is a list of (currency, amount) tuples.
    Return a dict of currency -> list of amounts, using defaultdict(list)."""
    rtn = defaultdict(list)
    for currency, amount in txns:
        rtn[currency].append(amount)

    return rtn

def top_two(words):
    """Return the 2 most common words as a list, using Counter."""
    counts = Counter(words)
    return [item for item, count in counts.most_common(2)]



def invert(d):
    """Return a new dict with keys and values swapped, using a dict comprehension."""
    # TODO
    inverted = {}
    for key, value in d.items():
        inverted[value] = key
    return inverted

    


def safe_lookup(balances, account_id):
    """Return balances[account_id], or Decimal('0') if it's missing. One line."""
    # TODO
    return balances.get(account_id, Decimal('0'))


# ---------- 2. Lists, sets, sorting ----------

def evens_squared(nums):
    """Return the squares of the even numbers, using a list comprehension."""
    # TODO
    squared = [x*x for x in nums if x%2==0]
    return squared


def missing_ids(ledger_ids, bank_ids):
    """Return a sorted list of ids that are in bank_ids but not ledger_ids, using sets."""
    # TODO
    return sorted(set(bank_ids) - set(ledger_ids))


def sort_txns(txns):
    """txns is a list of dicts with 'timestamp' and 'amount'.
    Return them sorted by timestamp ascending, then amount descending."""
    # TODO
    return sorted(txns, key=lambda x: (x['timestamp'], -x['amount']))


def pairs_with_index(items):
    """Return a list of 'index: item' strings, using enumerate and an f-string."""
    # TODO
    return [f"{index}: {item}" for index, item in enumerate(items)]


# ---------- 3. Money ----------

def apply_fee(amount):
    """amount is a Decimal. Return amount minus a 2.9% + 0.30 fee,
    rounded to 2 decimal places with ROUND_HALF_UP."""
    # TODO
    fee = amount * Decimal("0.029") + Decimal("0.30")
    return (amount - fee).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ---------- 4. Classes, enums, errors ----------

class Status(Enum):
    # TODO: CREATED, AUTHORIZED, CAPTURED as string values
    CREATED = 'created'
    AUTHORIZED = 'authorized'
    CAPTURED = 'captured'


class InsufficientFunds(Exception):
    # TODO: a custom exception (the body can be just `pass`)
    pass


@dataclass
class Account:
    account_id: str
    # TODO: balance: Decimal defaulting to Decimal("0")
    balance: Decimal = Decimal("0")
    # TODO: history: list defaulting to an empty list (careful: use field(default_factory=...))
    history: list = field(default_factory=list)

    def withdraw(self, amount):
        """Raise ValueError if amount <= 0, InsufficientFunds if amount > balance.
        Otherwise subtract it and append ('withdraw', amount) to history."""
        # TODO
        if amount <= 0:
            raise ValueError
        elif amount > self.balance:
            raise InsufficientFunds

        self.balance -= amount
        self.history.append(('withdraw', amount))


# ---------- 5. Heaps and queues ----------

def k_smallest(nums, k):
    """Return the k smallest numbers in ascending order, using heapq."""
    # TODO
    return heapq.nsmallest(k, nums)


def process_queue(tasks):
    """Use a deque: pop from the left until empty, collecting tasks in order."""
    # TODO
    rtn = []
    d = deque(tasks)
    while d:
        rtn.append(d.popleft())
    return rtn


# ---------- checks (don't edit) ----------

def _eq(got, want):
    assert got == want, f"got {got!r}, want {want!r}"


def check(name, fn):
    try:
        fn()
        print(f"PASS  {name}")
    except Exception as e:
        print(f"FAIL  {name}: {type(e).__name__} {e}")


def _account():
    a = Account("alice", Decimal("10"))
    a.withdraw(Decimal("3"))
    assert a.balance == Decimal("7") and a.history == [("withdraw", Decimal("3"))]
    for bad, err in [(Decimal("0"), ValueError), (Decimal("100"), InsufficientFunds)]:
        try:
            a.withdraw(bad)
            raise AssertionError(f"withdraw({bad}) should raise {err.__name__}")
        except err:
            pass
    assert Account("bob").history == [] and Account("bob").history is not Account("carl").history


if __name__ == "__main__":
    check("count_words", lambda: _eq(count_words(["a", "b", "a"]), {"a": 2, "b": 1}))
    check("group_by_currency", lambda: _eq(dict(group_by_currency([("USD", 1), ("EUR", 2), ("USD", 3)])), {"USD": [1, 3], "EUR": [2]}))
    check("top_two", lambda: _eq(top_two(["x", "y", "x", "z", "y", "x"]), ["x", "y"]))
    check("invert", lambda: _eq(invert({"a": 1, "b": 2}), {1: "a", 2: "b"}))
    check("safe_lookup", lambda: _eq((safe_lookup({"a": Decimal("5")}, "a"), safe_lookup({}, "z")), (Decimal("5"), Decimal("0"))))
    check("evens_squared", lambda: _eq(evens_squared([1, 2, 3, 4]), [4, 16]))
    check("missing_ids", lambda: _eq(missing_ids(["t1", "t2"], ["t3", "t1", "t0"]), ["t0", "t3"]))
    check("sort_txns", lambda: _eq([t["amount"] for t in sort_txns([{"timestamp": 2, "amount": 5}, {"timestamp": 1, "amount": 1}, {"timestamp": 2, "amount": 9}])], [1, 9, 5]))
    check("pairs_with_index", lambda: _eq(pairs_with_index(["a", "b"]), ["0: a", "1: b"]))
    check("apply_fee", lambda: _eq(apply_fee(Decimal("100.00")), Decimal("96.80")))
    check("Status enum", lambda: _eq(Status("captured"), Status.CAPTURED))
    check("Account + errors", _account)
    check("k_smallest", lambda: _eq(k_smallest([5, 1, 4, 2, 3], 3), [1, 2, 3]))
    check("process_queue", lambda: _eq(process_queue(["a", "b", "c"]), ["a", "b", "c"]))

