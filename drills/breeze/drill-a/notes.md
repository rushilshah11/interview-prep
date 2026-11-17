SAY: So we're building a backend service so that lets a merchant create payments and then look them up. Can you elaborate? What is it mean to create a payment? 

Notes: create a payments api where when a payment is created, it is in pending state. What happens after is out of scope. 

SAY: Who is considered the caller of our API? Is it the frontend or another service? Is it external or internal service? 

Notes: External. Merchants call from their backend services. Auth is out of scope. 

SAY: Since the call is external, that means the response shape we specify is a contract that other companies code depends on. Which means it needs to be stable. 
Error messages need to be clear and. And since requests coem over the internet, requests get retired which means we need to consider idempotency. We dont want to duplicate a payment. 
Is what i just mentioned in scope for todays interview? 

Notes: only response shape and errors

SAY: I'd like to dig deeper on Payment. What format is the amount, a string or a number? How many decimal places and which currencies are valid? 

Notes: They'd handle it either way, as a string or a number. Has to be positive, major units so dollars. At most 2 decimal places. USD, EUR, GBP. We can handle this by accepting amount as a string in the model. 

SAY: Which fields are required and what happens if one is missing?

Notes: merchant_id, amount, currency. optional description. throw error for required fields. Status code of 400 Bad Request or 422? My guess or preference is all 400 or 400 if inputs are missing and 422 for exceptions thrown inside the funciton with our business logic. 

SAY: When we throw these errors, is there a specific format you'd like? Do you want structure json or should we just raise an exception? My suggestion is structured json since external services are utilizing this. They can unpack it and use it in their own logic instead of directly crashing either service. 

Notes: Structured json with one exception handler than turns it into json. 

SAY: And who is allowed to access our API endpoints? Do we have a preset of callers/merchants? Or is it something anyone can call? Do we need to create a merchant first?

Notes: Only registered merchants can create payments. Add a simple way to create a merchant, just a name is fine, and the server gives it an id. If someone creates payment for unknown merchant, throw 404. 

SAY: Lastly, can you provide soem context on look up a payment? Is it get one by id, list a merchants payments. How should it be returned? Should it be filtered, ordered by amount? Date?

Notes: merchant should be able to get a single payment by id, and list all their payments, newest first. filter not needed, neither is paginartion. 

SAY: Ok, before moving to designing the API: just to confirm. In scope is create a merchant, create a payment: merchant_id, amount, currency, and optional description, get payment by id, list a merchants payments, newest first. Amounts can be string or number, positive, with at most 2 decimals in USD, EUR, GBP. Errors come back as structured json with a code and message. Unkwone merchants and payments return 404 with missing required fields as 400 and business logic errors 422. is there anything I am missing?

BLUEPRINT NOTES: 
Endpoints - 
1. GET /payments/{id}
2. GET /merchants/{merchant_id}/payments
3. POST /merchants
4. POST /payments

Models
1. Payments Model with amount as a string so it never becomes float. The response would be merchant_id, amount, currency, description
amount: str | float | int and then we convert to Decimal(str(value)) in the service. 
2. Payments Response Model with the same fields as above with status, created_at, and id. 
2. Merchants Model with merchant name and id as the response. 

Layers
1. Thin routes in app.py
2. Rules and business logic inside PaymentService
3. Error handling with one exception handler inside errors.py.

Errors and Codes
1. 400 bad request on function shape incorrect
2. 422 bad requst on if fields do not stick to business logic checks we decided
3. 404 for unknown payment
4. 404 for unknown merchants

SAY: Would you be able to provide feedback on this? Is there anyting I am missing? Do you prefer nested or ? inside the api call endpoint? I would probably ask AI what is best for our use case. Do you prefer to keep amount simple and just use Decimal? My assumption was to keep it flexible and handle the casting in our service. 

SAY: I'd like to cover edge cases. I feel like we covered most of them now. The only thing i could think of that we didnt was what if the request body isnt json? I would probably raise an axception of 400 as invalid format. Aside from that, is there anything you've seen go wrong in rpoduction that I should account for? 

test_create_payment_returns_201_pending
test_missing_field_is_400
test_non_json_body_is_400
test_amount_zero_negative_or_3_decimals_is_422
test_amount_as_number_is_accepted (Max said string or number)
test_unsupported_currency_is_422 (plus your lowercase decision)
test_unknown_merchant_is_404
test_unknown_payment_is_404
test_list_is_newest_first_and_only_that_merchant

Notes: lowercase everything and strip whitespaces for currency and any fields that have words. 

SAY: Can I use AI to generate code for this? 