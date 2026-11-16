# Breeze Drill A2: build a conversion quote API from an empty folder, AI after your blueprint

**Time box:** 30 minutes. **AI:** none for steps 1 and 2 (your questions and your blueprint). From step 3 on, AI is allowed. Before you switch, say out loud: "Is it OK if I use AI for this part?" Google is fine throughout (FastAPI docs, Python docs).
**Grading:** the Breeze prep guide: clarification and scope, interfaces and structure, correctness and edge cases, testing and debugging, communication.
**Follow:** the Breeze tab of the playbook, phases 1 to 6 and then 8.

## The brief

> Merchants on Breeze get paid in one currency and want to hold another, for example USD into USDC or EUR. Build a backend API that gives a merchant a price quote for a conversion, locks that price for a short time, and lets them accept it. Keep it in memory, no database.

That's all an interviewer might say. Everything else, you clarify.

## Steps

1. **Understand and clarify (5 min, no AI).** Restate the problem in two sentences. Write the questions you'd ask the interviewer in `notes.md`, then open `../_answers/drill-a2-interviewer.md`. Don't open it before you've written your questions.
2. **Blueprint and edge cases (5 min, no AI).** In `notes.md`, write the endpoints, request and response models, the service methods, the error types and their status codes, and your edge cases as test names. Think about where "now" comes from: how will your tests check a quote that has expired without waiting 30 seconds?
3. **Build in slices, AI on.** Do one endpoint at a time. Give the AI your blueprint as the constraint, review each diff against the checklist in `syntax warmup/fastapi/reading-backend-code.md`, and get tests for each endpoint before moving on. Use `TestClient(app)`.
4. **Wrap up (2 min).** Write 3 lines in `notes.md`: what you built, what you'd add next, and one tradeoff you made.

## Done when

- `pytest -q` passes, with at least one failure-case test per endpoint, and an expiry test that doesn't use `time.sleep`.
- No route contains business rules.
- `notes.md` has your questions, your blueprint and your wrap-up.

Then compare with `../_answers/drill-a2.md`.
