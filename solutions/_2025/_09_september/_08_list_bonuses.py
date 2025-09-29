"""
You are the manager of a number of employees who all sit in a row. The CEO would
like to give bonuses to all of your employees, but since the company did not
perform so well this year the CEO would like to keep the bonuses to a minimum.

The rules of giving bonuses is that:
- Each employee begins with a bonus factor of 1x.
- For each employee, if they perform better than the person sitting next to
them, the employee is given +1 higher bonus (and up to +2 if they perform better
than both people to their sides).

Given a list of employee's performance, find the bonuses each employee should
get.

Example:

>>> get_bonuses([1, 2, 3, 2, 3, 5, 1])
[1, 2, 3, 1, 2, 3, 1]
"""

import unittest
from collections.abc import Callable
from itertools import pairwise, product


def get_bonuses_build(performance: list[int]) -> list[int]:
    if not performance:
        return []

    result: list[int] = [1]
    for a, b in pairwise(performance):
        result.append(2 if a < b else 1)
        if a > b:
            result[-2] += 1

    return result


def get_bonuses(performance: list[int]) -> list[int]:
    result: list[int] = [1] * len(performance)
    for i in range(len(performance) - 1):
        [first, second] = performance[i : i + 2]
        if first > second:
            result[i] += 1
        elif first < second:
            result[i + 1] += 1

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], list[int]]] = [
        get_bonuses,
        get_bonuses_build,
    ]

    cases: list[tuple[list[int], list[int]]] = [
        ([], []),
        ([20], [1]),
        ([10, 10], [1, 1]),
        ([10, 20], [1, 2]),
        ([20, 10], [2, 1]),
        ([10, 20, 30], [1, 2, 2]),
        ([10, 30, 20], [1, 3, 1]),
        ([1, 2, 3, 2, 3, 5, 1], [1, 2, 3, 1, 2, 3, 1]),
    ]

    def test_cases(self):
        for solution, (performance, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, performance=performance, expected=expected):
                self.assertEqual(expected, solution(performance))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
