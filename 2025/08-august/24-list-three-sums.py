"""
Given an array, nums, of n integers, find all unique triplets (three numbers,
a, b, & c) in nums such that a + b + c = 0. Note that there may not be any
triplets that sum to zero in nums, and that the triplets must not be duplicates.

Example:

>>> three_sum([0, -1, 2, -3, 1]) == {frozenset({0, -1, 1}), frozenset({2, -3, 1})}
True

>>> three_sum([1, -2, 1, 0, 5]) == {frozenset({-2, 1, 1})}
True
"""

import unittest
from itertools import combinations, product
from typing import Callable


def three_sum(nums: list[int]) -> set[frozenset[int]]:
    """
    Find all unique triplets of integers in `nums` that add up to 0.

    There is a formula for each triplet: (a, b, -a - b), where a and b are
    integers. This function just tries every combination of (a, b) and returns
    the ones that satisfy the formula.

    This has O(n^2) time complexity. Space complexity is hard to determine.
    """
    if len(nums) < 3:
        return set()

    nums_set = set(nums)
    return {
        frozenset((a, b, -a - b))
        for a, b in combinations(nums, 2)  # O(n^2)
        if -a - b not in (a, b) and -a - b in nums_set
    }


def three_sum_gpt(nums: list[int]) -> set[frozenset[int]]:
    """
    An implementation given to me by ChatGPT.

    Find all unique triplets of integers in `nums` that add up to 0.

    The (a, b, -a - b) formula also implies that there must be at least one
    positive and one negative in every triplet...
    """
    sorted_nums = sorted(nums)
    result: set[frozenset[int]] = set()
    n = len(nums)

    for i in range(n - 2):
        if i > 0 and sorted_nums[i] == sorted_nums[i - 1]:
            continue  # skip duplicates

        l, r = i + 1, n - 1
        while l < r:
            s = sorted_nums[i] + sorted_nums[l] + sorted_nums[r]
            if s > 0:
                r -= 1
            elif s < 0:
                l += 1
            else:
                result.add(frozenset((sorted_nums[i], sorted_nums[l], sorted_nums[r])))
                l += 1
                r -= 1
                while l < r and sorted_nums[l] == sorted_nums[l - 1]:
                    l += 1
                while l < r and sorted_nums[r] == sorted_nums[r + 1]:
                    r += 1

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], set[frozenset[int]]]] = [
        three_sum,
        three_sum_gpt,
    ]

    cases: list[tuple[list[int], set[frozenset[int]]]] = [
        ([], set()),
        ([1, 2], set()),
        ([1, 2, 3], set()),
        ([1, 2, 3, -3], {frozenset({-3, 1, 2})}),
        ([0, -1, 2, -3, 1], {frozenset({0, -1, 1}), frozenset({2, -3, 1})}),
        ([1, -2, 1, 0, 5], {frozenset({-2, 1})}),
    ]

    def test_cases(self):
        for solution, (nums, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, expected=expected):
                self.assertEqual(expected, solution(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
