"""
Implement a class for a stack that supports all the regular functions (push,
pop) and an additional function of max() which returns the maximum element in
the stack (return None if the stack is empty). Each method should run in
constant time.

Example:

>>> s = MaxStack()
>>> s.push(1)
>>> s.push(2)
>>> s.push(3)
>>> s.push(2)
>>> s.max()
3
>>> s.pop()
2
>>> s.max()
3
>>> s.pop()
3
>>> s.max()
2
"""

from __future__ import annotations
from collections.abc import Iterable, Sequence
from typing import overload
from itertools import accumulate
import unittest


class MaxStack(Sequence[int]):
    """
    Implemented with two stacks: one stores the actual number, and the other
    stores what the max value was when the last value was pushed.
    """

    def __init__(self, iterable: Iterable[int] | None = None):
        self.stack: list[int]
        self.max_stack: list[int]
        if iterable is None:
            self.stack = []
            self.max_stack = []
        else:
            stack: list[int] = list(iterable)
            self.stack = stack
            self.max_stack = list(accumulate(stack, max))

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.max_stack.append(max(self.max_stack[-1], val) if self.max_stack else val)

    def pop(self) -> int:
        self.max_stack.pop()
        return self.stack.pop()

    def peek(self) -> int | None:
        return self.stack[-1] if self.stack else None

    def max(self) -> int | None:
        return self.max_stack[-1] if self.max_stack else None

    def __len__(self) -> int:
        return len(self.stack)

    @overload
    def __getitem__(self, index: int) -> int: ...
    @overload
    def __getitem__(self, index: slice) -> MaxStack: ...

    def __getitem__(self, index: int | slice) -> int | MaxStack:
        if type(index) is slice:
            return MaxStack(self.stack[index])
        else:
            return self.stack[index]


class Tests(unittest.TestCase):
    def test_smoke(self):
        s = MaxStack()
        s.push(1)
        s.push(2)
        s.push(3)
        s.push(2)
        self.assertEqual(3, s.max())
        s.pop()
        self.assertEqual(3, s.max())
        s.pop()
        self.assertEqual(2, s.max())

    def test_empty_pop(self):
        s = MaxStack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_empty_max(self):
        s = MaxStack()
        self.assertIsNone(s.max())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
