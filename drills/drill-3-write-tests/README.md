# Drill 3: Write test cases

**Playbook phases:** 2 · Clarify (edge cases), 4 · Verify ("Small tests", "Fail cases")
**Time box:** 20 minutes
**What's here:** a payments helper that splits an amount across people by weight (`allocate`), splits evenly (`split_evenly`), and splits a restaurant bill with tip by how many items each person had (`split_bill`). There is exactly one test. It passes. **The code has bugs that only good edge-case tests will catch.** Don't read the code hunting for bugs first; let your tests find them.

## The loop (every test you add)
1. **Say** what behavior this test proves and why it matters for money. "If I split $10 three ways, the shares must add back up to exactly $10."
2. **Prompt** for the test with your case in it, using the playbook's **Small tests** prompt. One behavior per test, named for what it proves.
3. **Check** the test the AI wrote: does it assert the thing you said, or something weaker? Did it add cases you didn't ask for? Keep, cut or note them.
4. **Say** what the result told you: passed (behavior confirmed) or failed (found a bug: write the bug in one sentence).

## Steps
1. Run `pytest -q` (1 test passes). Read `allocate.py` just enough to know the inputs and outputs.
2. Use the **Edge cases** prompt to brainstorm. Add your own first: think about money that doesn't divide evenly, zero, negatives, empty input, huge numbers, bad types.
3. Write tests until you've found **every bug you can**. Don't fix code yet.
4. Then fix the bugs you found, one at a time, re-running after each.

## Done when
- At least 8 focused tests, each named for what it proves.
- `notes.md` lists each bug your tests found, in one sentence each, and which test caught it.

Then compare with `../_answers/drill-3.md`.
