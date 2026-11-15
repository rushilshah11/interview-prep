# Drill 5 answer key

The prompt asked for exactly two things: an optional `amount`, and full refund when it's missing. Everything else is either unasked-for or wrong.

1. **Removed the "only paid orders" check (not asked for, dangerous).** `refunds_before.py` rejected refunds on pending orders; the new version refunds anything, including orders that were never paid. Test: a `pending` order raises `RefundError`.
2. **Uses `float` for money (wrong).** `float(amount)` brings binary rounding errors back (`0.1 + 0.2 != 0.3`) and mixes floats into a list of Decimals. Fix: `Decimal(str(amount))`, quantized to cents. Test: `refund_order("o1", "0.10")` returns `Decimal("0.10")`.
3. **Over-refund check ignores earlier refunds (wrong).** It compares against `order.total`, not what's left. Two refunds of 30 on a 50 order both succeed: 60 refunded. Fix: `remaining = order.total - sum(order.refunds)`. Test: refund 30 twice on a 50 order; the second raises.
4. **Renamed the parameter `order_id` → `id` (not asked for, breaks a caller).** `orders/api.py` calls `refund_order(order_id=...)`, which now raises `TypeError`. No test covers `api.py`, so "all tests pass" hid it. `id` also shadows a Python builtin. Test: `handle_refund_request({"order_id": "o1"})` works.
5. **Sets status to `"refunded"` on any partial refund (wrong).** After refunding 20 of 50, the order says refunded and the rest can't be tracked. Fix: only mark refunded when the remaining amount hits 0 (or use `partially_refunded`).
6. **Side effects nobody asked for:** a `print` (use logging, or remove it) and a customer email sent *inside* the refund function, before anything is persisted. If the email fails, the refund call blows up after the money logic ran. That's a design decision to raise, not one an AI should make silently.

**The meta-lesson:** "All existing tests pass ✅" proved nothing here, because the tests only cover the happy path and don't cover `api.py`. Your review is the real check.
