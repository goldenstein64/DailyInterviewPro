"""
Given two strings A and B of lowercase letters, return true if and only if we
can swap two letters in A so that the result equals B.

Examples:

>>> buddy_strings("ab", "ba")
True

>>> buddy_strings("ab", "ab")
False

>>> buddy_strings("aa", "aa")
True

>>> buddy_strings("aaaaaaabc", "aaaaaaacb")
True

>>> buddy_strings("", "aa")
False
"""

from itertools import islice
from collections.abc import Iterable
import unittest


def has_duplicates(string: str) -> bool:
    seen: set[str] = set()
    for char in string:
        if char in seen:
            return True
        else:
            seen.add(char)

    return False


def buddy_strings(a: str, b: str) -> bool:
    """
    Check if two strings can be equal after one string swaps a character pair.

    This was inspired by the Levenshtein distance implementation
    in 2025/july/21. I just considered the case where only swaps could be made
    and simplified the matrix to a 1D array.

    In the worst case, this has O(n) time complexity and O(n) space.
    """
    n: int = len(a)
    if n != len(b):
        return False

    indexes: Iterable[int] = range(n)
    filtered: Iterable[int] = filter(lambda i: a[i] != b[i], indexes)
    first3: Iterable[int] = islice(filtered, 3)
    swap_indexes: list[int] = list(first3)

    match swap_indexes:
        case []:  # a and b are identical
            return has_duplicates(a)
        case [i, j]:
            return a[i] == b[j] and a[j] == b[i]
        case _:
            return False


class Tests(unittest.TestCase):
    cases: list[tuple[str, str, bool]] = [
        ("", "", False),
        ("ab", "ba", True),
        ("ab", "ab", False),
        ("ab", "bc", False),
        ("aa", "aa", True),
        ("ab", "cd", False),
        ("abaca", "acaba", True),
        ("aaaaaaabc", "aaaaaaacb", True),
        ("", "aa", False),
    ]

    def test_cases(self):
        for a, b, expected in self.cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertIs(expected, buddy_strings(a, b))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
