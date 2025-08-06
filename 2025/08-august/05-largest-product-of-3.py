"""
You are given an array of integers. Return the largest product that can be made
by multiplying any 3 integers in the array.

Example:

    Input: [-4, -4, 2, 8]
    Output: 128

    the largest product can be made by multiplying -4 * -4 * 8 = 128.
"""

import unittest
from itertools import combinations, product
from math import prod
from typing import Callable
from heapq import nsmallest, nlargest


def maximum_product_of_three(nums: list[int]) -> int:
    """
    brute force solution, get the max of all combinations.

    This has O(n^3) time complexity and O(1) space
    """
    return max(prod(comb) for comb in combinations(nums, 3))


def maximum_product_of_three_extremes(nums: list[int]) -> int:
    """
    slightly more involved solution, sort the list and multiply the highest
    three elements _unless_ the first two elements are negative and the last one
    is non-negative.

    In the case this is true, take the maximum of the product of the smallest
    two elements and the product of the second-largest and third-largest
    elements, and multiply that with the largest element.

    This has O(n log n) time complexity and O(n) space.
    """

    sorted_nums = sorted(nums)
    if (
        (smallest := sorted_nums[0]) < 0
        and (second_smallest := sorted_nums[1]) < 0
        and (largest := sorted_nums[-1]) >= 0
    ):
        return (
            max(smallest * second_smallest, sorted_nums[-3] * sorted_nums[-2]) * largest
        )
    else:
        return prod(sorted_nums[-3:])


def maximum_product_of_three_extremes_gpt(nums: list[int]) -> int:
    """
    ChatGPT's suggested shorter version of the three_extremes implementation.
    """

    sorted_nums = sorted(nums)
    return max(
        sorted_nums[0] * sorted_nums[1] * sorted_nums[-1],
        sorted_nums[-3] * sorted_nums[-2] * sorted_nums[-1],
    )


def maximum_product_of_three_heap(nums: list[int]) -> int:
    smallest_2 = nsmallest(2, nums)
    largest_3 = nlargest(3, nums)
    return max(prod(smallest_2) * largest_3[0], prod(largest_3))


def maximum_product_of_three_sorted_list(nums: list[int]) -> int:
    smallest_2: list[int] = []
    largest_3: list[int] = []
    for num in nums:
        if len(smallest_2) == 2:
            if num < smallest_2[1]:
                if num < smallest_2[0]:
                    smallest_2[0], smallest_2[1] = num, smallest_2[0]
                else:
                    smallest_2[1] = num
        elif len(smallest_2) == 1:
            if num < smallest_2[0]:
                smallest_2.insert(0, num)
            else:
                smallest_2.append(num)
        else:
            smallest_2.append(num)

        if len(largest_3) == 3:
            if num > largest_3[2]:
                if num <= largest_3[1]:
                    largest_3[2] = num
                elif num > largest_3[0]:
                    largest_3[0], largest_3[1], largest_3[2] = (
                        num,
                        largest_3[0],
                        largest_3[1],
                    )
                else:
                    largest_3[1], largest_3[2] = num, largest_3[1]
        elif len(largest_3) == 2:
            if num <= largest_3[1]:
                largest_3.append(num)
            elif num > largest_3[0]:
                largest_3.insert(0, num)
            else:
                largest_3.insert(1, num)
        elif len(largest_3) == 1:
            if num > largest_3[0]:
                largest_3.insert(0, num)
            else:
                largest_3.append(num)
        else:
            largest_3.append(num)

    return max(prod(smallest_2) * largest_3[0], prod(largest_3))


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        maximum_product_of_three,
        maximum_product_of_three_extremes,
        maximum_product_of_three_extremes_gpt,
        maximum_product_of_three_heap,
        maximum_product_of_three_sorted_list,
    ]

    cases: list[tuple[list[int], int]] = [
        ([1, 2, 3], 6),
        ([-1, -2, -3], -6),
        ([-1, -2, -3, -4, 0], 0),
        ([-1, -2, -3, -4], -6),
        ([1, -2, -3, -4], 12),
        ([-1, 2, -3, -4], 24),
        ([-1, -2, 3, -4], 24),
        ([-1, -2, -3, 4], 24),
        ([1, 2, -3, -4], 24),
        ([1, -2, 3, -4], 24),
        ([-1, 2, 3, -4], 12),
        ([1, -2, -3, 4], 24),
        ([-1, 2, -3, 4], 12),
        ([-1, -2, 3, 4], 8),
        ([1, 2, 3, -4], 6),
        ([1, 2, -3, 4], 8),
        ([1, -2, 3, 4], 12),
        ([-1, 2, 3, 4], 24),
        ([1, 2, 3, 4], 24),
        ([-4, -4, 2, 8], 128),
    ]

    def test_all(self):
        for solution, (lst, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, lst=lst, expected=expected):
                self.assertEqual(expected, solution(lst))


if __name__ == "__main__":
    unittest.main()
