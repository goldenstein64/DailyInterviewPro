"""
Given a list of numbers, for each element find the next element that is larger
than the current element. Return the answer as a list of indices. If there are
no elements larger than the current element, then use `-1` instead.

Example:

>>> map_next_brute_force([3, 2, 5, 6, 9, 8])
[2, 2, 3, 4, -1, -1]

>>> map_next_brute_force([3, 2, 1])
[-1, -1, -1]

>>> map_next_brute_force([1, 2, 3])
[1, 2, -1]

>>> map_next_brute_force([9, 4, 3, 8, 10])
[4, 3, 3, 4, -1]
"""

import unittest
from itertools import islice, product
from collections.abc import Callable
from math import inf


def map_next_brute_force(nums: list[int]) -> list[int]:
    """
    For every number in `nums`, find the first number after it that is larger.
    This uses a simple algorithm where every number is processed one-by-one from
    beginning to end.

    The worst case is processing a non-decreasing array, which is O(n^2) time
    and O(n) space. The best case is processing an increasing array, which is
    O(n) time and O(n) space.

    For a uniformly random array, this probably has O(n^2) time and O(n) space,
    based on the notion that each number will traverse about i/n * n/2, or i/2,
    of the array, where i is the number's index in sorted(nums).
    """
    result: list[int] = []
    for i, current in enumerate(nums):
        found: int = -1
        for j, num in islice(enumerate(nums), i + 1, len(nums)):
            if num > current:
                found = j
                break

        result.append(found)

    return result


def map_next(nums: list[int]) -> list[int]:
    """
    For every number in `nums`, find the first number after it that is larger.
    Theory-crafting here, but it might be faster to process the array in
    reverse.
    """

    result: list[int] = [-1] * len(nums)
    indexes: list[tuple[int, int]] = list(enumerate(range(len(nums))))
    while indexes:
        _, i = indexes.pop()
        current: int = nums[i]
        max_num: float = -inf
        for j_index, j in reversed(indexes):
            num = nums[j]
            if num > current:
                break
            elif num > max_num:
                indexes.pop(j_index)
                result[j] = i
                max_num = num

    return result


def map_next_dict(nums: list[int]) -> list[int]:
    """
    For every number in `nums`, find the first number after it that is larger.
    This tries to use a list of running maximums and a dictionary mapping to
    figure out what the next number larger than current would be.

    This algorithm is _wrong_ for any result list with a decreasing index, e.g.
    `[9, 4, 3, 8, 10]`
    """
    running_max_indexes: list[int] = []
    mapping: dict[int, int] = {}
    running_max_i: int = -1
    running_max: float = -inf
    for i, num in enumerate(nums):
        if num > running_max:
            mapping[running_max_i] = i
            running_max_i = i
            running_max = num

        running_max_indexes.append(running_max_i)

    return [mapping.get(i, -1) for i in running_max_indexes]


def map_next_gpt(nums: list[int]) -> list[int]:
    """
    For every number in `nums`, find the first number after it that is larger.
    This uses a... "monotonic stack" to keep track of all numbers that haven't
    found their next number larger.

    This was suggested by a conversation with ChatGPT.

    Source: https://chatgpt.com/share/69953fc7-1538-8007-8cdd-9493efffc874
    """
    decreasing_stack: list[int] = []
    result: list[int] = [-1] * len(nums)
    for i, num in enumerate(nums):
        while decreasing_stack and num > nums[decreasing_stack[-1]]:
            j = decreasing_stack.pop()
            result[j] = i

        decreasing_stack.append(i)

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], list[int]]] = [
        map_next_brute_force,
        # map_next,
        # map_next_dict,
        map_next_gpt,
    ]

    cases: list[tuple[list[int], list[int]]] = [
        ([3, 2, 5, 6, 9, 8], [2, 2, 3, 4, -1, -1]),
        ([3, 2, 1], [-1, -1, -1]),
        ([1, 2, 3], [1, 2, -1]),
        ([9, 4, 3, 8, 10], [4, 3, 3, 4, -1]),
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
