"""
Given two strings, determine the edit distance between them. The edit distance
is defined as the minimum number of edits (insertion, deletion, or substitution)
needed to change one string to the other.

For example, "biting" and "sitting" have an edit distance of 2 (substitute b for
s, and insert a t).
"""

import unittest
from itertools import product

import numpy as np


def distance_rec(s1: str, s2: str) -> int:
    if len(s1) == 0:
        return len(s2)
    elif len(s2) == 0:
        return len(s1)
    elif s1[0] == s2[0]:
        return distance_rec(s1[1:], s2[1:])
    else:
        return 1 + min(
            distance_rec(s1[1:], s2),
            distance_rec(s1, s2[1:]),
            distance_rec(s1[1:], s2[1:]),
        )


def distance(s1: str, s2: str) -> int:
    """computes the Levenshtein distance between two words"""
    s1 = s1.lower()
    s2 = s2.lower()
    if s1 == s2:
        return 0

    len1: int = len(s1)
    len2: int = len(s2)

    matrix: np.ndarray = np.zeros((len1 + 1, len2 + 1), int)
    matrix[:, 0] = range(len1 + 1)
    matrix[0, :] = range(len2 + 1)

    for i, j in product(range(len1), range(len2)):
        cost = 0 if s1[i] == s2[j] else 1
        matrix[i + 1, j + 1] = min(
            matrix[i, j + 1] + 1,  # deletion
            matrix[i + 1, j] + 1,  # insertion
            matrix[i, j] + cost,  # swap
        )

    return int(matrix[-1, -1])


class Tests(unittest.TestCase):
    cases: list[tuple[str, str, int]] = [
        ("", "", 0),
        ("x", "x", 0),
        ("cat", "sat", 1),
        ("cat", "at", 1),
        ("cat", "chat", 1),
        ("snail", "crook", 5),
        ("biting", "sitting", 2),
    ]

    def test_smoke(self):
        for s1, s2, expected in self.cases:
            with self.subTest(s1=s1, s2=s2, expected=expected):
                self.assertEqual(expected, distance_rec(s1, s2))
                self.assertEqual(expected, distance(s1, s2))


if __name__ == "__main__":
    unittest.main()
