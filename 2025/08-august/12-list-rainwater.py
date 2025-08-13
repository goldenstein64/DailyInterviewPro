"""
You have a landscape in which puddles can form. You are given an array of
non-negative integers representing the elevation at each location. Return the
amount of water that would accumulate if it rains.

Example:
    Input:
                   +
           + W W W + + W +
       + W + + W + + + + + +
    [0,1,0,2,1,0,1,3,2,1,2,1]

    Output: 6, because 6 Ws were counted
"""

import unittest
from typing import Callable
from itertools import product, islice, accumulate


def capacity(heights: list[int]) -> int:
    """
    Find how much rainwater can be carried by a height-map.

    This has O(n) time and O(n) space complexity.

    - Looping through the height-map is O(n) time, popping from the stack repeatedly
      is O(n) amortized since each height can be pushed to it at most once.
    - Copying the height-map is O(n) space, and the stack is O(n) because,
      again, it will only hold at most n items.

    The worst case for time and space would be an input like:
    [k, k - 1, k - 2, ..., 2, 1, 0, k] for some integer k.
    """

    if len(heights) < 3:  # 3 heights are required to form a divot
        return 0

    heights = heights[:]  # make a copy since we're modifying the list
    descending_indexes: list[int] = []
    result = 0
    for i, height in enumerate(heights):
        if not descending_indexes:
            descending_indexes.append(i)
            continue

        if height < heights[descending_indexes[-1]]:
            descending_indexes.append(i)
            continue

        fill_start = descending_indexes.pop()
        while descending_indexes and height >= heights[descending_indexes[-1]]:
            fill_start = descending_indexes.pop()

        if descending_indexes:
            fill_start = descending_indexes[-1]

        surface = min(heights[fill_start], height)
        for j in range(fill_start + 1, i):
            divot_height = heights[j]
            depth = surface - divot_height
            result += depth

            # covers the case where higher divots enclose lower ones
            heights[j] = surface

        descending_indexes.append(i)

    return result


def capacity_g2g_naive(heights: list[int]) -> int:
    result = 0

    for i in range(1, len(heights) - 1):
        height = heights[i]
        left = max(islice(heights, 0, i + 1))
        right = max(islice(heights, i, len(heights)))

        result += min(left, right) - height

    return result


def capacity_g2g_lr_pass(heights: list[int]) -> int:
    left = accumulate(heights, max)
    right = reversed(list(accumulate(reversed(heights), max)))

    return sum(min(l, r) - h for l, r, h in zip(left, right, heights))


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        capacity,
        capacity_g2g_naive,
        capacity_g2g_lr_pass,
    ]

    cases: list[tuple[list[int], int]] = [
        ([], 0),
        ([1], 0),
        ([0, 2], 0),
        ([1, 2, 3], 0),
        ([1, 2, 1], 0),
        ([1, 1, 1], 0),
        ([1, 0, 1], 1),
        ([2, 0, 1], 1),
        ([1, 0, 2], 1),
        ([2, 0, 2], 2),
        ([2, 1, 2], 1),
        ([1, 0, 1, 0], 1),
        ([0, 1, 0, 1], 1),
        ([1, 1, 0, 1], 1),
        ([1, 0, 0, 1], 2),
        ([1, 0, 0, 2], 2),
        ([2, 0, 0, 1], 2),
        ([2, 0, 0, 2], 4),
        ([1, 0, 1, 0, 1], 2),
        ([1, 0, 1, 0, 2], 2),
        ([2, 0, 1, 0, 1], 2),
        ([1, 0, 2, 0, 1], 2),
        ([2, 0, 1, 0, 2], 5),
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([3, 0, 1, 0, 4, 0, 2], 10),
        ([3, 0, 2, 0, 4], 7),
    ]

    def test_all(self):
        for solution, (heights, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, heights=heights, expected=expected):
                self.assertEqual(expected, solution(heights))


if __name__ == "__main__":
    unittest.main()
