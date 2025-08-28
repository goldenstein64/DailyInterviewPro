"""
You are given an array of integers in an arbitrary order. Return whether or not
it is possible to make the array non-decreasing by modifying at most 1 element
to any value.

We define an array is non-decreasing if array[i] <= array[i + 1] holds for every
i (1 <= i < n).

Can you find a solution in O(n) time?

Examples:

>>> # True, since we can modify 13 to any value 4 or less
>>> check_gpt([13, 4, 7])
True

>>> # False, since there is no single element to fix
>>> check_gpt([13, 4, 1])
False
"""

import unittest
from itertools import pairwise, product


def check(ls: list[int]) -> bool:
    """
    My original implementation. This just counts how many times a pair of
    elements was found to be decreasing. If that count is greater than one, it's
    assumed it can't be fixed by changing one element.

    It also makes the assumption that if that count is equal to one, the issue
    can be fixed by changing one element. This assumption is wrong for four-
    element arrays like [2, 3, 0, 1].
    """
    corrected: bool = False
    for num1, num2 in pairwise(ls):
        if num1 > num2:
            if corrected:
                return False

            corrected = True

    return True


def check_gpt(ls: list[int]) -> bool:
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
    @staticmethod
    def cases() -> list[tuple[list[int], bool]]:
        return [
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
            ([4, 3, 4, 2], False),
            ([13, 4, 1], False),
            ([4, 3, 2, 2], False),
            ([5, 1, 3, 2, 5], False),
            ([5, 4, 3, 2, 1], False),
            ([2, 3, 0, 1], False),
        ]

    def test_cases(self):
        for solution in [check, check_gpt]:
            for ls, expected in self.cases():
                with self.subTest(solution=solution.__name__, ls=ls, expected=expected):
                    self.assertEqual(expected, solution(ls))

    def test_fuzz(self):
        for a, b, c, d in product(range(4), range(4), range(4), range(4)):
            with self.subTest(ls=[a, b, c, d]):
                self.assertEqual(check([a, b, c, d]), check_gpt([a, b, c, d]))


if __name__ == "__main__":
    unittest.main()
