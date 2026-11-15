# Drill 4: Add a feature without breaking anything

**Playbook phases:** 2 · Clarify and plan ("Blast radius", "Scope it"), 3 · Build simple, 4 · Verify ("Review the diff"), 6 · Harden
**Time box:** 25 minutes
**What's here:** a working ledger (accounts, deposit, withdraw, transfer, statement). `tests/test_ledger.py` passes. Product wants **holds**: reserve money for a pending card payment without moving it yet. `tests/test_holds.py` is the spec and fails right now.

## The loop (every change)
1. **Say** what you're about to change and what it could break. "Holds change what 'enough money' means, so withdraw and transfer both need to check available, not balance."
2. **Prompt** with that plan and a constraint: "smallest change", "reuse `money()` and the existing errors", "don't touch statement()".
3. **Check** the diff line by line. Did the AI touch anything you didn't ask for? Did it reinvent a helper that already exists? Did it add behavior nobody asked for (that you now have to decide on)?
4. **Say** one sentence about the result, then run **both** test files.

## Steps
1. Run `pytest -q`. Read `test_holds.py` first: it's the spec. Write the API you'll add in `notes.md`.
2. **Blast radius:** before coding, ask what relies on `balance` and what your change could break. Write your own answer first.
3. Ask the interviewer questions (write them in `notes.md`): should a captured hold show up in the statement? Can a hold expire? Can you hold on an account with zero balance?
4. Build in layers, one prompt each: `available()` → `place_hold` → withdraw/transfer use available → `release_hold` → `capture_hold`. Read each diff before the next prompt.
5. **Harden:** try to break it. Release a hold twice. Capture to an unknown account. What happens to the hold if capture fails halfway?

## Done when
- Both test files pass and `test_ledger.py` was never edited.
- `notes.md` has your blast-radius answer, your interviewer questions, and anything the AI changed that you didn't ask for (and what you did about it).

Then compare with `../_answers/drill-4.md`.
