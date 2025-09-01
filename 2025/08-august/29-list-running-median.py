"""
You are given a stream of numbers. Compute the median for each new element.

Example:

>>> median = running_median_naive([2, 1, 4, 7, 2, 0, 5])
>>> type(median)
<class 'generator'>
>>> list(median)
[2, 1.5, 2, 3.0, 2, 2.0, 2]
"""

from __future__ import annotations

import heapq
import unittest
from bisect import bisect
from collections.abc import Generator, Iterable
from itertools import product
from typing import Callable


def running_median_naive(stream: Iterable[int]) -> Generator[int | float]:
    """
    Generate running medians from a stream. This maintains a sorted
    list of all numbers so far and looks in the middle for each step.

    This has O(n) time complexity and O(1) space at each step, or O(n^2) time and
    O(n) space total.
    """
    sorted_list: list[int] = []
    for i, value in enumerate(stream):
        sorted_list.insert(bisect(sorted_list, value), value)
        if i % 2 == 0:
            yield sorted_list[len(sorted_list) // 2]
        else:
            median1 = sorted_list[len(sorted_list) // 2 - 1]
            median2 = sorted_list[len(sorted_list) // 2]
            yield (median1 + median2) / 2


def running_median_2heap(stream: Iterable[int]) -> Generator[int | float]:
    """
    Generate running medians from a stream. This maintains a max heap and min
    heap of all numbers lesser and greater than the median, respectively.

    This has O(log n) time complexity and O(1) space at each step, or O(n log n)
    time and O(n) space total.
    """
    low: list[int] = []  # max heap, use negative numbers
    high: list[int] = []  # min heap
    median: int | float = 0
    for i, value in enumerate(stream):
        # add the value to the correct side of the last median
        if i % 2 == 0:  # even values
            # the difference in length will always be 1 when we get here, so no
            # need to check
            if value < median:
                heapq.heappush(low, -value)
            else:
                heapq.heappush(high, value)

            median = -low[0] if len(low) > len(high) else high[0]
            yield median
        else:  # odd values
            # the difference in length may be greater than 1, so try balancing
            # them
            if value < median:
                heapq.heappush(low, -value)
                if len(low) > len(high):
                    heapq.heappush(high, -heapq.heappop(low))
            else:
                heapq.heappush(high, value)
                if len(high) > len(low):
                    heapq.heappush(low, -heapq.heappop(high))

            median = (-low[0] + high[0]) / 2
            yield median


def running_median_2heap_gpt(stream: Iterable[int]) -> Generator[int | float]:
    """
    A 2-heap implementation given to me by ChatGPT.

    This has O(n log n) time complexity and O(n) space.
    """
    low: list[int] = []
    high: list[int] = []

    for value in stream:
        if not low or value <= -low[0]:
            heapq.heappush(low, -value)
        else:
            heapq.heappush(high, value)

        # rebalance
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))

        # median
        if len(low) == len(high):
            yield (-low[0] + high[0]) / 2
        else:
            yield -low[0]


class Tests(unittest.TestCase):
    solutions: list[Callable[[Iterable[int]], Generator[int | float]]] = [
        running_median_naive,
        running_median_2heap,
        running_median_2heap_gpt,
    ]

    cases: list[tuple[list[int], list[int | float]]] = [
        ([], []),
        ([4], [4]),
        ([1, 1, 1], [1, 1.0, 1]),
        ([2, 3], [2, 2.5]),
        ([4, 3, 5], [4, 3.5, 4]),
        ([-4, 2, -3], [-4, -1.0, -3]),
        ([9, 5, 10, 4, 8], [9, 7.0, 9, 7.0, 8]),
        ([2, 1, 4, 7, 2, 0, 5], [2, 1.5, 2, 3.0, 2, 2.0, 2]),
    ]

    def test_cases(self):
        for solution, (stream, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, stream=stream, expected=expected):
                self.assertEqual(expected, list(solution(stream)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
