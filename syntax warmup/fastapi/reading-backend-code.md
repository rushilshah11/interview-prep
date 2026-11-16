# Reading backend code the AI writes (FastAPI)

You don't need to type this. You need to recognize each piece, say what it does, and catch what's wrong.

Setup, once, inside your `.venv`: `pip install fastapi uvicorn httpx pytest`

## The picture: a restaurant
- **Route** = the waiter. Takes the order (the request), passes it to the kitchen, brings back the plate (the response). The waiter doesn't cook.
- **Pydantic model** = the order form. If the customer leaves a required box empty or writes letters where a number goes, the form is rejected at the door (FastAPI's automatic 422) before the kitchen sees it.
- **Service / logic** = the kitchen. All the business rules live here: is the amount valid, is there enough money, is this a duplicate.
- **Exception handler** = the manager. When the kitchen says "we can't make that," the manager turns it into a consistent answer (JSON and a status code) instead of a crash.
- **Status code** = the one-word summary on the receipt: 201 made it, 400 your order was wrong, 404 we don't have that, 409 that conflicts with something.

If you see the waiter cooking (business rules inside the route), say so.

## What each line means

| You see | What it does |
|---|---|
| `app = FastAPI()` | Creates the app. Often wrapped in `def create_app():` so each test starts from a fresh, empty state. |
| `@app.post("/payments", status_code=201)` | "When a POST hits /payments, run this function, and answer 201 on success." |
| `@app.get("/payments/{payment_id}")` and `def get_payment(payment_id: str)` | The part in braces is a **path param**. It arrives as the function argument with the same name. |
| `class PaymentIn(BaseModel): merchant_id: str; amount: str` | A **Pydantic model**: the shape the JSON body must have. FastAPI checks it automatically. |
| `def create(body: PaymentIn)` | "The JSON body must match PaymentIn." A missing field or wrong type gets a **422** automatically, naming the field. |
| `idempotency_key: str \| None = Header(None)` | Reads a **header**. FastAPI turns `idempotency_key` into the `Idempotency-Key` header for you. Idempotency keys and auth tokens live here. |
| `limit: int = Query(10, ge=1, le=50)` | Reads a **query param** (`?limit=5`), converts it to an int, and rejects values outside 1–50 with a 422. |
| `status: str \| None = None` | An optional query param. If it's not in the URL, it's `None`. |
| `return payment.to_json()` | Returning a dict sends it as JSON, with the decorator's status code. |
| `return JSONResponse({...}, status_code=404)` | Sends a specific status code by hand. **Forget `status_code` and it's a 200.** |
| `raise HTTPException(status_code=404, detail="...")` | FastAPI's built-in way to stop and return an error. |
| `@app.exception_handler(ApiError)` | One place that turns any `ApiError` into JSON and a status code, so routes don't need try/except. |
| `client = TestClient(app)` then `client.post("/payments", json={...}, headers={...})` | Calls the API in a test without starting a server. `r.status_code` and `r.json()` are what you assert on. |

## Status codes you'll be asked to pick
- **200** OK. Also right for an idempotent replay ("you already made this; here it is again").
- **201** Created.
- **400** Bad input you check yourself (an amount with 3 decimal places, an unsupported currency).
- **422** FastAPI's automatic answer when the body or query params don't match their types. Also used for "valid shape, breaks a business rule" (below the minimum payout). Know that FastAPI produces it on its own.
- **404** Not found.
- **409** Conflict: a reused idempotency key with a different body, or an invalid state change (refunding a failed payment).
- **500** A bug. Never on purpose. If bad input can cause a 500, that's a finding.

## The review checklist: what to look for when the AI writes a route
1. **Can bad input reach a 500?** A dict lookup like `self.merchants[merchant_id]` on an unknown id raises KeyError, which becomes a 500. Ask: "What happens if this id doesn't exist?"
2. **Does an error return the wrong code?** `JSONResponse({"error": ...})` without `status_code` is a 200 with an error inside.
3. **Is money a float anywhere?** `amount: float` in a Pydantic model, `float(total)`, or a number in the response JSON all count. Money should be `str` in the model, `Decimal` inside, and a string going out.
4. **Is the waiter cooking?** If rules like balances or duplicates are in the route, ask the AI to move them into the service so they're testable without HTTP.
5. **Does a failed request change nothing?** Look for a change before the last check: saving, marking paid, or deducting before validating. All checks should come before any change.
6. **Is it consistent?** One error shape everywhere (`{"error": {"code", "message"}}`), one exception handler, not some routes building errors by hand and others raising.
7. **Do the tests hit the failure paths?** A happy-path test isn't enough. Ask the AI to list each test and the one behavior it proves, then check for a missing field, a bad amount, an unknown id and a conflict.

## Things to say while reviewing (out loud)
- "The route takes a PaymentIn body, reads the Idempotency-Key header, calls the service, and returns 201. The rules are in the service, so they're testable without HTTP."
- "Amount is a `str` in the model, not a float, so it never loses precision before we turn it into a Decimal."
- "If the merchant doesn't exist, this dict lookup throws a KeyError, and that's a 500. I want a 404."
- "This JSONResponse has no status_code, so the client sees a 200. Adding the status."
- "FastAPI already returns 422 if `amount` is missing. My own check covers the cases the type can't, like 3 decimal places."

## Prompts that get good route code
- "Add POST /payments in FastAPI. Use a Pydantic model with `amount` as a string, read the Idempotency-Key header, call `service.create`, and return 201. Keep the route thin: validation and rules go in the service. Add one exception handler that maps `ApiError` to JSON and its status."
- "List every way a request to this route could produce a 500, and fix each one so it returns a 4xx with a clear message."
- "Write tests with TestClient for this route: one happy path, plus a missing field, a bad amount, an unknown id, and a conflict. List each test and the behavior it proves."

## If the first part is no-AI
Breeze might start without AI, so it's worth being able to write one route by hand. This is enough, and it's fine to look up the rest:

```python
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class PaymentIn(BaseModel):
    merchant_id: str
    amount: str
    currency: str

@app.post("/payments", status_code=201)
def create_payment(body: PaymentIn, idempotency_key: str | None = Header(None)):
    return service.create(body.merchant_id, body.amount, body.currency, idempotency_key).to_json()
```
