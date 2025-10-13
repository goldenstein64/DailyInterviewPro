"""
Version numbers are strings that are used to identify unique states of software
products. A version number is in the format a.b.c.d. and so on where a, b, etc.
are numeric strings separated by dots. These generally represent a hierarchy
from major to minor changes. Given two version numbers version1 and version2,
conclude which is the latest version number. Your code should do the following:

If version1 > version2 return 1.
If version1 < version2 return -1.
Otherwise return 0.

Note that the numeric strings such as a, b, c, d, etc. may have leading zeroes,
and that the version strings do not start or end with dots. Unspecified level
revision numbers default to 0.

Examples:

>>> compare_version("1.0.33", "1.0.27")
1

>>> compare_version("0.1", "1.1")
-1

>>> compare_version("1.01", "1.001")
0

>>> compare_version("1.0", "1.0.0")
0
"""

import unittest
from itertools import repeat
from typing import Literal


type Comparison = Literal[-1, 0, 1]


def compare_version(version1: str, version2: str) -> Comparison:
    """
    Compare version strings consisting of only digits and dots. This uses a
    naive algorithm that turns the version numbers into lists, extends them to
    equal length by padding with zeroes, and using list comparison on them.

    This uses O(m + n) time and O(m + n) space, where m = len(version1) and
    n = len(version2).
    """

    if not version1 and not version2:
        return 0
    elif not version1:
        return -1
    elif not version2:
        return 1

    # turn them into lists of ints, e.g. "1.0.0" -> [1, 0, 0]
    ver1: list[int] = list(map(int, version1.split(".")))
    ver2: list[int] = list(map(int, version2.split(".")))

    # extend them to equal length
    len_ver1: int = len(ver1)
    len_ver2: int = len(ver2)
    if len_ver1 < len_ver2:
        ver1.extend(repeat(0, len_ver2 - len_ver1))
    elif len_ver1 > len_ver2:
        ver2.extend(repeat(0, len_ver1 - len_ver2))

    if ver1 < ver2:
        return -1
    elif ver1 > ver2:
        return 1
    else:
        return 0


class Tests(unittest.TestCase):
    cases: list[tuple[str, str, Comparison]] = [
        ("", "", 0),
        ("1", "", 1),
        ("", "1", -1),
        ("1", "1", 0),
        ("2", "1", 1),
        ("1", "2", -1),
        ("1.0.33", "1.0.27", 1),
        ("0.1", "1.1", -1),
        ("1.1", "1.-1", 1),
        ("1.01", "1.001", 0),
        ("1.0", "1.0.0", 0),
    ]

    def test_cases(self):
        for version1, version2, expected in self.cases:
            with self.subTest(version1=version1, version2=version2, expected=expected):
                self.assertEqual(expected, compare_version(version1, version2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
