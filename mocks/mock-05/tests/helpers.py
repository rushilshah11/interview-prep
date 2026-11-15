import itertools

_ids = itertools.count(1)


def rec(merchant="m_1", type="sale", amount="100.00", currency="USD", **over):
    r = {
        "id": f"t{next(_ids)}",
        "merchant_id": merchant,
        "type": type,
        "amount": amount,
        "currency": currency,
        "timestamp": "2026-11-14T12:00:00Z",
    }
    r.update(over)
    return r
