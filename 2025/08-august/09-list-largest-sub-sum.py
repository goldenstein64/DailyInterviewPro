"""
You are given an array of integers. Find the maximum sum of all possible
contiguous subarrays of the array.

Your solution should run in linear time.

Example:

>>> max_subarray_sum([34, -50, 42, 14, -5, 86])
137

Explanation: The contiguous subarray with the largest sum is [42, 14, -5, 86].
"""

import unittest
from itertools import accumulate, islice, product
from typing import Callable


def max_subarray_sum(arr: list[int]) -> int:
    """
    Find the contiguous sequence of numbers that give the greatest sum. This
    uses Kadane's algorithm.

    This has O(n) time complexity and O(1) space.

    See: https://www.geeksforgeeks.org/dsa/largest-sum-contiguous-subarray
    """
    if not arr:
        return 0

    max_ending = res = arr[0]
    for num in islice(arr, 1, len(arr)):
        max_ending = max(max_ending + num, num)
        res = max(res, max_ending)

    return res


def max_subarray_sum_accum(arr: list[int]) -> int:
    """
    A shorter implementation that uses accumulate to create an iterator of sums.
    """
    return 0 if not arr else max(accumulate(arr, lambda s, v: max(s + v, v)))


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        max_subarray_sum,
        max_subarray_sum_accum,
    ]

    cases: list[tuple[list[int], int]] = [
        ([], 0),
        ([10], 10),
        ([-10], -10),
        ([-10, -5], -5),
        ([5, -10], 5),
        ([5, -20, 10], 10),
        ([-50, 30, -20, 10], 30),
        ([34, -50, 42, 14, -5, 86], 137),
    ]

    def test_all(self):
        for solution, (arr, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, arr=arr, expected=expected):
                self.assertEqual(expected, solution(arr))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
