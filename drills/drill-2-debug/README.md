# Drill 2: Debug failing tests

**Playbook phases:** Anytime · A test fails, and 4 · Verify ("Sort the failures")
**Time box:** 20 minutes
**What's here:** a per-API-key rate limiter (a token bucket: each key gets a bucket of tokens that refills over time; each request spends tokens). Some tests fail. There are a few real bugs; tests are correct, don't change them.

## The loop (every failure)
1. **Say** (30 sec, in `notes.md` and quietly out loud): read the exact failing line, then your guess. "test_x fails because ___. I think the bug is in ___."
2. **Prompt** using the playbook's template, with your guess and "smallest fix, don't change the test."
3. **Check** the AI's answer against the code. Does the line it points to actually do what it says? Did it change anything you didn't ask for?
4. **Say** one sentence about the root cause, then re-run all tests.

## Steps
1. Run `pytest -q`. Before opening any code, write which failures you think share a cause. Then use **Sort the failures**.
2. Fix one root cause at a time. Re-run after every fix and note which tests flipped.
3. If you have no guess, use **Trace a flow**: "Trace `refill` with these inputs and tell me what each variable ends up as."
4. If the AI claims something, use **Show me the exact line**.

## Done when
- All tests pass, and for each bug `notes.md` has: the symptom, your guess, whether the guess was right, the root cause in one sentence.
- One extra line: a test that's missing from this suite.

Then compare with `../_answers/drill-2.md`.
