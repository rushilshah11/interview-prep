# Drill 1 answer key

1. A subscription billing system: customers start a 14-day trial on a plan (basic/pro/team), and each renewal creates an invoice with 8.875% tax and tries to charge the customer through an injected `charge` function. `Subscriptions` owns the state; `Invoices` stores the bills.
2. States: trial → active on a successful renewal charge; trial/active → past_due on a failed charge; past_due → canceled after 3 failed charges in a row (`MAX_FAILED`); any state → canceled via `cancel()`. Canceled is terminal: `renew` and `change_plan` raise.
3. `renew(sub_id, today)`: returns None if `today < period_end`. Otherwise creates an invoice for the next 30-day period. Success: invoice marked paid, state ACTIVE, `period_end` +30 days, `failed` reset to 0. Failure: `failed += 1`, state PAST_DUE (or CANCELED at 3), `period_end` unchanged.
4. Plan names are validated by `price_of` (raises `UnknownPlan`) in `start`, `change_plan` and `invoices.create`. Unknown subscription ids raise `SubscriptionError` in `get`. There is no validation of customer ids or dates.
5. Good things to flag:
   - Every failed retry creates a **new open invoice** for the same period, so a customer with 3 failures has 3 open invoices. Probably a bug: should retry the same invoice.
   - `change_plan` switches the plan immediately with **no proration**; the next invoice charges the full new price.
   - `charge` is injected and returns a bool, so there's no error detail and no idempotency if the charge call times out.
   - Tax is rounded per invoice (fine), and money is Decimal (good).
   - `cancel` on an already-canceled subscription silently succeeds.
