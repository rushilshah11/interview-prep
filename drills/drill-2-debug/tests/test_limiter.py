import pytest

from ratelimit.limiter import RateLimiter


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


@pytest.fixture
def clock():
    return FakeClock()


def drain(rl, key, n):
    for _ in range(n):
        assert rl.allow(key)


def test_allows_up_to_capacity(clock):
    rl = RateLimiter(3, 1, clock)
    drain(rl, "k1", 3)
    assert not rl.allow("k1")


def test_keys_are_independent(clock):
    rl = RateLimiter(2, 1, clock)
    drain(rl, "k1", 2)
    assert rl.allow("k2")


def test_cost_greater_than_one(clock):
    rl = RateLimiter(5, 1, clock)
    assert rl.allow("k1", cost=4)
    assert not rl.allow("k1", cost=2)


def test_refills_over_fractional_seconds(clock):
    rl = RateLimiter(2, 2, clock)
    drain(rl, "k1", 2)
    clock.advance(0.5)
    assert rl.allow("k1")


def test_remaining_after_partial_refill(clock):
    rl = RateLimiter(10, 4, clock)
    drain(rl, "k1", 10)
    clock.advance(1.5)
    assert rl.remaining("k1") == 6


def test_refill_never_exceeds_capacity(clock):
    rl = RateLimiter(5, 1, clock)
    assert rl.allow("k1")
    clock.advance(100)
    drain(rl, "k1", 5)
    assert not rl.allow("k1")


def test_separate_limiters_do_not_share_state(clock):
    a = RateLimiter(1, 1, clock)
    b = RateLimiter(1, 1, clock)
    assert a.allow("shared-key")
    assert b.allow("shared-key")
