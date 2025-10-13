"""
MS Excel column titles have the following pattern: A, B, C, ..., Z, AA, AB, ...,
AZ, BA, BB, ..., ZZ, AAA, AAB, ... etc. In other words, column 1 is named "A",
column 2 is "B", column 26 is "Z", column 27 is "AA" and so forth. Given a
positive integer, find its corresponding column name.

Examples:

>>> convert_to_title(1)
'A'

>>> convert_to_title(2)
'B'

>>> convert_to_title(26)
'Z'

>>> convert_to_title(51)
'AY'

>>> convert_to_title(52)
'AZ'

>>> convert_to_title(53)
'BA'

>>> convert_to_title(676)
'YZ'

>>> convert_to_title(702)
'ZZ'

>>> convert_to_title(704)
'AAB'
"""

# >>> divmod(702, 26)
# (27, 0)
# >>> divmod(702 - 1, 26)
# (26, 25)
# >>> divmod(702, 27)
# (26, 0)
# >>> 26 * 27
# 702
# >>> 26 + 26 * 26
# 702
# >>> 26 + 26 * 26 + 26 * 26 * 26
# 18278
# >>> 26 * 27 * 27
# 18954
# >>> 26 * 26 * 27
# 18252
# >>> 26 * 26 * 28
# 18928
# >>> 26 * 25 * 27
# 17550
# >>> 26 * 27 + 26 * 26 * 26
# 18278
# >>> 26 * (27 + 26 * 26)
# 18278
# >>> 26 + 26 * (26 + 26 * (26))
# 18278
# >>> f = lambda x: 26 + 26 * x
# >>> f(26)
# 702
# >>> f(1)
# 52
# >>> f(0)
# 26
# >>> f(f(26))
# 18278
# >>> f(f(f(26)))
# 475254
# >>> f(0)
# 26
# >>> f(f(0))
# 702
# >>> f(f(f(0)))
# 18278
# >>> f(f(f(f(0))))
# 475254

from typing import Final

ORD_A: Final[int] = ord("A")


def convert_to_title(n: int) -> str:
    """
    Convert a 1-based index into a column title seen in a spreadsheet
    application. This uses a derived algorithm from a REPL session I was
    experimenting with, pasted above in the comments.

    This uses roughly O(log26 n) time and O(log26 n) space.
    """
    # convert n to a base-26 integer with leading zeroes,
    # which means keep track of length, since 0s are interpreted as As.
    n -= 1
    n_range: int = 26
    length: int = 1
    while n >= n_range:
        length += 1
        n -= n_range
        n_range *= 26

    # take each digit from the base-26 integer and turn it into a letter.
    result: list[str] = []
    for _ in range(length):
        result.append(chr(ORD_A + n % 26))
        n //= 26

    result.reverse()
    return "".join(result)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
