"""
Given two strings A and B of lowercase letters, return true if and only if we
can swap two letters in A so that the result equals B.

Examples:

>>> buddy_strings("ab", "ba")
True

>>> buddy_strings("ab", "ab")
False

>>> buddy_strings("aa", "aa")
True

>>> buddy_strings("aaaaaaabc", "aaaaaaacb")
True

>>> buddy_strings("", "aa")
False
"""

import unittest


def has_duplicates(string: str) -> bool:
    seen: set[str] = set()
    for char in string:
        if char in seen:
            return True
        else:
            seen.add(char)

    return False


def buddy_strings(a: str, b: str) -> bool:
    """
    Check if two strings can be equal after one string swaps a character pair.

    This was inspired by the Levenshtein distance implementation
    in 2025/july/21. I just considered the case where only swaps could be made
    and simplified the matrix to a 1D array.

    In the worst case, this has O(n) time complexity and O(n) space.
    """
    if len(a) != len(b):
        return False

    swap_indexes: list[int] = []
    for i, (ca, cb) in enumerate(zip(a, b)):
        if ca != cb:
            swap_indexes.append(i)
            if len(swap_indexes) > 2:
                return False

    if not swap_indexes:  # a and b are identical
        return has_duplicates(a)

    return (
        len(swap_indexes) == 2
        and a[swap_indexes[0]] == b[swap_indexes[1]]
        and a[swap_indexes[1]] == b[swap_indexes[0]]
    )


class Tests(unittest.TestCase):
    cases: list[tuple[str, str, bool]] = [
        ("", "", False),
        ("ab", "ba", True),
        ("ab", "ab", False),
        ("ab", "bc", False),
        ("aa", "aa", True),
        ("ab", "cd", False),
        ("abaca", "acaba", True),
        ("aaaaaaabc", "aaaaaaacb", True),
        ("", "aa", False),
    ]

    def test_all(self):
        for a, b, expected in self.cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertIs(expected, buddy_strings(a, b))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
