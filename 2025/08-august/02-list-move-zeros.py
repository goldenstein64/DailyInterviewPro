"""
Given an array nums, write a function to move all 0's to the end of it while
maintaining the relative order of the non-zero elements.

Example:
    Input: [0, 1, 0, 3, 12]
    Output: [1, 3, 12, 0, 0]

You must do this in-place without making a copy of the array.
Minimize the total number of operations.
"""

import unittest
from itertools import product


class Solution:
    def move_zeros(self, nums: list[int]) -> None:
        """
        Most obvious solution, remove all zeros and append them to the end.

        This has O(n^2) time complexity and O(1) space.
        """
        zero_count = 0
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] == 0:  # comparison, n
                nums.pop(i)  # removal, z + n/2
                zero_count += 1

        nums += [0] * zero_count  # addition, z
        # P(n + 2z + n**2/2)
        # where n = len(nums), z = zero_count

    def move_zeros_swap(self, nums: list[int]) -> None:
        """
        I used this to implement Tetris' line clear algorithm; swap all
        non-zeros by an offset equal to the current number of zeros.

        This has O(n) time complexity and O(1) space.
        """
        offset = 0
        for i, num in enumerate(nums):
            if num == 0:  # comparison, n
                offset += 1
            elif offset > 0:
                nums[i], nums[i - offset] = nums[i - offset], num  # swap, p

        # P(n + p)
        # where n = len(nums), p = len(nums) - zero_count


class Tests(unittest.TestCase):
    solutions: list[str] = [
        "move_zeros",
        "move_zeros_tetris",
    ]

    cases: list[tuple[list[int], list[int]]] = [
        ([], []),
        ([1], [1]),
        ([0], [0]),
        ([0, 1, 2], [1, 2, 0]),
        ([1, 0, 2], [1, 2, 0]),
        ([1, 2, 0], [1, 2, 0]),
        ([0, 1, 2, 0], [1, 2, 0, 0]),
        ([0, 1, 0, 2, 0, 1, 0], [1, 2, 1, 0, 0, 0, 0]),
        ([0, 0, 0, 2, 0, 1, 3, 4, 0, 0], [2, 1, 3, 4, 0, 0, 0, 0, 0, 0]),
    ]

    def test_all(self):
        for solution, (original, expected) in product(self.solutions, self.cases):
            nums = original.copy()
            with self.subTest(solution=solution, nums=original, expected=expected):
                getattr(Solution(), solution)(nums)
                self.assertEqual(expected, nums)


if __name__ == "__main__":
    unittest.main()
