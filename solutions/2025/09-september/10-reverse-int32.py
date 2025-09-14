"""
Write a function that reverses the digits a 32-bit signed integer, x. Assume
that the environment can only store integers within the 32-bit signed integer
range, [-2^31, 2^31 - 1]. The function returns 0 when the reversed integer
overflows.

Examples:

>>> reverse_int32(123)
321

>>> reverse_int32(2**31)
0
"""

import unittest

_MIN = -(2**31)
_MAX = 2**31 - 1


def reverse_int32(x: int) -> int:
    sign: int = -1 if x < 0 else 1
    abs_x: int = abs(x)
    result: int = 0
    while abs_x > 0:
        result *= 10
        result += abs_x % 10
        abs_x //= 10

    result *= sign
    return result if _MIN <= result <= _MAX else 0


def reverse_int32_divmod(x: int) -> int:
    sign: int = -1 if x < 0 else 1
    abs_x: int = abs(x)
    result: int = 0
    while abs_x > 0:
        abs_x, mod = divmod(abs_x, 10)
        result = result * 10 + mod

    result *= sign
    return result if _MIN <= result <= _MAX else 0


class Tests(unittest.TestCase):
    cases: list[tuple[int, int]] = [
        (0, 0),
        (1, 1),
        (15, 51),
        (-13, -31),
        (123, 321),
        (2**31, 0),
        (2**31 - 1, 0),  # > 2**31 - 1 when reversed
    ]

    def test_cases(self):
        for x, expected in self.cases:
            with self.subTest(x=x, expected=expected):
                self.assertEqual(expected, reverse_int32(x))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
