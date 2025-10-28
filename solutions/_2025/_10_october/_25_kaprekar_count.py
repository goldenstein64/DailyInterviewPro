"""
Kaprekar's Constant is the number 6174. This number is special because it has
the property where for any 4-digit number that has 2 or more unique digits, if
you repeatedly apply a certain function it always reaches the number 6174.

This certain function is as follows:
- Order the number in ascending form and descending form to create 2 numbers.
- Pad the descending number with zeros until it is 4 digits in length.
- Subtract the ascending number from the descending number.
- Repeat.

Given a number n, find the number of times the function needs to be applied to
reach Kaprekar's constant.

Example:

>>> kaprekar_count(1)
5

>>> kaprekar_count(123)
3

>>> kaprekar_count_int(123)
3

>>> kaprekar_count_int(1)
5

Explanation:
3210 - 0123 = 3087
8730 - 0378 = 8352
8532 - 2358 = 6174
"""

from typing import Final
from collections.abc import Iterable
from math import log10, floor

KAPREKAR: Final[int] = 6174


def digits(n: int) -> Iterable[int]:
    while n > 0:
        yield n % 10
        n //= 10


def digit_len(n: int) -> int:
    return floor(log10(n)) + 1


def join_int(digits: Iterable[int]) -> int:
    result: int = 0
    for digit in digits:
        result *= 10
        result += digit

    return result


def kaprekar_count_int(n: int) -> int:
    result: int = 0
    for _ in range(10):
        asc_ls = sorted(digits(n))
        asc: int = join_int(asc_ls)
        desc: int = join_int(reversed(asc_ls))
        if (desc_len := digit_len(desc)) < 4:
            desc *= 10 ** (4 - desc_len)
        n = desc - asc
        result += 1
        # print(f"{desc:04d} - {asc:04d} = {n:04d}")
        if n == KAPREKAR:
            break

    return result


def kaprekar_count(n: int) -> int:
    result: int = 0
    while n != KAPREKAR:
        s: str = str(n)
        s = "0" * (4 - len(s)) + s
        asc: str = "".join(sorted(s))
        desc: str = "".join(reversed(asc))
        n = int(desc) - int(asc)
        # print(f"{desc:04s} - {asc:04s} = {n:04d}")
        result += 1

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
