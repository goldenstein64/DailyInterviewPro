"""
Given an array of n positive integers and a positive integer s, find the minimal
length of a contiguous subarray of which the sum ≥ s. If there isn't one, return
0 instead.

Example:

>>> min_sub_array_len([2, 3, 1, 2, 4, 3], 7)
2

Explanation: the subarray [4,3] has the minimal length under the problem
constraint.
"""

import unittest
from collections import deque
from typing import Iterable, Callable
from itertools import product


def min_sub_array_len_gen(nums: Iterable[int], s: int) -> int:
    """a streaming alternative implementation given to me by ChatGPT."""
    window: deque[int] = deque()
    rolling_sum: int = 0
    min_len: int | None = None

    for num in nums:
        window.append(num)
        rolling_sum += num

        while rolling_sum >= s:
            min_len = len(window) if min_len is None else min(min_len, len(window))
            rolling_sum -= window.popleft()

    return 0 if min_len is None else min_len


def min_sub_array_len(nums: list[int], s: int) -> int:
    """
    An implementation that uses a sliding window to determine the shortest
    valid sub-array.
    """
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
    solutions: list[Callable[[list[int], int], int]] = [
        min_sub_array_len_gen,
        min_sub_array_len,
    ]

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
        for solution, (nums, s, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, s=s, expected=expected):
                self.assertEqual(expected, solution(nums, s))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
