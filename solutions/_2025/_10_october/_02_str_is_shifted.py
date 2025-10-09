"""
You are given two strings, A and B. Return whether A can be shifted some number
of times to get B.

See: https://www.geeksforgeeks.org/dsa/a-program-to-check-if-strings-are-rotations-of-each-other


Example:

>>> is_shifted("abcde", "cdeab")
True

>>> is_shifted("ababa", "abaab")
True
"""

import unittest
from collections import Counter
from collections.abc import Callable, Generator
from itertools import product


def find_all(
    s: str, sub: str, start: int | None = None, end: int | None = None
) -> Generator[int]:
    """Generate all indexes where `sub` was found in `s`."""
    i: int = -1 if start is None else start - 1
    while (i := s.find(sub, i + 1, end)) != -1:
        yield i


def is_shifted(a: str, b: str) -> bool:
    """
    Determine whether `a` can be shifted to produce `b`.

    This uses an algorithm that finds the least common letter in `a`, generates
    a shifted version of `a` that starts with that letter, and compares it to
    all possible shifted versions of `b`. If one comparison succeeds, `a` can be
    shifted to match `b`.

    This uses O(nk) time and O(n) space, where `n = len(a)` and
    `k = b.count(least_common_letter)`.
    """
    if len(a) != len(b):
        return False
    elif a == b:
        return True

    # get the least common letter in `a`
    a_counts: Counter[str] = Counter(a)
    ltr: str = min(a_counts.items(), key=lambda t: t[1])[0]

    # shift `a` so it starts with the least common letter
    a_shift: str = a
    if a[0] != ltr:
        a_index: int = a.find(ltr)
        assert a_index != -1
        a_shift: str = a[a_index:] + a[:a_index]

    # look for any shifted version of `b` that matches `a`
    return any(a_shift == b[i:] + b[:i] for i in find_all(b, ltr))


def is_shifted_find(a: str, b: str) -> bool:
    """"""
    if len(a) != len(b):
        return False
    elif a == b:
        return True

    return (a * 2).find(b) != -1


def build_kmp_table(sub: str) -> list[int]:
    """
    Build a partial match table for use in the Knuth-Morris-Pratt algorithm.

    See: https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm
    """
    result: list[int] = [0] * (len(sub) + 1)
    pos: int = 1
    cnd: int = 0

    result[0] = -1

    for pos in range(1, len(sub)):
        result[pos] = result[cnd] if sub[pos] == sub[cnd] else cnd
        while cnd >= 0 and sub[pos] != sub[cnd]:
            cnd = result[cnd]
        cnd += 1

    result[-1] = cnd

    return result


def kmp_search(s: str, sub: str, kmp_table: list[int] | None = None) -> Generator[int]:
    """
    Perform a substring search using the Knuth-Morris-Pratt algorithm. This is
    functionally identical to `s.find(sub)`.

    See: https://en.wikipedia.org/wiki/Knuth–Morris–Pratt_algorithm
    """
    if kmp_table is None:
        kmp_table = build_kmp_table(sub)

    j: int = 0
    k: int = 0
    len_sub: int = len(sub)

    while j < len(s):
        if sub[k] == s[j]:
            j += 1
            k += 1
            if k == len_sub:  # occurrence found
                yield j - k
                k = kmp_table[k]  # kmp_table[len_sub] can't be -1
        else:
            k = kmp_table[k]
            if k == -1:
                j += 1
                k += 1


def is_shifted_kmp(a: str, b: str) -> bool:
    """
    Determine whether `a` can be shifted to produce `b`. This performs a
    substring search using the KMP algorithm.

    This uses O(n) time and O(n) space.
    """
    if len(a) != len(b):
        return False
    elif a == b:
        return True

    return next(kmp_search(a * 2, b), None) is not None


class Tests(unittest.TestCase):
    solutions: list[Callable[[str, str], bool]] = [
        is_shifted,
        is_shifted_find,
        is_shifted_kmp,
    ]

    cases: list[tuple[str, str, bool]] = [
        ("", "", True),
        ("abab", "ab", False),
        ("a", "b", False),
        ("aba", "abc", False),
        ("abcde", "cdeab", True),
        ("ababa", "abaab", True),
    ]

    def test_cases(self):
        for solution, (a, b, expected) in product(self.solutions, self.cases):
            sol: str = solution.__name__
            with self.subTest(solution=sol, a=a, b=b, expected=expected):
                self.assertEqual(expected, solution(a, b))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
