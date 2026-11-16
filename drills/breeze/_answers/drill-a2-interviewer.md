# Drill A2: what the interviewer would answer

Open this only after you've written your questions. If you asked something not listed here, pick a reasonable answer, write it down as an assumption, and say it out loud.

- **Endpoints?** Create a quote, get a quote, and accept (execute) a quote. Optional: list the supported currency pairs.
- **Currency pairs?** USD→USDC, USD→EUR and EUR→USD. Anything else is rejected.
- **Where do rates come from?** A hardcoded rate table is fine: USD→USDC 1.0000, USD→EUR 0.9200, EUR→USD 1.0850. In production it would be a live price feed.
- **Fees?** Breeze takes a 0.5% spread: the merchant gets `amount × rate × (1 − 0.005)`. Round the result to 2 decimal places, half up.
- **Request?** `merchant_id`, `from_currency`, `to_currency`, and `amount` (the amount in from_currency, a positive decimal with at most 2 places).
- **Response?** id, merchant_id, the pair, amount, rate, fee, the amount the merchant receives, status, `expires_at`.
- **How long is a quote locked?** 30 seconds.
- **Accepting?** Only the merchant who created the quote can accept it, only once, and only before it expires. Accepting moves the status from `open` to `executed`.
- **Errors?** Up to you, but make them consistent and say which codes you picked for an expired quote and an already-executed quote.
- **Balances?** Out of scope. Assume the merchant has the funds.
- **Auth?** Out of scope. Pass `merchant_id` in the body.
