# Drill 4 answer key

**Blast radius:** `withdraw` and `transfer` both compare against `acct.balance`; both must use available (`balance - sum(holds)`). `deposit` and `statement` don't need to change. `test_transfer_too_much_changes_nothing` must keep passing, so the available check has to happen before anything mutates.

**A clean design (smallest change):**
- `Account` gets `holds: dict[str, Decimal] = field(default_factory=dict)` (careful: not `= {}`).
- `available(account_id)` = `balance - sum(holds.values())`.
- One private check, e.g. `_require_available(acct, value)`, raising `InsufficientFunds`; `withdraw`, `transfer` and `place_hold` all call it. Duplicating the check three times is the "quick hack" version.
- `place_hold`: `money()` the amount, reject a duplicate hold id with `LedgerError`, check available, store it.
- `release_hold`: unknown id raises `LedgerError` (pop with a check).
- `capture_hold(account_id, hold_id, to_id)`: look up both accounts **first** (so an unknown `to_id` fails before anything changes), pop the hold, then move the money and record entries (e.g. `capture_out` / `capture_in`). Order matters: if you pop the hold and then `get(to_id)` raises, the hold is gone but no money moved.

**Things the AI often does that you should catch:** adds `holds={}` as a mutable default; changes `statement()` to show holds (nobody asked); adds a new exception class when `LedgerError` / `InsufficientFunds` already fit; rewrites `withdraw`/`transfer` entirely instead of swapping one comparison; edits `test_ledger.py` to make it pass.

**Good clarifying questions:** Do holds expire? Should captures appear in the statement, and as one entry or two? Can a capture be for less than the hold (partial capture)? Is a hold on one currency only?
