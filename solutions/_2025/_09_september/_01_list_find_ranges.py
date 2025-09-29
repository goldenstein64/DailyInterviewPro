"""
Given a sorted list of numbers, return a list of pairs that represent all of
the consecutive numbers.

Assume that all numbers will be greater than or equal to 0, and each element can
repeat.

Example:

>>> find_ranges([0, 1, 2, 5, 7, 8, 9, 9, 10, 11, 15])
[(0, 2), (5, 5), (7, 11), (15, 15)]
"""

import unittest
from itertools import count, groupby, islice


def find_ranges(nums: list[int]) -> list[tuple[int, int]]:
    if not nums:
        return []

    result: list[tuple[int, int]] = []

    start: int = nums[0]
    end: int = start
    for num in islice(nums, 1, len(nums)):
        if num == end + 1:
            end = num
        elif num != end:
            result.append((start, end))
            start = end = num

    result.append((start, end))

    return result


def find_ranges_gpt(nums: list[int]) -> list[tuple[int, int]]:
    """ """
    if not nums:
        return []

    counter = count()

    def groupby_key(num: int) -> int:
        return num - next(counter)

    # group by value minus its index (shifts consecutive numbers into same group)
    groups = groupby(nums, key=groupby_key)
    list_groups = [list(group) for _, group in groups]
    return [(group[0], group[-1]) for group in list_groups]


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], list[tuple[int, int]]]] = [
        ([0], [(0, 0)]),
        ([0, 0], [(0, 0)]),
        ([0, 1], [(0, 1)]),
        ([0, 1, 2], [(0, 2)]),
        ([0, 1, 1, 2], [(0, 2)]),
        ([0, 1, 2, 2], [(0, 2)]),
        ([0, 0, 2], [(0, 0), (2, 2)]),
        ([0, 1, 2, 5, 7, 8, 9, 9, 10, 11, 15], [(0, 2), (5, 5), (7, 11), (15, 15)]),
    ]

    def test_cases(self):
        for nums, expected in self.cases:
            with self.subTest(nums=nums, expected=expected):
                self.assertEqual(expected, find_ranges(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
