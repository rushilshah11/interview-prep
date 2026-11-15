from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bucket:
    capacity: int
    refill_per_sec: float
    tokens: float
    updated: float


def refill(bucket: Bucket, now: float) -> None:
    elapsed = now - bucket.updated
    if elapsed <= 0:
        return

    
    bucket.tokens = min(bucket.capacity, bucket.tokens + float(elapsed) * bucket.refill_per_sec)
    bucket.updated = now
