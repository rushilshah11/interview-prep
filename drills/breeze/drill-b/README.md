# Breeze Drill B: add a list endpoint to an existing API, AI on partway

**Time box:** 30 minutes.
**AI:** none for the first 10 minutes. After that, AI is allowed. This copies Breeze's "the interviewer will tell you when". At the 10-minute mark, say out loud: "Is it OK if I use AI for this part?" and then switch.
**Grading:** the Breeze prep guide.

## What's here
A small FastAPI app in `txns/` with 23 seeded transactions. You can get one transaction or create one. `tests/test_existing.py` passes. There are no docstrings.

## The ask

> The merchant dashboard needs a transactions page. Add an endpoint to list transactions, with filters and pagination, so the frontend can show a table.

## Steps
1. **Orient, no AI (3 min).** Run the tests, skim the two files, and say how a request flows.
2. **Clarify, no AI (3 min).** Write your questions in `notes.md`, then open `../_answers/drill-b-interviewer.md`.
3. **Blueprint, no AI (4 min).** Write it in `notes.md`: the route, its query params, the response shape, where the filtering logic goes (not in the route), and the errors.
4. **Build, AI on.** Work in slices: filters, then pagination, then validating the query params. Use the playbook loop on every slice: guess, prompt with a constraint, check the diff, say what changed.
5. **Test.** Write your own tests in `tests/test_list.py`. For any test the AI writes, have it list each test's name and the one behavior it proves.
6. **Wrap up.** In `notes.md`: what you built, one tradeoff, and what changes at 10 million rows.

## Done when
- `pytest -q` passes and `tests/test_existing.py` wasn't edited.
- Bad query params return 400 with a clear message, never a 500.

Then compare with `../_answers/drill-b.md`.
