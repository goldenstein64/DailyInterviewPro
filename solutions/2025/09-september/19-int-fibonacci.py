"""
The Fibonacci sequence is the integer sequence defined by the recurrence
relation: F(n) = F(n-1) + F(n-2), where F(0) = 0 and F(1) = 1. In other words,
the nth Fibonacci number is the sum of the prior two Fibonacci numbers. Below
are the first few values of the sequence:

0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

Given a number n, print the n-th Fibonacci Number.

Examples:
>>> fibonacci(1)
1
>>> fibonacci(5)
5
>>> fibonacci(6)
8
>>> fibonacci(10)
55
"""


def fibonacci(n: int) -> int:
    """
    Compute the nth fibonacci number
    """

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return a


if __name__ == "__main__":
    import doctest

    doctest.testmod()
