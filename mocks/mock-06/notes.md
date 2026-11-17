High level: So we're building a backend service that lets merchants create payments and look them up."

functionality: 
 - create_payment(merchant_id, amount, currency, idempotency_key)
        rules: amount is a positive decimal with at most 2 decimal places. Accept strings or Decimal. Reject floats, because float drift like 0.1 + 0.2 can’t touch money. currency must be one of USD, EUR, GBP. Merchants are registered first. Reject a merchant we don’t know. Idempotency: the same key with the same body returns the same payment, not a duplicate. The same key with a different body raises a conflict error.
 - register_merchant(merchant)
        in memory, no need for a api endpoint. 
 - get_payment by ID is fine to add. ID is payment id

 - Payment modeling should record that a merchant wants to charge a customer a certain amount in a certain currency. No money moves yet, we just set status to pending until further stuff happens in the card processor. 

 - External servers (merchants) call our API

Types
 - Amount is a string or Decimal, in dollar amount
- All four fields are required. If any is missing, reject it with a validation error. 
 - Types exceptions are fine for now. In the future, implement structured json. 

Error Handling: 
- 422 for Bad Requests
- 403 for a merchant who is forbidden to access a specific payment
- 404 for a unknown merchant
- 409 for idempotency.

Endpoints
- POST /merchants to create a merchant
- POST /payments to create a payment
- GET /payments/{payment_id} to get a singular payment

Pydantic Models
- PaymentIn has merchant_id, amount: str | int, currency, and idempotency_key
- PaymentOut adds id and status and created_at

Layers
- thin routes in app.py with a PaymentsService that handles business logic. Errors.py that has our exception handler and error details

Classes and Objects
- One dictionary for idempotency. This will track if a id maps to an existing body so we prevent duplicates. The lookup for the key should be scoped to the merchant_id and the idempotency key so it is unique to the body. 
- One dictionary mapping merchants to an id
- A payments class that handles the business logic that our routes will call. 

Tests and Edge Cases:
• test_create_payment_returns_201_pending
• test_missing_field_is_400, test_non_json_body_is_400
• test_amount_zero_negative_or_3_decimals_is_422, 
 test_unsupported_currency_is_422
• test_unknown_merchant_is_404, test_unknown_payment_is_404
 - test for same key with same body
 - test for same key with different body