"""
You are given an array of integers. Return an array of the same size where the
element at each index is the product of all the elements in the original array
except for the element at that index.

You cannot use division or floor division in this problem.

Example:

>>> products_naive([1, 2, 3, 4, 5])
[120, 60, 40, 30, 24]
"""

import unittest
from collections.abc import Callable
from itertools import product
from math import prod


def products_naive(nums: list[int]) -> list[int]:
    """
    Produce a list of numbers such that each index `i` contains a product of all
    elements in `nums` except for `nums[i]`. This uses a simple algorithm that
    filters by index and computes `n` products.

    This algorithm has O(n^2) time complexity and O(n) space.
    """

    result: list[int] = []
    n: int = len(nums)
    for i in range(n):
        result.append(prod(nums[j] for j in range(n) if j != i))

    return result


# [2, 3, 4, 5, 6]
def products_prefix_suffix(nums: list[int]) -> list[int]:
    """
    Produce a list of numbers such that each index `i` contains a product of all
    elements in `nums` except for `nums[i]`. This produces a prefix list and
    suffix product list whose elements are multiplied element-wise.
    """
    prefix: int = 1
    prefixes: list[int] = []
    for num in nums:
        prefixes.append(prefix)
        prefix *= num

    suffix: int = 1
    suffixes: list[int] = []
    for num in reversed(nums):
        suffixes.append(suffix)
        suffix *= num

    return [pre * suf for pre, suf in zip(prefixes, reversed(suffixes))]


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], list[int]]] = [
        products_naive,
        products_prefix_suffix,
    ]

    cases: list[tuple[list[int], list[int]]] = [
        ([], []),
        ([10], [1]),
        ([10, 5], [5, 10]),
        ([10, 5, 15], [75, 150, 50]),
        ([1, 2, 3, 4, 5], [120, 60, 40, 30, 24]),
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
