# Drill 5: Review code the AI wrote

**Playbook phases:** 3/4 Check steps, 4 · Verify ("Review the diff"), Anytime · "AI makes a claim", "AI agrees too fast"
**Time box:** 20 minutes
**What's here:** a teammate asked an AI to add partial refunds. Read `AI_CHAT.md` for the exact prompt and the AI's (very confident) reply. The new code is `orders/refunds.py`; the old version is `orders/refunds_before.py`. **The tests pass.** Your job is to decide if this is safe to merge.

## The loop (every concern)
1. **Say** what you expected the change to be, given the prompt, before you read the diff. Then for each difference: "This line does ___. Was that asked for? Is it right?"
2. **Prompt** to check it: "Show me the exact line that supports that", "What calls `refund_order`, and does this change break any of them?", "Give me a counterexample where this is wrong."
3. **Check** the AI's answer against the code. Don't take "all tests pass" as proof of anything.
4. **Say** one sentence: keep it, fix it, or ask the interviewer. Anything the AI did that wasn't in the prompt is a decision you now own.

## Steps
1. Run `pytest -q` (all pass). Write in `notes.md`: what does the prompt ask for, exactly? List it in 2 bullets.
2. Compare `refunds_before.py` with `refunds.py` line by line. Mark each change: **asked for**, **not asked for**, or **wrong**.
3. Check every caller of `refund_order` (there's more than the tests).
4. For each problem, write a failing test that proves it, then fix it with the smallest change.

## Done when
- `notes.md` has a review comment for each problem, the way you'd write it on a PR: what's wrong, why it matters for a payments product, the fix.
- Each problem has a test that failed before your fix and passes after.

Then compare with `../_answers/drill-5.md`.
