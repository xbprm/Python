from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

start = 1
end = 1000

factor = Decimal("1.19")
tolerance = Decimal("0.0")


def is_close_to_integer(value: Decimal, max_distance: Decimal) -> bool:
    lower = value.to_integral_value(rounding=ROUND_FLOOR)
    upper = value.to_integral_value(rounding=ROUND_CEILING)
    distance = min(value - lower, upper - value)
    return distance <= max_distance

matches = [
    n for n in range(start, end + 1)
    if is_close_to_integer(Decimal(n) * factor, tolerance)
]

print(matches)