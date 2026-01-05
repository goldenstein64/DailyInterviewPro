"""
Given an integer, reverse the digits. Do not convert the integer into a string
and reverse it.

Example:

>>> reverse_integer(135)
531
>>> reverse_integer(-321)
-123
"""


def reverse_integer(num: int) -> int:
    result: int = 0
    abs_num: int = abs(num)
    sign: int = num // abs_num
    while abs_num > 0:
        digit: int = abs_num % 10
        result = result * 10 + digit
        abs_num //= 10

    return sign * result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
