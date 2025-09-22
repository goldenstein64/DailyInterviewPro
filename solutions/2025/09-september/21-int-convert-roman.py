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

from __future__ import annotations

import re
from collections.abc import Callable


def pattern_from_tier(
    tier: str, multiplier: int = 1
) -> Callable[[str, int], tuple[int, int]]:
    i, v, x = tier
    nine = f"{i}{x}"
    four = f"{i}{v}"
    pattern = re.compile(f"{i}{x}|{i}{v}|{v}{i}{{0,3}}|{i}{{1,3}}$")

    def to_added(input: str, endpos: int) -> tuple[int, int]:
        match = pattern.search(input, endpos=endpos)
        if not match:
            return 0, endpos

        added = 0
        group = match.group()
        if group == nine:
            added = 9
        elif group == four:
            added = 4
        else:
            added = (5 if v in group else 0) + group.count(i)

        return added * multiplier, match.start()

    return to_added


thousands_pattern = re.compile(r"M{1,3}$")


def thousands(input: str, endpos: int) -> tuple[int, int]:
    match = thousands_pattern.search(input, endpos=endpos)
    if not match:
        return 0, endpos

    return match.group().count("M") * 1_000, match.start()


hundreds = pattern_from_tier("CDM", 100)
tens = pattern_from_tier("XLC", 10)
ones = pattern_from_tier("IVX", 1)


def digit_to_roman(digit: int, numerals: str) -> str:
    match digit:
        case 0:
            return ""
        case 1 | 2 | 3:
            return numerals[0] * digit
        case 4:
            return numerals[0] + numerals[1]
        case 5:
            return numerals[1]
        case 6 | 7 | 8:
            return numerals[1] + numerals[0] * (digit - 5)
        case 9:
            return numerals[0] + numerals[2]
        case _:
            raise ValueError("not a digit")


def int_to_roman(num: int) -> str:
    return (
        digit_to_roman(num // 1000 % 10, "M**")
        + digit_to_roman(num // 100 % 10, "CDM")
        + digit_to_roman(num // 10 % 10, "XLC")
        + digit_to_roman(num % 10, "IVX")
    )


def roman_to_int(roman: str) -> int:
    result: int = 0
    endpos = len(roman)
    added, endpos = ones(roman, endpos)
    result += added
    added, endpos = tens(roman, endpos)
    result += added
    added, endpos = hundreds(roman, endpos)
    result += added
    added, endpos = thousands(roman, endpos)
    result += added

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
