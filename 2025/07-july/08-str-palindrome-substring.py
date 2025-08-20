"""
A palindrome is a sequence of characters that reads the same backwards and
forwards. Given a string, s, find the longest palindromic substring in s.

Similar to yesterday, the takeaway is to think in terms of window functions. The
answer here was pretty simple, but it required exploring for a more complicated
solution (optimizing for checking palindromes that are longer than the
current longest palindrome).

Examples:

>>> longest_palindrome("banana")
'anana'

>>> longest_palindrome("million")
'illi'

>>> longest_palindrome("tracecars")
'racecar'
"""

import unittest


def longest_palindrome(s: str) -> str:
    """Find the longest substring that is a palindrome."""

    if len(s) < 2:
        return s

    start = end = len(s) - 1

    def expand_around_center(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1

        return left + 1, right - 1

    for center in range(len(s) - 1):
        left, right = expand_around_center(left=center - 1, right=center + 1)
        if right - left > end - start:
            start = left
            end = right

        left, right = expand_around_center(left=center, right=center + 1)
        if right - left > end - start:
            start = left
            end = right

    return s[start : end + 1]


class Tests(unittest.TestCase):
    cases: list[tuple[str, str]] = [
        ("", ""),
        ("x", "x"),
        ("tracecars", "racecar"),
        ("banana", "anana"),
        ("million", "illi"),
        ("porous", "oro"),
        ("oivanmklsmnmsoracecar", "racecar"),
    ]

    def test_all(self):
        for s, expected in self.cases:
            with self.subTest(s=s, expected=expected):
                self.assertEqual(expected, longest_palindrome(s))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
