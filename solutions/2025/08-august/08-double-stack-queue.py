"""
Implement a queue class using two stacks. A queue is a data structure that
supports the FIFO protocol (First in = first out). Your class should support the
enqueue and dequeue methods like a standard queue.
"""

from __future__ import annotations

import unittest
from typing import Iterable, Protocol


class Queue[T](Protocol):
    def __init__(self, iterable: Iterable[T] | None = None): ...
    def enqueue(self, value: T) -> None: ...
    def dequeue(self) -> T: ...


class MyQueue[T](Queue[T]):
    """
    An implementation of a queue using two stacks. This implementation is O(n)
    worst-case in both cases, although it is O(1) for repeated enqueues or
    repeated dequeues.

    Moving everything from the dequeue stack to the enqueue stack is unnecessary
    since the user doesn't receive any information when calling enqueue.
    """

    def __init__(self, iterable: Iterable[T] | None = None):
        self.enqueue_stack: list[T] = list(iterable) if iterable else []
        self.dequeue_stack: list[T] = []

    def enqueue(self, value: T) -> None:
        while self.dequeue_stack:
            self.enqueue_stack.append(self.dequeue_stack.pop())

        self.enqueue_stack.append(value)

    def dequeue(self) -> T:
        while self.enqueue_stack:
            self.dequeue_stack.append(self.enqueue_stack.pop())

        return self.dequeue_stack.pop()


class QueueGPT[T](Queue[T]):
    """
    An implementation I edited by ChatGPT, a double-stack queue that has an
    O(1) enqueue and an amortized O(1) dequeue that is cheaper in most cases.
    """

    def __init__(self, iterable: Iterable[T] | None = None):
        self.enqueue_stack: list[T] = list(iterable) if iterable else []
        self.dequeue_stack: list[T] = []

    def enqueue(self, value: T) -> None:
        self.enqueue_stack.append(value)

    def __transfer(self) -> None:
        if self.dequeue_stack:
            return

        if not self.enqueue_stack:
            raise IndexError

        while self.enqueue_stack:
            self.dequeue_stack.append(self.enqueue_stack.pop())

    def dequeue(self) -> T:
        self.__transfer()
        return self.dequeue_stack.pop()

    def peek(self) -> T:
        self.__transfer()
        return self.dequeue_stack[-1]


class Tests(unittest.TestCase):
    solutions: list[type[Queue[int]]] = [MyQueue, QueueGPT]

    def test_smoke(self):
        for Solution in self.solutions:
            with self.subTest(Solution=Solution.__name__):
                queue: Queue[int] = Solution()
                queue.enqueue(1)
                queue.enqueue(2)
                queue.enqueue(3)
                self.assertEqual(1, queue.dequeue())
                self.assertEqual(2, queue.dequeue())
                self.assertEqual(3, queue.dequeue())


if __name__ == "__main__":
    unittest.main()
