# Breeze drills (Mon Nov 16, before tonight's mock)

The Breeze round is backend and full stack, Python is fine, and AI is allowed only when the interviewer says so. These drills practice that setup. Grading follows Breeze's prep guide: clarification and scope, interfaces and structure, correctness and edge cases, testing and debugging, communication. AI collaboration is graded too, whenever it's on.

| Order | Drill | Time | AI | Practices |
|---|---|---|---|---|
| 1 | `drill-a` Build a payments API from an empty folder | 30 min | After your questions and blueprint | Clarifying, a blueprint, reviewing AI-written FastAPI routes, error codes |
| 1b | `drill-a2` Build a conversion quote API (prices locked for 30s) from an empty folder | 30 min | After your questions and blueprint | Same as A in a new domain, plus injecting the clock so expiry is testable |
| 2 | `drill-c` Debug a payouts API | 20 min | None | Root cause first, all-or-nothing, status codes (also preps Rokt's no-AI round) |
| 3 | `drill-b` Add a list endpoint with filters and pagination | 30 min | After 10 min | Asking to switch AI on, cursor vs offset tradeoff, query param validation |

Take a 10-minute break between drills. Everything here is FastAPI. `../../syntax warmup/fastapi/reading-backend-code.md` explains what each piece of route code does and what to check when the AI writes it.

Setup, once, inside your `.venv`: `pip install fastapi uvicorn httpx pytest`

Run each drill in its own folder with `pytest -q`. When you finish one, tell me "done drill X" and I'll grade it from `notes.md` and the git diff.
