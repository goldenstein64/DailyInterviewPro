"""
Given an integer, reverse the digits. Do not convert the integer into a string
and reverse it.

Examples:

>>> reversed(135)
531

>>> reversed(-321)
-123
"""


def reversed(value: int) -> int:
    abs_value: int = abs(value)
    sign: int = -1 if value < 0 else 1
    result: int = 0
    while abs_value > 0:
        result *= 10
        result += abs_value % 10
        abs_value //= 10

    return sign * result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
