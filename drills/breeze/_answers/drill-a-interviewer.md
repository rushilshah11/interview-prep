# Drill A: what the interviewer would answer

Open this only after you've written your questions. If you asked something not listed here, pick a reasonable answer, write it down as an assumption, and say it out loud.

- **Endpoints?** Create a merchant, create a payment, get one payment, and list a merchant's payments.
- **What's in a payment?** `merchant_id`, `amount`, `currency`, and an optional `description`. The server assigns `id`, `status` ("pending") and `created_at`.
- **Amount format?** A string or number in major units ("12.50"). It must be positive with at most 2 decimal places. Reject anything else. Don't use floats internally.
- **Currencies?** USD, EUR and GBP only.
- **Unknown merchant?** 404.
- **Error format?** Up to you, but make it consistent. Something like `{"error": {"code": "invalid_amount", "message": "..."}}`.
- **Listing?** `GET /merchants/<id>/payments`, newest first. An optional `?status=` filter would be nice to have.
- **Auth?** Out of scope for today.
- **Persistence?** In memory is fine. Mention what you'd use in production.
