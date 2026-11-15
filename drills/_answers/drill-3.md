# Drill 3 answer key

**Bugs your tests should catch:**

1. **Shares don't add up to the total.** `allocate(10, [1, 1, 1])` returns `[3.33, 3.33, 3.33]` = 9.99. A cent disappears. Every share is rounded down and the leftover cents are never handed out. Fix: after rounding down, give the leftover cents one at a time to the first (or largest) shares. Test: `sum(allocate(10, [1, 1, 1])) == Decimal("10.00")`.
2. **Negative weights are accepted.** `allocate(100, [3, -1])` returns `[150.00, -50.00]`. Fix: reject any weight `<= 0`... or decide zero weights are allowed (a person who owes nothing) and only reject negatives. That's a great clarifying question to ask out loud.
3. **All-zero weights crash with a raw Decimal error** (`DivisionByZero` / `InvalidOperation`) instead of an `AllocationError`. Test: `pytest.raises(AllocationError)` for `allocate(100, [0, 0])`.
4. **`split_evenly(total, 0)` raises "need at least one weight"**, which is confusing for the caller, and **`split_evenly(10, -1)`** does the same. Worth a clearer error naming `people`.
5. **`to_money` rounds the *total* down before splitting**, so `allocate("10.005", [1])` returns 10.00 silently. Debatable: a good test plus a clarifying question ("should sub-cent totals be rejected?").
6. **`split_bill` inherits bug 1.** `split_bill(100, 18, {"a": 1, "b": 1, "c": 1})` should sum to 118.00 but sums to 117.99.

**Tests that should pass (and are still worth writing):** single weight gets the whole amount; weights 1:3 split 25/75; string and float totals work (`"12.50"`, `12.5`); non-numeric total raises `AllocationError`; zero or negative total raises; empty weights raises.
