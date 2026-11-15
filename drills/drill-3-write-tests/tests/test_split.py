from decimal import Decimal

from split.allocate import allocate


def test_two_equal_weights():
    assert allocate(100, [1, 1]) == [Decimal("50.00"), Decimal("50.00")]
