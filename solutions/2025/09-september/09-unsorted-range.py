"""
Given a list of integers, return the bounds of the minimum range that must be
sorted so that the whole list would be sorted.

Example:

>>> find_range_naive([1, 7, 9, 5, 7, 8, 10])
(1, 5)
"""

from collections.abc import Callable, Sequence, Generator
from itertools import islice, product
import unittest
from math import inf


class reversed_enumerate[T]:
    def __new__(cls, seq: Sequence[T], start: int = 0) -> Generator[tuple[int, T]]:
        return ((i + start, seq[i]) for i in range(len(seq) - 1, -1, -1))


def find_range_naive(nums: list[int]) -> tuple[int, int] | None:
    """
    Find the smallest range of numbers that need to be sorted to form a sorted
    list. This uses a naive approach that just gets the smallest and largest
    values and compares them to the first and last values.
    """
    i: int = 0
    j: int = len(nums)

    while i < j:
        low = min(islice(nums, i, j))
        high = max(islice(nums, i, j))

        step_found: bool = False

        if nums[i] == low:
            step_found = True
            i += 1

        if nums[j - 1] == high:
            step_found = True
            j -= 1

        if not step_found:
            return (i, j - 1)

    return None


def find_range_two_pass_pointer(nums: list[int]) -> tuple[int, int] | None:
    """
    Find the smallest range of numbers that need to be sorted to form a sorted
    list. This uses a more involved approach where two unsorted pairs are
    found, followed by getting the min/max of the range including those
    pairs, and the pointers to those pairs are shifted away until the complete
    range is found.
    """
    if len(nums) <= 1:
        return None

    # find left-most unsorted index
    start: int = 0
    while start < len(nums) - 1 and nums[start] <= nums[start + 1]:
        start += 1

    if start == len(nums) - 1:
        return None  # list is sorted

    # find right-most unsorted index
    end: int = len(nums) - 1
    while nums[end - 1] <= nums[end]:
        end -= 1

    unsorted: list[int] = nums[start : end + 1]
    low = min(unsorted)
    high = max(unsorted)

    # expand outwards
    while start > 0 and nums[start - 1] > low:
        start -= 1

    while end < len(nums) - 1 and nums[end + 1] < high:
        end += 1

    return (start, end)


def find_range_two_pass_iter(nums: list[int]) -> tuple[int, int] | None:
    n = len(nums)
    if n <= 1:
        return None

    start: int | None = None
    end: int | None = None

    max_seen = -inf
    for i, num in enumerate(nums):
        if num < max_seen:
            end = i
        else:
            max_seen = num

    if end is None:
        return None

    min_seen = inf
    for i, num in reversed_enumerate(nums):
        if num > min_seen:
            start = i
        else:
            min_seen = num

    return (start, end) if start is not None else None


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], tuple[int, int] | None]] = [
        find_range_naive,
        find_range_two_pass_pointer,
        find_range_two_pass_iter,
    ]

    cases: list[tuple[list[int], tuple[int, int] | None]] = [
        ([], None),
        ([1], None),
        ([1, 2], None),
        ([2, 1], (0, 1)),
        ([1, 2, 3], None),
        ([3, 2, 1], (0, 2)),
        ([1, 3, 2], (1, 2)),
        ([2, 1, 3], (0, 1)),
        ([1, 2, 3, 4], None),
        ([1, 3, 2, 4], (1, 2)),
        ([1, 7, 9, 5, 7, 8, 10], (1, 5)),
        ([1, 3, 2, 4, 7, 6, 5, 8], (1, 6)),
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
