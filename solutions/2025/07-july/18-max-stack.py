"""
Implement a class for a stack that supports all the regular functions (push,
pop) and an additional function of max() which returns the maximum element in
the stack (return None if the stack is empty). Each method should run in
constant time.
"""

import unittest


class MaxStack:
    """
    Implemented with two stacks: one stores the actual number, and the other
    stores what the max value was when the last value was pushed.
    """

    def __init__(self):
        self.stack: list[int] = []
        self.max_stack: list[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        self.max_stack.append(max(self.max_stack[-1], val) if self.max_stack else val)

    def pop(self) -> int:
        self.max_stack.pop()
        return self.stack.pop()

    def max(self) -> int | None:
        return self.max_stack[-1] if self.max_stack else None


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
    unittest.main()
