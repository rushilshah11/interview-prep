from decimal import Decimal

PLANS = {"basic": Decimal("9.99"), "pro": Decimal("29.00"), "team": Decimal("99.00")}


class UnknownPlan(Exception):
    pass


def price_of(plan: str) -> Decimal:
    try:
        return PLANS[plan]
    except KeyError:
        raise UnknownPlan(plan)
