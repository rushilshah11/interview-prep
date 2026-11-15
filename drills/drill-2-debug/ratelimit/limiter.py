from __future__ import annotations

import math
from typing import Callable

from ratelimit.bucket import Bucket, refill


class RateLimiter:
    def __init__(self, capacity: int, refill_per_sec: float, clock: Callable[[], float], buckets: dict | None = None):
        if capacity <= 0 or refill_per_sec <= 0:
            raise ValueError("capacity and refill rate must be positive")
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self.clock = clock
        self._buckets = buckets if buckets is not None else {}

    def _bucket(self, key: str) -> Bucket:
        now = self.clock()
        b = self._buckets.get(key)
        if b is None:
            b = Bucket(self.capacity, self.refill_per_sec, float(self.capacity), now)
            self._buckets[key] = b
        refill(b, now)
        return b

    def allow(self, key: str, cost: int = 1) -> bool:
        """Reject cost <= 0, fetch this key's bucket refilled to now, then spend `cost` tokens and return True if enough remain, else spend nothing and return False."""
        if cost <= 0:
            raise ValueError("cost must be positive")
        b = self._bucket(key)
        if b.tokens >= cost:
            b.tokens -= cost
            return True
        return False

    def remaining(self, key: str) -> int:
        return math.floor(self._bucket(key).tokens)
