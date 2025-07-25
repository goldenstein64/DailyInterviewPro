"""
Given an array of n positive integers and a positive integer s, find the minimal
length of a contiguous subarray of which the sum ≥ s. If there isn't one, return
0 instead.

Example:

    Input: s = 7, nums = [2,3,1,2,4,3]
    Output: 2

Explanation: the subarray [4,3] has the minimal length under the problem
constraint.
"""

import unittest


class Solution:
    def min_sub_array_len(self, nums: list[int], s: int) -> int:
        i: int = 0
        rolling_sum: int = 0
        result: int | None = None
        for j, num in enumerate(nums):
            rolling_sum += num
            if rolling_sum >= s:
                while rolling_sum - nums[i] >= s:
                    rolling_sum -= nums[i]
                    i += 1

                result = j - i + 1 if result is None else min(result, j - i + 1)

        return 0 if result is None else result


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int, int]] = [
        ([], 1, 0),
        ([5], 3, 1),
        ([5], 5, 1),
        ([5], 8, 0),
        ([2, 3, 1, 2, 4, 3], 4, 1),
        ([2, 3, 1, 2, 4, 3], 6, 2),
        ([2, 3, 1, 2, 4, 3], 7, 2),
        ([2, 3, 1, 2, 4, 3], 9, 3),
        ([2, 3, 1, 2, 4, 3], 15, 6),
        ([2, 3, 1, 2, 4, 3], 16, 0),
    ]

    def test_all(self):
        for nums, s, expected in self.cases:
            with self.subTest(nums=nums, s=s, expected=expected):
                self.assertEqual(expected, Solution().min_sub_array_len(nums, s))


if __name__ == "__main__":
    unittest.main()
