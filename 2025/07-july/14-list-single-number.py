"""
Given a list of numbers, where every number shows up twice except for one number, find that one number.

Example:
    Input: [4, 3, 2, 4, 1, 3, 2]
    Output: 1

Challenge: Find a way to do this using O(1) memory.
"""

import unittest
from functools import reduce
from operator import xor
from typing import Callable


def single_number(nums: list[int]) -> int:
    """
    My first instinct solution. O(n) time and O(n) space.
    """
    singles: set[int] = set()
    for num in nums:
        if num in singles:
            singles.remove(num)
        else:
            singles.add(num)

    if len(singles) != 1:
        raise Exception("single number not found")

    return singles.pop()


def single_number_const_space(nums: list[int]) -> int:
    """
    My constant space solution, by sorting the list in-place and searching by
    pair.
    """

    # Every input list must have an odd length
    # Otherwise, it doesn't have an odd number of unique elements
    if len(nums) % 2 == 0:
        raise Exception("list does not have exactly one unique element")

    nums.sort()
    for i in range(1, len(nums), 2):
        item1 = nums[i - 1]
        item2 = nums[i]
        if item1 != item2:
            return item1

    return nums[-1]


def single_number_xor_trick(nums: list[int]) -> int:
    """
    ChatGPT came up with this solution. I would've never guessed it myself. It's
    known as the "XOR" trick.
    """
    result = 0
    for num in nums:
        result ^= num

    return result


def single_number_xor_trick2(nums: list[int]) -> int:
    """Shortening of ChatGPT's solution"""
    return reduce(xor, nums)


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        single_number,
        single_number_const_space,
        single_number_xor_trick,
        single_number_xor_trick2,
    ]

    @staticmethod
    def cases() -> list[tuple[list[int], int]]:
        return [
            ([4], 4),
            ([3, 3, 4], 4),
            ([3, 4, 3], 4),
            ([4, 3, 3], 4),
            ([4, 3, 2, 4, 1, 3, 2], 1),
        ]

    def test_all(self):
        for solution in self.solutions:
            for nums, expected in self.cases():
                with self.subTest(
                    solution=solution.__name__, nums=nums, expected=expected
                ):
                    self.assertEqual(expected, solution(nums))


if __name__ == "__main__":
    unittest.main()
