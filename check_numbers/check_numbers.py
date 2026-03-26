from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR

start = 1
end = 10000

factor = Decimal("1.19")
tolerance = Decimal("0.01")


def is_valid_sum(n: int) -> bool:
    """
    Checks if n can be represented as 11 plus a combination of 10, 20, 50, or 100.
    This is true if (n - 11) is a non-negative multiple of 10.
    """
    if n < 11:
        return False
    return (n - 11) % 10 == 0


def is_close_to_integer(value: Decimal, max_distance: Decimal) -> bool:
    lower = value.to_integral_value(rounding=ROUND_FLOOR)
    upper = value.to_integral_value(rounding=ROUND_CEILING)
    distance = min(value - lower, upper - value)
    return distance <= max_distance

matches = [
    n for n in range(start, end + 1)
    if is_close_to_integer(Decimal(n) * factor, tolerance) and is_valid_sum(n)
]

print(matches)