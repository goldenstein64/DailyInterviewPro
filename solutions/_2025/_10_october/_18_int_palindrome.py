"""
Given an integer, check if that integer is a palindrome. For this problem do not
convert the integer to a string to check if it is a palindrome.

Example:

>>> is_palindrome(1234321)
True

>>> is_palindrome(1234322)
False
"""

import unittest
from collections.abc import Callable
from itertools import product
from math import floor, log10


def is_palindrome(n: int) -> bool:
    """
    Determine whether an integer is a palindrome. Negative numbers are never
    palindromes because they have an asymmetric negative sign.

    This uses O(log10 n) time and O(log2 n) space.
    """
    if n < 0:
        return False
    elif n == 0:
        return True

    length: int = floor(log10(n)) + 1
    for i in range(length // 2):
        former: int = n // 10 ** (length - i - 1) % 10
        latter: int = n // 10**i % 10
        if former != latter:
            return False

    return True


def is_palindrome_truncate(n: int) -> bool:
    """
    Determine whether an integer is a palindrome. Negative numbers are never
    palindromes because they have an asymmetric negative sign.

    This uses O(log10 n) time and O(log2 n) space.
    """
    if n < 0:
        return False
    elif n == 0:
        return True

    length: int = floor(log10(n)) + 1
    while length > 1:
        power: int = 10 ** (length - 1)
        first: int = n // power
        last: int = n % 10
        if first != last:
            return False

        n -= first * power  # remove the first digit
        n //= 10  # remove the last digit
        length -= 2

    return True


class Tests(unittest.TestCase):
    solutions: list[Callable[[int], bool]] = [
        is_palindrome,
        is_palindrome_truncate,
    ]

    cases: list[tuple[int, bool]] = [
        (0, True),
        (1, True),
        (-101, False),
        (11, True),
        (767, True),
        (766, False),
        (1234321, True),
        (1234322, False),
    ]

    def test_cases(self):
        for solution, (n, expected) in product(self.solutions, self.cases):
            sol: str = solution.__name__
            with self.subTest(solution=sol, n=n, expected=expected):
                self.assertEqual(expected, solution(n))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
