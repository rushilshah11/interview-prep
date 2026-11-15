# Playbook drills

One drill per part of your AI Coding Interview Playbook. Each is a small, standalone project with no docstrings, a README with the steps, and an answer key in `_answers/` (only open it after you finish).

| Drill | Playbook phase | Time | What you practice |
|---|---|---|---|
| `drill-1-understand` | 1 · Understand | 15 min | Orient, map the lifecycle, trace a flow, check the AI's summary against the code |
| `drill-2-debug` | Anytime · A test fails, 4 · Sort the failures | 20 min | Read the failing line, guess first, prompt with your guess, find shared root causes |
| `drill-3-write-tests` | 2 · Edge cases, 4 · Small tests | 20 min | Brainstorm edge cases, write focused tests that expose hidden bugs |
| `drill-4-add-feature` | 2 · Blast radius & scope, 3 · Build, 6 · Harden | 25 min | Add a feature in layers, read each diff, catch changes you didn't ask for |
| `drill-5-review-ai-code` | Check steps, Stuck / AI seems off | 20 min | Review an AI's change, push back on its claims, find unasked-for changes |

## Every drill uses the same loop

1. **Say:** write one line in `notes.md` (your guess or plan) before every prompt, and say it quietly out loud.
2. **Prompt:** `[what I see or think] + [the ask] + [the constraint]`.
3. **Check:** open the line the AI changed or pointed to. Does it do what you expected? Did it do anything you didn't ask for?
4. **Say:** one sentence on what you confirmed, what was new, and what you'll do about it.

## Setup

From `interview prep/`: `source .venv/bin/activate`, then `cd drills/drill-1-understand && pytest -q`.

## To redo a drill

Make a copy before you start (`cp -r drill-2-debug drill-2-debug-try2`) so you can rerun the original later. Or ask your AI tool to plant new bugs in a fresh copy: "Plant 2 subtle bugs that make existing tests fail. Don't tell me what or where, and don't change the tests."
