"""
Given a string, return the first recurring letter that appears. If there are no
recurring letters, return `None`.

Example:

>>> first_recurring_char("qwertty")
't'

>>> first_recurring_char("qwerty")  # no output

>>> first_recurring_char("abcdebg")
'b'
"""

import unittest


def first_recurring_char(s: str) -> str | None:
    chars: set[str] = set()
    for ch in s:
        if ch not in chars:
            chars.add(ch)
        else:
            return ch

    return None


class Tests(unittest.TestCase):
    cases: list[tuple[str, str | None]] = [
        ("qwertty", "t"),
        ("qwerty", None),
        ("abcdebg", "b"),
    ]

    def test_cases(self):
        for s, expected in self.cases:
            with self.subTest(s=s, expected=expected):
                self.assertEqual(expected, first_recurring_char(s))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
