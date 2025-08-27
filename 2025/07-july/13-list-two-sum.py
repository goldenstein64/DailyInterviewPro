"""
You are given a list of numbers, and a target number k. Return whether or not
there are two numbers in the list that add up to k.

Try to do it in a single pass of the list.

Example:

>>> two_sum([4, 7, 1, -3, 2], 5)
True
"""

import unittest


def two_sum(ls: list[int], k: int) -> bool:
    solutions: set[int] = set()
    for value in ls:
        if value in solutions:
            return True
        else:
            solutions.add(k - value)

    return False


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int, bool]] = [
        ([], 5, False),
        ([5], 5, False),
        ([5, 0], 5, True),
        ([1, 5, 0], 5, True),
        ([5, 1, 0], 5, True),
        ([5, 0, 1], 5, True),
        ([3, 2], 5, True),
        ([3, 1], 5, False),
        ([3, 3], 5, False),
        ([12, -7], 5, True),
        ([4, 7, 1, -3, 2], 5, True),
    ]

    def test_all(self):
        for ls, k, expected in self.cases:
            with self.subTest(ls=ls, k=k, expected=expected):
                self.assertEqual(expected, two_sum(ls, k))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
