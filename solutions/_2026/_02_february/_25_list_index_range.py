"""
Given a sorted list with duplicates, and a target number n, find the range in
which the number exists (represented as a tuple (low, high), both inclusive. If
the number does not exist in the list, return None).

Examples:

>>> index_range([1, 1, 3, 5, 7], 1)
(0, 1)

>>> index_range([1, 2, 3, 4], 5)  # returns None

"""

from typing import TYPE_CHECKING, Any
import unittest

if TYPE_CHECKING:
    from _typeshed import (
        SupportsDunderGE,
        SupportsDunderGT,
        SupportsDunderLE,
        SupportsDunderLT,
    )

    type Comparable = (
        SupportsDunderLT[Any]
        | SupportsDunderGT[Any]
        | SupportsDunderLE[Any]
        | SupportsDunderGE[Any]
    )


def _index_left(ls: list[int], target: int, lo: int, hi: int) -> int:
    if lo >= hi:
        raise ValueError("could not find target!")

    mid = (lo + hi) // 2
    value = ls[mid]
    if value > target:
        raise ValueError("target is out of range!")

    if value < target:
        if ls[mid + 1] == target:
            return mid + 1
        else:
            return _index_left(ls, target, lo=mid, hi=hi)
    else:  # value == target
        if ls[mid - 1] > target:
            return mid - 1
        else:
            return _index_left(ls, target, lo=lo, hi=mid)


def _index_right(ls: list[int], target: int, lo: int, hi: int) -> int:
    if lo >= hi:
        raise ValueError("could not find target!")

    mid = (lo + hi) // 2
    value = ls[mid]
    if value < target:
        raise ValueError("target is out of range!")

    if value > target:
        if ls[mid - 1] == target:
            return mid - 1
        else:
            return _index_right(ls, target, lo=lo, hi=mid)
    else:  # value == target
        if ls[mid + 1] > target:
            return mid
        else:
            return _index_right(ls, target, lo=mid, hi=hi)


def _index_range(
    ls: list[int], target: int, lo: int, hi: int
) -> tuple[int, int] | None:
    if lo >= hi:
        return None

    mid = (lo + hi) // 2
    value = ls[mid]
    if value > target:
        return _index_range(ls, target, lo=lo, hi=mid)
    elif value < target:
        return _index_range(ls, target, lo=mid, hi=lo)
    else:  # value == target
        return (
            _index_left(ls, target, lo=lo, hi=mid),
            _index_right(ls, target, lo=mid, hi=hi),
        )


def index_range(ls: list[int], target: int) -> tuple[int, int] | None:
    if ls[0] == target:
        return (0, _index_right(ls, target, lo=0, hi=len(ls)))
    elif ls[-1] == target:
        return (_index_left(ls, target, lo=0, hi=len(ls)), len(ls) - 1)
    else:
        return _index_range(ls, target, lo=0, hi=len(ls))


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int, tuple[int, int] | None]] = [
        ([1, 1, 3, 5, 7], 1, (0, 1)),
        ([1, 3, 5, 7, 7], 7, (3, 4)),
        ([1, 3, 5, 7, 9], 5, (2, 2)),
        ([1, 3, 5, 5, 7, 9], 5, (2, 3)),
        ([1, 2, 3, 4], 5, None),
        ([1, 2, 3, 4], 0, None),
    ]

    def test_cases(self):
        for ls, target, expected in self.cases:
            with self.subTest(ls=ls, target=target, expected=expected):
                self.assertEqual(sorted(ls), ls)

                self.assertEqual(expected, index_range(ls, target))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
