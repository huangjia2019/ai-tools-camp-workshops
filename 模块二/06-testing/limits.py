from decimal import Decimal, ROUND_HALF_UP


def limits(price, rate, tick):
    price, rate, tick = map(lambda x: Decimal(str(x)), (price, rate, tick))
    if not all(x.is_finite() for x in (price, rate, tick)):
        raise ValueError('inputs must be finite')
    if price <= 0 or tick <= 0 or not 0 <= rate < 1:
        raise ValueError('invalid inputs')
    up = (price * (1 + rate) / tick).to_integral_value(ROUND_HALF_UP) * tick
    down = (price * (1 - rate) / tick).to_integral_value(ROUND_HALF_UP) * tick
    return up, down
