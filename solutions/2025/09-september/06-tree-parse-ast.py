"""
You are given a binary tree representation of an arithmetic expression. In this
tree, each leaf is an integer value, and a non-leaf node is one of the four
operations: '+', '-', '*', or '/'.

Write a function that takes this tree and evaluates the expression.

Example:

>>> evaluate(((3, "+", 2), "*", (4, "+", 5)))
45
"""

from __future__ import annotations

import unittest
from operator import add, floordiv, mul, sub, truediv
from typing import Callable, Literal

type Op = Literal["+", "-", "*", "/", "//"]
type SyntaxTuple = float | tuple[SyntaxTuple, Op, SyntaxTuple]

evals: dict[Op, Callable[[float, float], float]] = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "//": floordiv,
}


def evaluate(expr: SyntaxTuple) -> float:
    match expr:
        case int(val) | float(val):
            return val
        case (left, op, right):
            return evals[op](evaluate(left), evaluate(right))


class Tests(unittest.TestCase):
    cases: list[tuple[SyntaxTuple, float]] = [
        (23, 23),
        ((5, "+", 8), 13),
        ((9, "+", 0), 9),
        ((90, "-", 1), 89),
        ((1, "-", 90), -89),
        ((6, "*", 4), 24),
        ((6, "/", 3), 2.0),
        ((1, "/", 5), 0.2),
        ((1, "//", 5), 0),
        (((2, "*", 3), "+", 4), 10),
        ((2, "*", (3, "+", 4)), 14),
        (((3, "+", 2), "*", (4, "+", 5)), 45),
    ]

    def test_cases(self):
        for expr, expected in self.cases:
            with self.subTest(expr=expr, expected=expected):
                self.assertAlmostEqual(expected, evaluate(expr), places=7)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
