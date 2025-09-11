"""
Design a simple stack that supports push, pop, top, and retrieving the minimum
element in constant time.

Example:

>>> stack = MinStack()
>>> stack.push(-2)
>>> stack.push(0)
>>> stack.push(-3)
>>> stack.min()
-3
>>> stack.pop()
-3
>>> stack.peek()
0
>>> stack.min()
-2
"""

from __future__ import annotations
from collections.abc import Sequence, Iterable
from typing import overload
from itertools import accumulate
import unittest


class MinStack(Sequence[int]):
    def __init__(self, iterable: Iterable[int] | None = None):
        self.stack: list[int]
        self.min_stack: list[int]

        if iterable is None:
            self.stack = []
            self.min_stack = []
        else:
            stack: list[int] = list(iterable)
            self.stack = stack
            self.min_stack = list(accumulate(stack, min))

    def push(self, v: int) -> None:
        self.stack.append(v)
        if self.min_stack:
            self.min_stack.append(min(self.min_stack[-1], v))
        else:
            self.min_stack.append(v)

    def pop(self) -> int | None:
        self.min_stack.pop()
        return self.stack.pop()

    def peek(self) -> int | None:
        return self.stack[-1] if self.stack else None

    def min(self) -> int | None:
        return self.min_stack[-1] if self.min_stack else None

    def __len__(self):
        return len(self.stack)

    @overload
    def __getitem__(self, index: int) -> int: ...
    @overload
    def __getitem__(self, index: slice) -> MinStack: ...

    def __getitem__(self, index: int | slice) -> int | MinStack:
        if type(index) is slice:
            return MinStack(self.stack[index])
        else:
            return self.stack[index]


class Tests(unittest.TestCase):
    def test_smoke(self):
        s = MinStack()
        s.push(-1)
        s.push(-2)
        s.push(-3)
        s.push(-2)
        self.assertEqual(-3, s.min())
        s.pop()
        self.assertEqual(-3, s.min())
        s.pop()
        self.assertEqual(-2, s.min())

    def test_empty_pop(self):
        s = MinStack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_empty_max(self):
        s = MinStack()
        self.assertIsNone(s.min())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
