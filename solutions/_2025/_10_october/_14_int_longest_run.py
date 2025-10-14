"""
Return the longest run of 1s for a given integer n's binary representation.

Example:

>>> longest_run(0b1111010)
4
"""


def longest_run(n: int) -> int:
    result: int = 0
    current: int = 0
    while n > 0:
        if n % 2 == 1:
            current += 1
        else:
            result = max(result, current)
            current = 0

        n //= 2

    return max(result, current)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
