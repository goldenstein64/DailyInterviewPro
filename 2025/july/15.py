"""
You are given an array of integers in an arbitrary order. Return whether or not
it is possible to make the array non-decreasing by modifying at most 1 element
to any value.

We define an array is non-decreasing if array[i] <= array[i + 1] holds for every
i (1 <= i < n).

Example:

    [13, 4, 7] should return true, since we can modify 13 to any value 4 or
    less, to make it non-decreasing.

    [13, 4, 1] however, should return false, since there is no way to modify
    just one element to make the array non-decreasing.

Can you find a solution in O(n) time?
"""

import unittest
from itertools import pairwise


def check(ls: list[int]) -> bool:
    """
    My original implementation. This just counts how many times a pair of
    elements wasn't found to be non-decreasing. If it's greater than once, it's
    assumed it can't be fixed by changing one element.
    """
    corrected: bool = False
    for num1, num2 in pairwise(ls):
        if num1 > num2:
            if corrected:
                return False

            corrected = True

    return True


def check_sim(ls: list[int]) -> bool:
    """An implementation provided to me by ChatGPT."""
    changed = False
    for i in range(len(ls) - 1):
        if ls[i] > ls[i + 1]:
            if changed:
                return False
            # Try modifying nums[i] or nums[i+1]
            if i == 0 or ls[i - 1] <= ls[i + 1]:
                ls[i] = ls[i + 1]  # pretend to lower nums[i]
            else:
                ls[i + 1] = ls[i]  # pretend to raise nums[i+1]
            changed = True
    return True


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], bool]] = [
        ([], True),
        ([5], True),
        ([5, 10], True),
        ([9, 3], True),
        ([1, 4, 7], True),
        ([13, 4, 13], True),
        ([1, 13, 7], True),
        ([13, 4, 7], True),
        ([4, 2, 3], True),
        ([3, 6, 1], True),
        ([1, 1, 2, 1], True),
        ([1, 1, 2, 3], True),
        ([1, 2, 3, 1], True),
        ([4, 2, 1], False),
        ([13, 4, 1], False),
        ([4, 3, 2, 2], False),
        ([5, 1, 3, 2, 5], False),
        ([5, 4, 3, 2, 1], False),
    ]

    def test_all(self):
        for ls, expected in self.cases:
            with self.subTest(ls=ls, expected=expected):
                self.assertEqual(expected, check(ls))
                self.assertEqual(expected, check_sim(ls))


if __name__ == "__main__":
    unittest.main()
