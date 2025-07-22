"""
Given a mathematical expression with just single digits, plus signs, negative
signs, and brackets, evaluate the expression. Assume the expression is properly
formed.

Example:
    Input: - ( 3 + ( 2 - 1 ) )
    Output: -4
"""

import unittest
from typing import Callable
from enum import Enum
from dataclasses import dataclass, field
from operator import neg, add, sub
from functools import partial


class State(Enum):
    EXPR = 0
    OP = 1


@dataclass
class EvalStack:
    val: int = 0
    ops: list[Callable[[int], int]] = field(default_factory=list[Callable[[int], int]])

    def apply(self, val: int) -> None:
        while len(self.ops) > 0:
            val = self.ops.pop()(val)

        self.val = val


def eval_once(stacks: list[EvalStack], state: State, c: str) -> State:
    match (state, c):
        case (_, c) if c.isspace():
            pass

        case (State.EXPR, "-"):
            stacks[-1].ops.append(neg)

        case (State.EXPR, "("):
            stacks.append(EvalStack())

        case (State.EXPR, c) if c.isnumeric():
            stacks[-1].apply(int(c))
            return State.OP

        case (State.OP, "+"):
            last_stack = stacks[-1]
            last_stack.ops.append(partial(add, last_stack.val))
            return State.EXPR

        case (State.OP, "-"):
            last_stack = stacks[-1]
            last_stack.ops.append(partial(sub, last_stack.val))
            return State.EXPR

        case (State.OP, ")"):
            last_stack = stacks.pop()
            stacks[-1].apply(last_stack.val)

        case args:
            raise ValueError(f"could not match on {args}")

    return state


def eval(expression: str) -> int:
    """
    evaluates an expression with neg, add, sub, and grouping operators. The
    expression is assumed to be valid, so there is minimal error handling.
    """

    stacks: list[EvalStack] = [EvalStack()]
    state: State = State.EXPR

    for c in expression:
        state = eval_once(stacks, state, c)

    return stacks[0].val


class Tests(unittest.TestCase):
    cases: list[tuple[str, int]] = [
        ("9", 9),
        ("-1", -1),
        ("3 + 6", 9),
        ("3 - 5", -2),
        ("3 - -1", 4),
        ("- ( 3 + ( 2 - 1 ) )", -4),
    ]

    def test_all(self):
        for expression, expected in self.cases:
            with self.subTest(expression=expression, expected=expected):
                self.assertEqual(expected, eval(expression))


if __name__ == "__main__":
    unittest.main()
