# Drill B: what the interviewer would answer

- **Route?** `GET /transactions`.
- **Filters?** `merchant_id` (required: the dashboard is always one merchant's view), `status` (one of pending, succeeded, failed, refunded), and `created_from` / `created_to` as ISO dates. `created_from` is inclusive and `created_to` is exclusive.
- **Order?** Newest first.
- **Pagination?** `limit` defaults to 10, with a max of 50. Your choice of offset or cursor, but be ready to explain why.
- **Response?** `{"data": [...], "next_cursor": "..." or null}`, or for offset paging, `{"data": [...], "total": N}`.
- **Bad params?** 400, naming the bad param. An unknown merchant returns an empty list (merchants live in another service).
- **Ties in created_at?** They can happen in production. Your ordering must be stable.
