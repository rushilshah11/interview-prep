# Drill 1: Understand an unfamiliar codebase

**Playbook phase:** 1 · Understand (and the Check step)
**Time box:** 15 minutes
**What's here:** a small subscription billing system with no docstrings. The tests pass. Nothing is broken; your only job is to understand it.

## The loop (every move)
1. **Say** your read or guess in one line in `notes.md` (and quietly out loud).
2. **Prompt** with that guess in it, plus a constraint.
3. **Check** the AI's answer against the actual code. Open the line.
4. **Say** one sentence about what you confirmed or what was new. If the AI mentions something you didn't ask about, write it down and decide if it matters.

## Steps
1. Run `pytest -q`. Write one line: what do the test names tell you about what this code does?
2. Skim the four files yourself for 3 minutes. Write your guess: "I think this is ___ and the main object is ___."
3. Use the playbook's **Orient** prompt, with your guess in it.
4. Use **Map the lifecycle** on `subscriptions.py`: how does a Subscription move between states?
5. Use **Trace a flow** on `renew()`: what happens on a successful charge, and on a failed one?
6. **Check:** pick one thing the AI told you and verify it by reading the code. Was it right?

## Done when you can answer these in `notes.md`, in your own words
1. What does this codebase do? (2 sentences, headline first)
2. What states can a subscription be in, and what moves it between them?
3. Step by step, what does `renew()` change on a successful charge? On a failed one?
4. Where does validation happen, and what happens on bad input?
5. Name two things you'd ask the interviewer about or flag as risky.

Then compare with `../_answers/drill-1.md`.
