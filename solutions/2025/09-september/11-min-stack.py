"""
Design a simple stack that supports push, pop, top, and retrieving the minimum
element in constant time.

Example:

>>> stack = MinStack()
>>> stack.push(-2)
>>> stack.push(0)
>>> stack.push(-3)
>>> stack.get_min()
-3
>>> stack.pop()
-3
>>> stack.top()
0
>>> stack.get_min()
-2
"""


class MinStack:
    def __init__(self):
        self.data: list[int] = []
        self.min_data: list[int] = []

    def push(self, v: int) -> None:
        self.data.append(v)
        if self.min_data:
            self.min_data.append(min(self.min_data[-1], v))
        else:
            self.min_data.append(v)

    def pop(self) -> int | None:
        self.min_data.pop()
        return self.data.pop()

    def top(self) -> int:
        return self.data[-1]

    def get_min(self) -> int:
        return self.min_data[-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
