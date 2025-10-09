"""
You are given an array of integers. Return the length of the longest consecutive
elements sequence in the array.

Example:

>>> longest_consecutive([100, 4, 200, 1, 3, 2])
4
"""

import unittest
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Interval:
    start: int
    end: int

    def __len__(self):
        return self.end - self.start + 1

    def __contains__(self, val: int) -> bool:
        return self.start - 1 <= val <= self.end + 1


def longest_consecutive(nums: list[int]) -> int:
    """
    Find the length of the longest consecutive integer sequence. This uses a
    simplistic algorithm that creates a set of intervals and tries to create,
    extend, or merge them together each iteration.

    This uses O(nk) time and O(nk) space, where n = len(nums) and
    k = len(intervals). This has a worst-case time complexity of O(n^2) when
    every element has its own interval, and best-case time complexity of O(n)
    when every element is in one big interval.
    """
    if not nums:
        return 0

    intervals: set[Interval] = set()

    for n in nums:  # O(n)
        chosen_intervals: set[Interval] = {i for i in intervals if n in i}  # O(k)

        new_interval: Interval
        if chosen_intervals:
            intervals -= chosen_intervals
            new_interval = Interval(
                start=min(n, min(i.start for i in chosen_intervals)),
                end=max(n, max(i.end for i in chosen_intervals)),
            )
        else:
            new_interval = Interval(n, n)

        intervals.add(new_interval)

    return max(map(len, intervals))


def longest_consecutive_find_start(nums: list[int]) -> int:
    """
    Find the length of the longest consecutive integer sequence. This uses an
    algorithm suggested by Google's Learn About and GeeksForGeeks.

    This uses O(n) time and O(n) space.

    See: https://www.geeksforgeeks.org/dsa/longest-consecutive-subsequence
    """
    if not nums:
        return 0

    nums_set: set[int] = set(nums)
    result: int = 1
    for n in nums:  # O(n)
        if n - 1 in nums_set or n + 1 not in nums_set:  # O(1)
            continue

        # O(1), since latter numbers in the sequence don't get here
        length: int = 2
        while n + length in nums_set:
            length += 1

        result = max(result, length)  # O(1)

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        longest_consecutive,
        longest_consecutive_find_start,
    ]

    cases: list[tuple[list[int], int]] = [
        ([], 0),
        ([1], 1),
        ([10], 1),
        ([1, 2], 2),
        ([2, 1, 4], 2),
        ([2, 1, 4, 3], 4),
        ([100, 4, 200, 1, 3, 2], 4),
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
