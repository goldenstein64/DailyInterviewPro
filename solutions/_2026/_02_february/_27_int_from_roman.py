"""
Given a Roman numeral, find the corresponding decimal value. Inputs will be
between 1 and 3999.

Examples:

>>> roman_to_int("IX")
9

>>> roman_to_int("VII")
7

>>> roman_to_int("MCMIV")
1904
"""

from collections.abc import Callable


# This has been done before!
from solutions._2025._09_september._21_int_convert_roman import (
    roman_to_int as roman_to_int_old,
)


tiers = [
    ("IVX", 1),
    ("XLC", 10),
    ("CDM", 100),
    ("M**", 1_000),
]

digits: list[tuple[int, Callable[[str, str, str], str]]] = [
    (1, lambda i, v, x: i),
    (2, lambda i, v, x: i * 2),
    (3, lambda i, v, x: i * 3),
    (4, lambda i, v, x: i + v),
    (5, lambda i, v, x: v),
    (6, lambda i, v, x: v + i),
    (7, lambda i, v, x: v + i * 2),
    (8, lambda i, v, x: v + i * 3),
    (9, lambda i, v, x: i + x),
]
digits.sort(key=lambda t: len(t[1](*",,,")), reverse=True)


def roman_to_int(roman: str) -> int:
    pos: int = len(roman)
    result: int = 0
    for (i, v, x), multiplier in tiers:
        base: int = 0
        for new_base, digit in digits:
            check = digit(i, v, x)
            if roman.endswith(check, pos - len(check), pos):
                base = new_base
                pos -= len(check)
                break

        result += base * multiplier
        if pos <= 0:
            break

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    roman_to_int = roman_to_int_old
    doctest.testmod()
