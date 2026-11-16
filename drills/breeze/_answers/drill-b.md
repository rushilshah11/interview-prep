# Drill B: what a strong answer looks like

## The orientation an interviewer wants to hear
"The `Store` holds transactions in a dict. `create_app` builds the FastAPI app around a store, seeded by default. Routes do their own validation inline, so there's no service layer yet. Money is a Decimal and goes out as a string."

A good catch to mention: `POST /transactions` doesn't validate `currency` and never rejects `"1.234"`. Note it as out of scope rather than fixing it.

## A clean shape
- `txns/query.py` (or a method on `Store`): `list_txns(store, merchant_id, status=None, created_from=None, created_to=None, limit=10, cursor=None) -> (items, next_cursor)`. Pure logic, testable without HTTP.
- The route declares the query params as typed function arguments, and FastAPI parses and validates them: `limit: int = Query(10, ge=1, le=50)`, `status: Literal["pending", "succeeded", "failed", "refunded"] | None = None`, `created_from: datetime | None = None`. It calls the function and returns JSON.
- Sort by `(created_at, id)`, descending. Including the `id` breaks ties, so the order stays stable.

## Offset vs cursor (the tradeoff they want to hear)
- **Offset:** simple, but if a new transaction arrives between page 1 and page 2, rows shift, so you see duplicates or skip some. It's also slow on big tables, because `OFFSET 100000` scans everything before it.
- **Cursor:** encode the last row's `(created_at, id)` and return rows "before" it. It stays stable while new rows arrive, and at scale it becomes an indexed range query. A cursor is opaque to the client, so you can base64 it.
- For a live payments table, choose cursor and say why.

## Edge cases
- `limit=0`, `limit=-1`, `limit=abc`, `limit=500` → FastAPI returns 422 automatically with `Query(ge=1, le=50)`. Know that it does this, and say whether 422 or a custom 400 is the contract.
- `status=done` → 422 via `Literal`, or a 400 you raise yourself.
- `created_from=not-a-date` → 422 when it's typed as `datetime`. `created_from` later than `created_to` → 400 or an empty list (say which).
- A missing `merchant_id` → 400.
- The last page returns `next_cursor: null`.

## Tests that prove the tricky parts
- Paging all the way through returns every one of a merchant's transactions exactly once, with no gaps or duplicates.
- Ties: two transactions with the same `created_at` both appear, in a stable order.
- Date boundaries: `created_from` is inclusive and `created_to` is exclusive.
- Filters combine (merchant plus status).

## At 10 million rows
Use a database index on `(merchant_id, created_at DESC, id DESC)`, keep cursor pagination, and never compute `total` on every request (it's expensive). Mention caching only if there's time left.
