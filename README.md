# Interview Prep

My technical interview practice: LeetCode / NeetCode 150 solutions, timed mock interviews, and Python syntax drills.

## Layout

| Folder | What's in it |
| --- | --- |
| `mocks/` | Timed mock interviews, each a small project with its own tests (wallets, payments, settlement) |
| `warmup/` | Warm-up builds before mocks |
| `syntax warmup/` | Python syntax drills and answers |
| `example agent/` | A minimal tool-using agent loop, for AI coding interviews |

## Running tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install pytest
cd mocks/mock-04 && pytest
```
