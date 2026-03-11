"""
Given an integer, reverse the digits. Do not convert the integer into a string
and reverse it.

Examples:

>>> reversed(135)
531

>>> reversed(-321)
-123
"""

# This has been done before!
from solutions._2026._01_january._05_int_reverse import reverse_integer as reversed_old
from solutions._2025._09_september._10_reverse_int32 import (
    reverse_int32 as reversed_old2,
)


def reversed(value: int) -> int:
    abs_value: int = abs(value)
    sign: int = -1 if value < 0 else 1
    result: int = 0
    while abs_value > 0:
        result *= 10
        result += abs_value % 10
        abs_value //= 10

    return sign * result


if __name__ == "__main__":
    from typing import cast, Any
    import doctest

    doctest.testmod()
    reversed = cast(Any, reversed_old)
    doctest.testmod()
    reversed = cast(Any, reversed_old2)
    doctest.testmod()
