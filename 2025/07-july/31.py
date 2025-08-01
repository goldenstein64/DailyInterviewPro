"""
There are n people lined up, and each have a height represented as an integer. A
murder has happened right in front of them, and only people who are taller than
everyone in front of them are able to see what has happened. How many witnesses
are there?

Example:
    Input: [3, 6, 3, 4, 1]
    Output: 3
    Explanation: Only [6, 4, 1] were able to see in front of them.

     #
     #
     # #
    ####
    ####
    #####
    36341                                 x (murder scene)
"""

import unittest
from dataclasses import dataclass, field
from functools import reduce
from itertools import product
from typing import Callable


@dataclass(frozen=True)
class WitnessState:
    rolling_max: int = 0
    result: list[int] = field(default_factory=list[int])


def witnesses_func(heights: list[int]) -> list[int]:
    new_state: WitnessState = reduce(
        lambda state, height: (
            state
            if height <= state.rolling_max
            else WitnessState(rolling_max=height, result=state.result + [height])
        ),
        reversed(heights),
        WitnessState(),
    )
    return [*reversed(new_state.result)]


def witnesses(heights: list[int]) -> list[int]:
    rolling_max: int = 0
    result: list[int] = []
    for height in reversed(heights):
        if height > rolling_max:
            result.append(height)
            rolling_max = height

    return [*reversed(result)]


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], list[int]]] = [witnesses, witnesses_func]

    cases: list[tuple[list[int], list[int]]] = [
        ([], []),
        ([0], []),
        ([5], [5]),
        ([3, 5], [5]),
        ([4, 4], [4]),
        ([5, 3], [5, 3]),
        ([4, 5, 3], [5, 3]),
        ([3, 6, 3, 4, 1], [6, 4, 1]),
    ]

    def test_all(self):
        for solution, (heights, expected) in product(self.solutions, self.cases):
            name = solution.__name__
            with self.subTest(solution=name, heights=heights, expected=expected):
                self.assertEqual(expected, solution(heights))


if __name__ == "__main__":
    unittest.main()
