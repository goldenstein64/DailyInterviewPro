"""
Given two rectangles, find the area of intersection.

Examples:

>>> intersection_area(Rectangle(0, 0, 3, 2), Rectangle(1, 1, 3, 3))
2

>>> intersection_area(Rectangle(0, 0, 1, 1), Rectangle(2, 2, 3, 3))
0

>>> intersection_area(Rectangle(0, 0, 1, 1), Rectangle(1, 1, 2, 2))
0
"""

import unittest
from dataclasses import dataclass
from collections.abc import Callable
from itertools import product


@dataclass
class Rectangle:
    min_x: int
    min_y: int
    max_x: int
    max_y: int

    def __post_init__(self):
        if self.min_x > self.max_x or self.min_y > self.max_y:
            raise ValueError("Invalid rectangle bounds")

    def __contains_wrong__(self, point: tuple[int, int]) -> bool:
        # ChatGPT says this is a closed interval test,
        # but Rectangle.area() assumes half-open intervals.
        return (
            self.min_x <= point[0] <= self.max_x
            and self.min_y <= point[1] <= self.max_y
        )

    def __contains__(self, point: tuple[int, int]) -> bool:
        return (
            self.min_x <= point[0] < self.max_x and self.min_y <= point[1] < self.max_y
        )

    def area(self) -> int:
        return (self.max_x - self.min_x) * (self.max_y - self.min_y)


def intersection_area(rect1: Rectangle, rect2: Rectangle) -> int:
    # ChatGPT says this is a closed interval test,
    # but Rectangle.area() assumes half-open intervals.
    if (
        rect1.max_x <= rect2.min_x
        or rect1.max_y <= rect2.min_y
        or rect2.max_x <= rect1.min_x
        or rect2.max_y <= rect1.min_y
    ):
        return 0

    intersection = Rectangle(
        min_x=max(rect1.min_x, rect2.min_x),
        min_y=max(rect1.min_y, rect2.min_y),
        max_x=min(rect1.max_x, rect2.max_x),
        max_y=min(rect1.max_y, rect2.max_y),
    )

    return intersection.area()


def intersection_area_gpt(rect1: Rectangle, rect2: Rectangle) -> int:
    # ChatGPT's implementation
    width = min(rect1.max_x, rect2.max_x) - max(rect1.min_x, rect2.min_x)
    height = min(rect1.max_y, rect2.max_y) - max(rect1.min_y, rect2.min_y)

    return max(width, 0) * max(height, 0)


class Tests(unittest.TestCase):
    solutions: list[Callable[[Rectangle, Rectangle], int]] = [
        intersection_area,
        intersection_area_gpt,
    ]

    cases: list[tuple[tuple[int, int, int, int], tuple[int, int, int, int], int]] = [
        ((0, 0, 3, 2), (1, 1, 3, 3), 2),
        ((0, 0, 1, 1), (2, 2, 3, 3), 0),
        ((0, 0, 1, 1), (1, 1, 2, 2), 0),
    ]

    def test_cases(self):
        for solution, (arg1, arg2, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, rect1=arg1, rect2=arg2, expected=expected):
                rect1 = Rectangle(*arg1)
                rect2 = Rectangle(*arg2)

                self.assertEqual(expected, solution(rect1, rect2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
