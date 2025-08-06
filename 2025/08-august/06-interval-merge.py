"""
You are given an array of intervals - that is, an array of tuples (start, end).
The array may not be sorted, and could contain overlapping intervals. Return
another array where the overlapping intervals are merged.

Example:
    Input: [(1, 3), (5, 8), (4, 10), (20, 25)]
    Output: [(1, 3), (4, 10), (20, 25)]

    since (5, 8) and (4, 10) can be merged into (4, 10).
"""

import unittest
from itertools import islice, product
from typing import Callable


def is_overlapping(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """Check whether two intervals overlap."""
    return (
        a[0] <= b[0] <= a[1]
        or a[0] <= b[1] <= a[1]
        or b[0] <= a[0] <= b[1]
        or b[0] <= a[1] <= b[1]
    )


def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Brute force solution: try every combination of tuples and merge the ones
    that overlap.
    """
    if len(intervals) <= 1:
        return intervals

    last: set[tuple[int, int]] = set()
    result: set[tuple[int, int]] = {*intervals}

    if len(result) <= 1:
        return intervals

    while last != result:
        if not result:
            return []

        last = result
        result = set()
        removed: set[tuple[int, int]] = set()

        for i, a in enumerate(last):
            if a in removed:
                continue

            merged = a
            for b in islice(last, i + 1, len(last)):
                if b not in removed and is_overlapping(merged, b):
                    removed.add(merged)
                    merged = (min(merged[0], b[0]), max(merged[1], b[1]))
                    removed.add(b)

            result.add(merged)

    return list(result)


def merge_naive_g4g(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    A solution I found on GeeksForGeeks: sort all intervals and merge those that
    overlap with previous intervals. This was marked as the "naive solution."

    This has worst case O(n^2) time complexity (nothing is merged on every
    iteration) and O(n) space.
    It has best case O(n) time complexity (everything is merged on the first
    iteration).
    Average time complexity cannot be calculated.
    """
    if len(intervals) <= 1:
        return intervals

    sorted_intervals = sorted(intervals)
    result: list[tuple[int, int]] = []

    # check for all possible overlaps
    for i, a in enumerate(sorted_intervals):
        start, end = a

        # skip already merged intervals
        if result and end <= result[-1][1]:
            continue

        # find the end of the merged range
        for b in islice(sorted_intervals, i + 1, len(sorted_intervals)):
            if b[0] <= end:
                end = max(end, b[1])

        result.append((start, end))

    return result


def merge_involved_g4g(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    A solution I found on GeeksForGeeks: sort the intervals and merge those that
    overlap with the last included interval.

    This has O(n log n) time complexity (due to sorting) and O(n) space.
    """
    if len(intervals) <= 1:
        return intervals

    sorted_i = sorted(intervals)

    last = sorted_i[0]
    result: list[tuple[int, int]] = [last]

    for interval in islice(sorted_i, 1, len(sorted_i)):
        if interval[0] <= last[1]:
            last = result[-1] = (last[0], max(last[1], interval[1]))
        else:
            last = interval
            result.append(interval)

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[tuple[int, int]]], list[tuple[int, int]]]] = [
        merge,
        merge_naive_g4g,
        merge_involved_g4g,
    ]

    cases: list[tuple[list[tuple[int, int]], set[tuple[int, int]]]] = [
        ([], set()),
        ([(1, 5)], {(1, 5)}),
        ([(1, 5), (1, 5)], {(1, 5)}),
        ([(1, 3), (4, 8)], {(1, 3), (4, 8)}),
        ([(4, 8), (1, 3)], {(1, 3), (4, 8)}),
        ([(1, 4), (4, 8)], {(1, 8)}),
        ([(4, 8), (1, 4)], {(1, 8)}),
        ([(1, 5), (4, 8)], {(1, 8)}),
        ([(4, 8), (1, 5)], {(1, 8)}),
        ([(1, 3), (3, 5), (5, 7)], {(1, 7)}),
        ([(1, 3), (4, 4), (5, 7)], {(1, 3), (4, 4), (5, 7)}),
        ([(1, 3), (5, 8), (4, 10), (20, 25)], {(1, 3), (4, 10), (20, 25)}),
        ([(7, 8), (1, 5), (2, 4), (4, 6)], {(1, 6), (7, 8)}),
    ]

    def test_all(self):
        for solution, (intervals, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, intervals=intervals, expected=expected):
                merged = set(solution(intervals))
                self.assertEqual(expected, merged, f"{expected} != {merged}")


if __name__ == "__main__":
    unittest.main()
