"""
Given an array of integers of size n, where all elements are between 1 and n
inclusive, find all of the elements of [1, n] that do not appear in the array.
Some numbers may appear more than once.

Example:

>>> sorted(find_missing_numbers([4, 5, 2, 6, 8, 2, 1, 5]))
[3, 7]

>>> sorted(find_missing_numbers([4, 6, 2, 6, 7, 2, 1]))
[3, 5]
"""

import unittest
from collections.abc import Callable
from itertools import product


def find_missing_numbers_sorted(nums: list[int]) -> list[int]:
    """
    Find all missing consecutive integers in `nums` between 1 and `len(nums)`.
    This uses a simple algorithm that sorts the list and adds all integers in
    the range of what the number was supposed to be and what number
    was missing.

    This has O(n log n) time complexity and O(n + k) space complexity, where
    n = len(nums) and k is the number of missing integers.
    """
    if not nums:
        return []

    i: int = 1
    result: list[int] = []
    for num in sorted(nums):
        result.extend(range(i, num))
        i = num + 1

    result.extend(range(i, len(nums) + 1))

    return result


def find_missing_numbers_set(nums: list[int]) -> list[int]:
    """
    Find all missing consecutive integers in `nums` between 1 and `len(nums)`.
    This uses a simple algorithm that puts all values between 1 and `len(nums)`
    in a set and removes all values in the input list. The resulting set is
    turned into a list and returned.

    This has O(n + k) time complexity and O(n + k) space complexity, where
    n = len(nums) and k is the number of missing integers.
    """
    if not nums:
        return []

    val_set: set[int] = set(range(1, len(nums) + 1))
    return list(val_set.difference(nums))


def find_missing_numbers_set_gpt(nums: list[int]) -> list[int]:
    """
    A version of `find_missing_numbers_set` that tries to avoid materializing
    `val_set`. This change was suggested by ChatGPT.

    This has O(n + k) time complexity and O(n + k) space complexity, where
    n = len(nums) and k is the number of missing integers.
    """
    if not nums:
        return []

    max_val: int = max(nums)
    seen: set[int] = set(nums)
    result: list[int] = [i for i in range(1, max_val + 1) if i not in seen]
    result.extend(range(max_val + 1, len(nums) + 1))
    return result


find_missing_numbers = find_missing_numbers_set_gpt


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], list[int]]] = [
        find_missing_numbers_set,
        find_missing_numbers_set_gpt,
        find_missing_numbers_sorted,
    ]

    cases: list[tuple[list[int], list[int]]] = [
        ([], []),
        ([3, 1, 2], []),
        ([4, 5, 2, 6, 8, 2, 1, 5], [3, 7]),
        ([4, 6, 2, 6, 7, 2, 1], [3, 5]),
        ([2, 2, 2, 2], [1, 3, 4]),
    ]

    def test_cases(self):
        for solution, (nums, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, expected=expected):
                self.assertEqual(expected, sorted(solution(nums)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
