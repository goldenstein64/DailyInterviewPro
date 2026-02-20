"""
Given an array of integers, return the length of the longest increasing
subsequence (not necessarily contiguous) in the array.

Example:

>>> longest_increasing([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])
6
"""

import unittest

# This was done before!
from solutions._2025._09_september._04_list_longest_increasing import (
    longest_increasing_patience as longest_increasing_old,
    Tests as _,
)


if __name__ == "__main__":
    import doctest

    longest_increasing = longest_increasing_old
    doctest.testmod()
    unittest.main()
