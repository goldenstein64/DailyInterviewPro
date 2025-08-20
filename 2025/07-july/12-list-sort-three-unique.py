"""
Given a list of numbers with only 3 unique numbers (1, 2, 3), sort the list in
O(n) time.

Challenge: Try sorting the list using constant space.

Example:
    Input: [3, 3, 2, 1, 3, 2, 1]
    Output: [1, 1, 2, 2, 3, 3, 3]
"""

import unittest
from collections import Counter
from random import randint, shuffle


def sort_nums(nums: list[int]) -> None:
    counts: Counter[int] = Counter(nums)
    index = 0
    for num in range(1, 4):
        for _ in range(counts.get(num, 0)):
            nums[index] = num
            index += 1


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], list[int]]] = [
        ([], []),
        ([1], [1]),
        ([3, 1, 2], [1, 2, 3]),
        ([3, 3, 2, 1, 3, 2, 1], [1, 1, 2, 2, 3, 3, 3]),
    ]

    def test_all(self):
        for original, expected in self.cases:
            nums = original.copy()
            with self.subTest(nums=nums):
                sort_nums(nums)
                self.assertEqual(expected, nums)

    def test_fuzz(self):
        for _ in range(100):
            expected: list[int] = []
            for i in range(1, 4):
                expected.extend([i] * randint(0, 100))

            nums: list[int] = expected.copy()
            shuffle(nums)
            with self.subTest(nums=nums, expected=expected):
                sort_nums(nums)
                self.assertEqual(expected, nums)


if __name__ == "__main__":
    unittest.main()
