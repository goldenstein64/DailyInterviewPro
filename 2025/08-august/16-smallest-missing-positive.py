"""
You are given an array of integers. Return the smallest positive integer that is
not present in the array. The array may contain duplicate entries.

Example:
    Input: [3, 4, -1, 1]
    Output: 2
    Because it is the smallest positive integer that doesn't exist in the array

Your solution should run in linear time and use constant space.
"""

import unittest
from itertools import product
from typing import Callable


def smallest_missing_positive(nums: list[int]) -> int:
    """
    Return the smallest positive integer missing from the array.

    This has O(n) time complexity and O(n) space.
    """

    positives: set[int] = set(num for num in nums if num > 0)
    incremented_positives: set[int] = set(num + 1 for num in positives)
    incremented_positives.add(1)
    return min(incremented_positives - positives)


def smallest_missing_positive_lookup(nums: list[int]) -> int:
    """
    Return the smallest positive integer missing from the array. This mutates
    `nums` in place!

    This has O(n) time complexity and O(1) space.
    """

    n: int = len(nums)
    for i in range(n):
        while 0 <= (j := nums[i] - 1) < n and j != i and nums[j] != nums[i]:
            nums[i], nums[j] = nums[j], nums[i]

    for i, num in enumerate(nums):
        if num - 1 != i:
            return i + 1

    return n + 1


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        smallest_missing_positive,
        smallest_missing_positive_lookup,
    ]

    cases: list[tuple[list[int], int]] = [
        ([], 1),
        ([-1], 1),
        ([0], 1),
        ([1], 2),
        ([1, 1], 2),
        ([2], 1),
        ([2, 2], 1),
        ([2, 1], 3),
        ([3, 4, -1, 1], 2),
        ([3, 4, 2, 1], 5),
    ]

    def test_all(self):
        for solution, (nums, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, expected=expected):
                self.assertEqual(expected, solution(nums.copy()))


if __name__ == "__main__":
    unittest.main()
