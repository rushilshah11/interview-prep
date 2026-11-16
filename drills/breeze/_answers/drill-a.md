# Drill A: what a strong answer looks like

## Questions worth asking
Ask about the amount format and precision, the allowed currencies, what happens with an unknown merchant, the error format, and what's in scope (listing, filters, auth, persistence). Bonus: "What does a payment's status mean before it's processed?"

## A clean shape

```
payments/
  service.py   # PaymentService: create_merchant, create_payment, get_payment, list_payments
  errors.py    # ApiError(code, message, status) and its subclasses
  app.py       # create_app(service) -> FastAPI app, thin routes, one exception handler
tests/
  test_service.py   # rules, no HTTP
  test_api.py       # one or two tests per route through the test client
```

- **Money.** Parse with `Decimal(str(value))`. Reject a bool or NaN, anything not positive, and more than 2 decimal places (check the exponent with `d.as_tuple().exponent < -2`). Serialize as a string, `"12.50"`, so JSON never turns it into a float.
- **Errors.** One base class that carries `status` and `code`, plus a single `@app.exception_handler(ApiError)` that returns `JSONResponse(..., status_code=e.status)`. Routes never catch errors one at a time.
- **Request models.** A Pydantic `PaymentIn` with `amount: str`, never `amount: float`, so the money never passes through a float. FastAPI returns 422 when the body doesn't match the model, which is fine; say that you know it happens.
- **App factory.** `create_app(service=None)` lets each test start from a fresh state.
- **IDs.** Use `uuid4` or a counter. Don't let the client choose them.

## Edge cases a reviewer looks for
- A missing body, or a body that isn't JSON → FastAPI's automatic 422 (or 400 if you handle it yourself; say which).
- A missing field, or a field of the wrong type → 422 from the Pydantic model, naming the field.
- An amount of `"0"`, `"-1"`, `"1.234"`, `"abc"`, `true` or `null` → 400.
- An unknown currency → 400. A lowercase `"usd"` → decide whether to normalize or reject, and say which.
- An unknown merchant on create or list → 404. An unknown payment → 404.

## Tradeoffs worth saying out loud
- An in-memory dict now, Postgres in production, with a unique constraint on the id.
- Amounts as strings in JSON, to avoid float drift.
- Validation in the service, not the route, so a future CLI or queue consumer gets the same rules.
