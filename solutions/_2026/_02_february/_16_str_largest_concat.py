"""
Given a number of integers, combine them so it would create the largest number.

>>> largest_num([17, 7, 2, 45, 72])
'77245217'
"""

from collections.abc import Iterator
from itertools import tee
import unittest


# this has been done before!
from solutions._2025._09_september._24_str_largest_concat import Tests


def largest_num(nums: list[int]) -> str:
    """
    Create the largest possible integer from concatenating the input list of
    non-negative integers. This is wrong. See these cases:

    >>> # gives '6054548546' instead
    >>> largest_num([54, 546, 548, 60])
    '6054854654'

    >>> # gives '9533430' instead
    >>> largest_num([3, 30, 34, 5, 9])
    '9534330'

    smaller numbers are given higher priority than larger numbers, when in
    reality they should be given the same priority as their last integer.
    """
    str_nums: Iterator[str] = map(str, nums)
    str_nums1, str_nums2 = tee(str_nums)
    max_len: int = max(map(len, str_nums1))
    sorted_nums: list[str] = sorted(
        str_nums2, key=lambda s: s + "A" * (max_len - len(s)), reverse=True
    )
    return "0" if sorted_nums[0] == "0" else "".join(sorted_nums)


Tests.solutions = [largest_num]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
