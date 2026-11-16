# Drill C: answer key

There are 5 bugs. All 7 tests fail at first, mostly because of bug 1, which hides the others.

1. **Money serialized as a float** (`ledger.py`, `"amount": float(total)`). JSON gets `15.5` instead of `"15.50"`, and `0.1 + 0.2` can drift. Fix: `str(total)`. This is the root cause: fix it first, and then the remaining failures become readable.
2. **Failed transactions get paid out** (`t.status != "pending"`). The filter excludes only pending, so failed and refunded transactions slip through. Fix: `t.status == "succeeded"`. The lesson: write the filter as the allowed list, not as exclusions.
3. **A rejected payout still marks transactions paid.** It sets `paid_out = True` before checking `MIN_PAYOUT`, so a rejected 0.50 payout eats those transactions forever. Fix: run every check first, then mutate. It's the same all-or-nothing rule as Drill 4.
4. **Errors return 200** (`app.py`). The `@app.exception_handler(PayoutError)` returns `JSONResponse(...)` without `status_code=e.status`, and JSONResponse defaults to 200. Fix: pass `status_code=e.status`. Your Ledger already had a 422; the handler dropped it.
5. **An unknown merchant is a 500** (a `KeyError` on `self.merchants[merchant_id]` in both the ledger and the GET route). Fix: `.get()` plus a 404 `PayoutError`, which the exception handler turns into a 404. Note that the test client uses `raise_server_exceptions=False`, so you see the 500 a real client would get instead of a traceback.

## Things the tests miss (good extra tests)
- `add_merchant` silently overwrites an existing merchant (the same quirk as the Drill 4 ledger).
- Payout ids come from `len(m.payouts) + 1`, so they're only unique per merchant.
- Two concurrent payout requests could pay the same transactions twice. In production you'd need a lock or a DB transaction with a "claimed" status.
- A payout when nothing is due raises `below_minimum` with total 0. That's arguably fine, but a `nothing_to_pay` code would be clearer.

## What good narration sounds like
"All 7 fail, including the simple sum test, so I think there's one cross-cutting cause, probably in how the amount is returned. Fixing that first. ... Now 3 fail, and they look like separate bugs: the status filter, the order of the minimum check, and the 404."
