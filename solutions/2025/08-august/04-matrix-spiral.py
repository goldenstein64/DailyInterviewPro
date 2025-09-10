"""
You are given a 2D array of integers. Print out the clockwise spiral traversal of the matrix.

Example:

>>> matrix_spiral(
...     [[1,  2,  3,  4,  5 ],
...      [6,  7,  8,  9,  10],
...      [11, 12, 13, 14, 15],
...      [16, 17, 18, 19, 20]]
... )
[1, 2, 3, 4, 5, 10, 15, 20, 19, 18, 17, 16, 11, 6, 7, 8, 9, 14, 13, 12]
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from itertools import count
from typing import Final, Generator


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rotate90(self) -> Point:
        return Point(-self.y, self.x)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


def traverse_region(begin: Point, end: Point, direction: Point) -> Generator[Point]:
    """
    Generate a line that is always hugging the region's left edge relative to
    its direction.
    """
    match direction:
        case Point(1, 0):
            return (Point(i, begin.y) for i in range(begin.x, end.x))
        case Point(0, 1):
            return (Point(end.x - 1, i) for i in range(begin.y, end.y))
        case Point(-1, 0):
            return (Point(i, end.y - 1) for i in range(end.x - 1, begin.x - 1, -1))
        case Point(0, -1):
            return (Point(begin.x, i) for i in range(end.y - 1, begin.y - 1, -1))
        case _:
            raise Exception


def matrix_spiral(m: list[list[int]]) -> list[int]:
    """
    Keep track of an open region and carve out lines from it clockwise until
    either dimension collapses to 0.

    This has O(m*n) time complexity and O(m*n) space, where m and n are the
    width and height of the matrix.
    """
    result: Final[list[int]] = []
    begin: Point = Point(0, 0)
    end: Point = Point(len(m[0]), len(m))
    direction: Point = Point(1, 0)
    while end.x - begin.x > 0 and end.y - begin.y > 0:
        result.extend(m[pt.y][pt.x] for pt in traverse_region(begin, end, direction))
        direction = direction.rotate90()

        # remove the part of the region that was traversed by traverse_region
        if direction.x > 0 or direction.y > 0:
            begin += direction
        else:
            end += direction

    return result


def matrix(w: int, h: int) -> list[list[int]]:
    """
    Create a matrix with width `w` and height `h`.

    Example:

    >>> matrix(2, 3)
    [[1, 2], [3, 4], [5, 6]]
    """
    nums = count(1)
    return [[next(nums) for _ in range(w)] for _ in range(h)]


class Tests(unittest.TestCase):
    def test_matrix(self):
        self.assertEqual([[1, 2], [3, 4], [5, 6]], matrix(2, 3))

    cases: list[tuple[list[list[int]], list[int]]] = [
        (matrix(1, 1), [1]),
        (matrix(1, 2), [1, 2]),
        (matrix(2, 1), [1, 2]),
        (matrix(2, 2), [1, 2, 4, 3]),
        (matrix(2, 3), [1, 2, 4, 6, 5, 3]),
        (matrix(3, 2), [1, 2, 3, 6, 5, 4]),
        (matrix(3, 3), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
        (
            matrix(5, 4),
            [1, 2, 3, 4, 5, 10, 15, 20, 19, 18, 17, 16, 11, 6, 7, 8, 9, 14, 13, 12],
        ),
    ]

    def test_cases(self):
        for m, expected in self.cases:
            with self.subTest(m=m, expected=expected):
                self.assertEqual(expected, matrix_spiral(m))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    unittest.main()
