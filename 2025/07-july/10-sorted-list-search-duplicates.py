"""
Given a sorted array, A, with possibly duplicated elements, find the indices of
the first and last occurrences of a target element, x. Return -1 if the target
is not found.

Examples:

>>> get_range([1,3,3,5,7,8,9,9,9,15], 9)
[6, 8]

>>> get_range([100, 150, 150, 153], 150)
[1, 2]

>>> get_range([1,2,3,4,5,6,10], 9)
[-1, -1]
"""

import unittest

# from bisect import bisect_left, bisect_right


def bisect_left_bounds(arr: list[int], target: int, lo: int, hi: int) -> int:
    if lo >= hi:
        return hi

    mid = (lo + hi) // 2
    val = arr[mid]
    if target <= val:
        return bisect_left_bounds(arr, target, lo, mid)
    else:
        return bisect_left_bounds(arr, target, mid + 1, hi)


def bisect_left(arr: list[int], target: int) -> int:
    return bisect_left_bounds(arr, target, 0, len(arr))


def bisect_right_bounds(arr: list[int], target: int, lo: int, hi: int) -> int:
    if lo >= hi:
        return hi

    mid = (lo + hi) // 2
    val = arr[mid]
    if target >= val:
        return bisect_right_bounds(arr, target, mid + 1, hi)
    else:
        return bisect_right_bounds(arr, target, lo, mid)


def bisect_right(arr: list[int], target: int) -> int:
    return bisect_right_bounds(arr, target, 0, len(arr))


def get_range(arr: list[int], target: int) -> list[int]:
    first: int = bisect_left(arr, target)
    if first == len(arr) or arr[first] != target:
        return [-1, -1]

    return [first, bisect_right(arr, target) - 1]


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int, list[int]]] = [
        ([1, 3, 3, 5, 7, 8, 9, 9, 9, 15], 9, [6, 8]),
        ([100, 150, 150, 153], 150, [1, 2]),
        ([1, 2, 3, 4, 5, 6, 10], 9, [-1, -1]),
        ([1, 2, 2, 2, 2, 3, 4, 7, 8, 8], 2, [1, 4]),
        ([], 5, [-1, -1]),
    ]

    def test_all(self):
        for arr, target, expected in self.cases:
            with self.subTest(arr=arr, target=target, expected=expected):
                self.assertEqual(expected, get_range(arr, target))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
