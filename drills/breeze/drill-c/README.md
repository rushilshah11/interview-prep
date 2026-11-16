# Breeze Drill C: debug a payouts API, no AI

**Time box:** 20 minutes. **AI:** none. This counts as practice for Rokt's code review round too.
**Grading:** the Breeze prep guide, mainly correctness and edge cases, testing and debugging, and communication.

## What's here
A FastAPI payouts API. A merchant's succeeded transactions get paid out in one payout, there's a 1.00 minimum, and a transaction is never paid twice. `tests/test_payouts.py` is the spec. All 7 tests fail right now. There are no docstrings.

## Steps
1. **Run the tests and say what you see.** All 7 fail. Before reading any code, guess out loud whether this is one root cause or several.
2. **Fix the root cause first, then re-run.** When one bug hides others, the failure list changes after each fix. Read it again each time.
3. **For each bug, write one line in `notes.md`:** the symptom, the cause, the fix, and which test proves it.
4. **Look for what the tests miss.** Find one more problem the tests don't catch, and write a test for it.

## Done when
- All 7 tests pass and you didn't edit `test_payouts.py`.
- `notes.md` has one line per bug, plus your extra test.

Then compare with `../_answers/drill-c.md`.
