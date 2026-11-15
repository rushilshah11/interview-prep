# Drill 2 answer key

6 tests fail at the start, but there are only 3 bugs. The big lesson: **most of the failures share one root cause**, and some of them are failures in tests that look totally unrelated (`test_keys_are_independent`, `test_cost_greater_than_one`).

1. **`limiter.py` `__init__`: mutable default `buckets: dict = {}`.** Python creates that `{}` once, so every RateLimiter made without passing `buckets` shares the same dict. Tests that reuse key `"k1"` see tokens spent by *earlier tests*. That's why the failures look random and depend on test order. Fix: `buckets: dict | None = None`, then `self._buckets = buckets if buckets is not None else {}`. After this fix, 3 tests still fail.
2. **`bucket.py` `refill`: `int(elapsed)` drops fractional seconds.** After 0.5s, `int(0.5) == 0`, so nothing refills. Fix: `elapsed * bucket.refill_per_sec`. Fixes `test_refills_over_fractional_seconds` and `test_remaining_after_partial_refill`.
3. **`bucket.py` `refill`: no cap at capacity.** A bucket idle for 100s ends up with 104 tokens instead of 5. Fix: `bucket.tokens = min(bucket.capacity, bucket.tokens + elapsed * bucket.refill_per_sec)`. Fixes `test_refill_never_exceeds_capacity`.

What a strong run looks like: you notice that failing tests like `test_keys_are_independent` make no sense on their own, guess "state is leaking between tests," and find the shared default. Then you re-run and see 3 left.

Missing tests worth naming: `cost=0` or negative raises; clock going backwards (handled by `elapsed <= 0`, but untested); `remaining` on a brand-new key returns capacity. Also worth raising out loud: two requests at the same moment on the same key isn't handled (no locking).
