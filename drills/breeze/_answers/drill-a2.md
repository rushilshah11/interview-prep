# Drill A2: what a strong answer looks like

## Questions worth asking
Ask about the supported pairs, where rates come from, how the fee works and how it's rounded, how long a quote is locked, who can accept it and how many times, and what's out of scope (balances, auth). Bonus: "Should the quote show the fee separately, so the merchant can see it?"

## A clean shape

```
quotes/
  service.py   # QuoteService(rates, clock): create_quote, get_quote, execute_quote
  errors.py    # ApiError(code, message, status) and its subclasses
  app.py       # create_app(service=None) -> FastAPI, thin routes, one exception handler
tests/
  test_service.py   # rules and expiry, no HTTP
  test_api.py       # one or two TestClient tests per route
```

- **Inject the clock.** `QuoteService(clock=lambda: datetime.now(timezone.utc))`. Tests pass a fake clock they can move forward, so the expiry test takes no time. This is the design point the drill is looking for. Say why: "Time is an input. If the service reads the real clock directly, I can't test expiry without sleeping."
- **Inject the rates too.** A dict passed into the service, so a live price feed can replace it later without changing any rules.
- **Money.** `amount` is a `str` in the Pydantic model, then a Decimal. `receive = (amount * rate * (1 - SPREAD)).quantize(Decimal("0.01"), ROUND_HALF_UP)`. The fee is the difference before and after the spread, also as a Decimal. Every amount goes out as a string.
- **Status.** `open` → `executed`. Expired is derived from the clock rather than stored, or stored when someone tries to execute; either works if you say which.

## Status codes (say your choice and why)
- Unknown pair or bad amount → 400. A missing field → FastAPI's automatic 422.
- Unknown quote → 404.
- A different merchant tries to execute → 403, or 404 to avoid revealing that the quote exists (a good tradeoff to say out loud).
- Already executed → 409.
- Expired → 410 Gone, or 409. Either works if you say why.

## Edge cases a reviewer looks for
- A same-currency pair (USD→USD) → 400.
- An amount of `"0"`, `"-5"` or `"1.234"`, or an amount sent as a float → 400.
- Lowercase currency codes: decide whether to normalize or reject, and say which.
- Executing exactly at `expires_at`: decide whether that's expired, and test the boundary.
- Executing twice → the second call gets 409 and nothing changes.
- Rounding: 100.00 USD→EUR at 0.92 with a 0.5% spread = 91.54.

## Tradeoffs worth saying out loud
- An in-memory dict now. In production: a database row per quote, and the execute step as one atomic update (`UPDATE ... WHERE status = 'open' AND expires_at > now()`) so two concurrent accepts can't both succeed.
- A fixed rate table now, a price feed later. The rate is locked into the quote when it's created, so a later rate change doesn't affect an open quote.
- Rounding happens once, at the end, so precision isn't lost in the middle of the calculation.
