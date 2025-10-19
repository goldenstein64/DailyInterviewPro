"""
Given a string with only `(` and `)`, find the minimum number of characters to
add or subtract to fix the string such that the brackets are balanced.

Example:

>>> fix_brackets('(()()')
1
"""

# I have already done this
from solutions._2025._08_august._27_str_parenthesis_removal import (
    count_invalid_parentheses as fix_brackets,  # type: ignore
)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
