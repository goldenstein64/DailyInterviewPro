"""
Given a string, you need to reverse the order of characters in each word within
a sentence while still preserving whitespace and initial word order.

Note: In the string, each word is separated by a single space and there will not
be any extra space in the string.

Example:
>>> reverse_words("The cat in the hat")
'ehT tac ni eht tah'
"""

import unittest


def reverse_words(string: str) -> str:
    """Reverse each word in a given string."""
    words = string.split()
    rev_word_iters = map(reversed, words)
    rev_words = map("".join, rev_word_iters)
    return " ".join(rev_words)


class Tests(unittest.TestCase):
    cases: list[tuple[str, str]] = [
        ("", ""),
        ("a", "a"),
        ("ab", "ba"),
        ("a b", "a b"),
        ("abcd", "dcba"),
        ("ab cd", "ba dc"),
        ("change", "egnahc"),
        ("into change", "otni egnahc"),
        ("The cat in the hat", "ehT tac ni eht tah"),
    ]

    def test_cases(self):
        for string, expected in self.cases:
            with self.subTest(string=string, expected=expected):
                self.assertEqual(expected, reverse_words(string))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
