"""
You are given a positive integer N which represents the number of steps in a
staircase. You can either climb 1 or 2 steps at a time. Write a function that
returns the number of unique ways to climb the stairs.

Can you find a solution in O(n) time?
"""

import unittest
from functools import cache

# this looks like the fibonacci sequence...
#
# 1: 1
# 0 -> 1
#
# 2: 2
# 0 -> 1 -> 2
# 0 -> 2
#
# 3: 3
# 0 -> 1 -> 2 -> 3
# 0 -> 1 -> 3
# 0 -> 2 -> 3
#
# 4: 5
# 0 -> 1 -> 2 -> 3 -> 4
# 0 -> 1 -> 2 -> 4
# 0 -> 1 -> 3 -> 4
# 0 -> 2 -> 3 -> 4
# 0 -> 2 -> 4
#
# 5: 8
# 0 -> 1 -> 2 -> 3 -> 4 -> 5
# 0 -> 1 -> 2 -> 3 -> 5
# 0 -> 1 -> 2 -> 4 -> 5
# 0 -> 1 -> 3 -> 4 -> 5
# 0 -> 1 -> 3 -> 5
# 0 -> 2 -> 3 -> 4 -> 5
# 0 -> 2 -> 3 -> 5
# 0 -> 2 -> 4 -> 5
#
# 6: 13
# 0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6
# 0 -> 1 -> 2 -> 3 -> 4 -> 6
# 0 -> 1 -> 2 -> 3 -> 5 -> 6
# 0 -> 1 -> 2 -> 4 -> 5 -> 6
# 0 -> 1 -> 3 -> 4 -> 5 -> 6
# 0 -> 2 -> 3 -> 4 -> 5 -> 6
# 0 -> 1 -> 2 -> 4 -> 6
# 0 -> 1 -> 3 -> 4 -> 6
# 0 -> 1 -> 3 -> 5 -> 6
# 0 -> 2 -> 3 -> 5 -> 6
# 0 -> 2 -> 3 -> 4 -> 6
# 0 -> 2 -> 4 -> 5 -> 6
# 0 -> 2 -> 4 -> 6


@cache
def staircase(n: int) -> int:
    if n < 4:
        return n
    else:
        return staircase(n - 1) + staircase(n - 2)


class Tests(unittest.TestCase):
    cases: list[tuple[int, int]] = [
        (0, 0),  # arguably, you can't climb a staircase that doesn't exist
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 5),
        (5, 8),
        (6, 13),
        (7, 21),
        (8, 34),
        (9, 55),
        (10, 89),
    ]

    def test_cases(self):
        for n, expected in self.cases:
            with self.subTest(n=n, expected=expected):
                self.assertEqual(expected, staircase(n))


if __name__ == "__main__":
    unittest.main()
