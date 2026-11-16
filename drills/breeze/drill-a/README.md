# Breeze Drill A: build an API from an empty folder, AI after your blueprint

**Time box:** 30 minutes. **AI:** none for steps 1 and 2 (your questions and your blueprint). From step 3 on, AI is allowed. Before you switch, say out loud: "Is it OK if I use AI for this part?" Google is fine throughout (FastAPI docs, Python docs).
**Grading:** the Breeze prep guide: clarification and scope, interfaces and structure, correctness and edge cases, testing and debugging, communication.

## The brief

> Merchants use Breeze to charge their customers. Build a small backend API that lets a merchant create payments and look them up. Keep it in memory, no database.

That's all an interviewer might say. Everything else, you clarify.

## Steps

1. **Clarify (3 min).** Write the questions you'd ask the interviewer in `notes.md`. Then open `../_answers/drill-a-interviewer.md`, which has the answers an interviewer would give. Don't open it before you've written your questions.
2. **Blueprint out loud (3 min).** In `notes.md`, write the shape before any code: the files, the classes and functions with their signatures, the error types, and which status code each error maps to. The prep guide wants logic separate from I/O, so keep the rules in a plain Python module and make the FastAPI routes thin.
3. **Build in slices, AI on.** Do one endpoint at a time. Give the AI your blueprint as the constraint, review each diff against the checklist in `reading-backend-code.md`, and get a test for each endpoint before moving on. Use FastAPI's test client: `TestClient(app).post("/payments", json={...})`. It needs `httpx` installed.
4. **Edge cases.** Make every bad input return a clear error with a status code, never a 500.
5. **Wrap up (2 min).** Write 3 lines in `notes.md`: what you built, what you'd add next, and one tradeoff you made.

## Done when

- `pytest -q` passes, with at least one failure-case test per endpoint.
- No route contains business rules. Routes parse the input, call your logic, and return JSON.
- `notes.md` has your questions, your blueprint and your wrap-up.

Then compare with `../_answers/drill-a.md`.
