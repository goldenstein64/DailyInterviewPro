"""
Given a non-negative integer `n`, convert the integer to hexadecimal and return
the result as a string. Hexadecimal is a base 16 representation of a number,
where the digits are `0123456789ABCDEF`. Do not use any builtin base conversion
functions like `hex`.

Example:

>>> to_hex(0)
'0'
>>> to_hex(123)
'7B'
>>> to_hex(-123)
'-7B'
>>> to_hex(65535)
'FFFF'
>>> to_hex(65536)
'10000'
"""

from typing import Final

digits: Final[str] = "0123456789ABCDEF"


def to_hex(n: int) -> str:
    if n == 0:
        return "0"
    elif n < 0:
        return f"-{to_hex(-n)}"

    result: list[str] = []
    while n > 0:
        result.append(digits[n % 16])
        n //= 16

    return "".join(reversed(result))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
