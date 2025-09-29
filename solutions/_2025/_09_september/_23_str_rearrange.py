"""
Given a string, rearrange the string so that no character next to each other are
the same. If no such arrangement is possible, then return None.

Example:

>>> s = rearrange_string("abbccc")  # e.g. 'cbcbca' or 'cbcabc'
>>> no_runs(s)
True
"""

from itertools import pairwise, repeat
from collections import Counter
import unittest


def no_runs(s: str | None) -> bool:
    return s is not None and all(a != b for a, b in pairwise(s))


def rearrange_string(s: str) -> str | None:
    """
    This simply keeps a counter of every character in the string and alternates
    between characters. It can't handle every case, e.g. 'aaabc' becomes
    'abcaa'.

    This has about O(n) time complexity and O(n) space.
    """
    counter: Counter[str] = Counter(s)
    most_common: list[tuple[str, int]] = counter.most_common()
    most_common.reverse()
    result: list[str] = []
    while most_common:
        for i in reversed(range(len(most_common))):
            k, count = most_common[i]
            result.append(k)
            if count <= 1:
                del most_common[i]
            else:
                most_common[i] = (k, count - 1)

    new_s: str = "".join(result)
    return new_s if no_runs(new_s) else None


def rearrange_string_greedy(s: str) -> str | None:
    """
    An implementation I adapted from G2G. Get letter frequencies, sort them by
    most common, get a list of all letters sorted by commonality, and alternate
    between the first and second half of the list.

    This has O(n) time complexity and O(n) space.

    See: https://www.geeksforgeeks.org/dsa/rearrange-characters-string-no-two-adjacent
    """

    if not s:
        return ""

    n: int = len(s)
    most_common: list[tuple[str, int]] = Counter(s).most_common()

    if most_common[0][1] > (n + 1) // 2:
        return None

    result: list[str] = list(s)
    elements = [l for c, count in most_common for l in repeat(c, count)]
    mid = n // 2 + n % 2
    result[::2] = elements[:mid]
    result[1::2] = elements[mid:]
    return "".join(result)


class Tests(unittest.TestCase):
    cases: list[tuple[str, bool]] = [
        ("", True),
        ("a", True),
        ("abb", True),  # bab
        ("aa", False),
        ("abbccc", True),  # cbacbc
        ("aaabc", True),  # abaca
    ]

    def test_cases(self):
        for s, expected in self.cases:
            with self.subTest(s=s, expected=expected):
                new_s: str | None = rearrange_string_greedy(s)
                self.assertEqual(expected, no_runs(new_s))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
