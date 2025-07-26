"""
You [have] 2 integers n and m representing an n by m grid, determine the number
of ways you can get from the top-left to the bottom-right of the matrix y going
only right or down.

Example:
    n = 2, m = 2

    This should return 2, since the only possible routes are:
    Right, down
    Down, right.
"""

from functools import cache
from itertools import product
import unittest
import math
from typing import Callable


@cache
def num_ways(n: int, m: int) -> int:
    """
    Calculate the number of paths through an n-by-m grid where all paths
    start at the top-left, end at the bottom-right, and can only move right or
    down.
    """
    if n == 0 or m == 0 or n == m == 1:
        return 0
    elif n == 1 or m == 1:
        return 1
    else:
        return num_ways(n - 1, m) + num_ways(n, m - 1)


def num_ways_gpt(n: int, m: int) -> int:
    """An implementation given to me by ChatGPT"""
    if n == 0 or m == 0:
        return 0

    return math.comb(n + m - 2, n - 1)


class Tests(unittest.TestCase):
    solutions: list[Callable[[int, int], int]] = [num_ways, num_ways_gpt]

    cases: list[tuple[int, int, int]] = [
        (0, 0, 0),
        (0, 10, 0),
        (10, 0, 0),
        (4, 1, 1),
        (1, 5, 1),
        (2, 2, 2),
        (2, 5, 5),
        (3, 3, 6),
        (3, 5, 15),
    ]

    def test_all(self):
        for solution, (n, m, expected) in product(self.solutions, self.cases):
            with self.subTest(solution=solution.__name__, n=n, m=m, expected=expected):
                self.assertEqual(expected, solution(n, m))


if __name__ == "__main__":
    unittest.main()
