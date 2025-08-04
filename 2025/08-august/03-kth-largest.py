"""
Given a list, find the k-th largest element in the list.

Example:
    Input: list = [3, 5, 2, 4, 6, 8], k = 3
    Output: 5
"""

import unittest
from bisect import bisect
from heapq import nlargest
from itertools import product
from operator import neg
from typing import Callable


def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Obvious solution, sort the list and get the kth index

    This has O(n log n) time complexity and presumably O(n) space.
    """
    if k == 1:
        return max(nums)
    elif k == len(nums):
        return min(nums)
    else:
        return sorted(nums)[-k]


def find_kth_largest_sorted_list(nums: list[int], k: int) -> int:
    """
    Less obvious solution, keep a sorted list of the k largest and update it in
    a loop.

    This has O(k(n - k)) time complexity and O(n + k) space. It approaches O(n) for small k
    """
    if k == 1:
        return max(nums)
    elif k == len(nums):
        return min(nums)

    largest_nums: list[int] = nums[:k]
    largest_nums.sort(reverse=True)

    for i in range(k, len(nums)):
        num = nums[i]
        if num > largest_nums[-1]:
            j = bisect(largest_nums, -num, key=neg)
            largest_nums.insert(j, num)
            largest_nums.pop()

    return largest_nums[-1]


def find_kth_largest_heapq(nums: list[int], k: int) -> int:
    """
    A solution given to me by ChatGPT. Use heapq.nlargest.

    This apparently has O(n log k) time complexity and O(n + k) space.
    """
    if k == 1:
        return max(nums)
    elif k == len(nums):
        return min(nums)
    else:
        return nlargest(k, nums)[-1]


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int], int], int]] = [
        find_kth_largest,
        find_kth_largest_sorted_list,
        find_kth_largest_heapq,
    ]

    cases: list[tuple[list[int], int, int | Exception]] = [
        ([10], 1, 10),
        ([4, 3], 2, 3),
        ([3, 5, 2, 4, 6, 8], 1, 8),
        ([3, 5, 2, 4, 6, 8], 2, 6),
        ([3, 5, 2, 4, 6, 8], 3, 5),
        ([3, 5, 2, 4, 6, 8], 4, 4),
    ]

    def test_all(self):
        for solution, (nums, k, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, k=k, expected=expected):
                self.assertEqual(expected, solution(nums, k))


if __name__ == "__main__":
    unittest.main()
