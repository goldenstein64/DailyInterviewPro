"""
You are given a string of parentheses. Return the minimum number of parentheses
that would need to be removed in order to make the string valid. "Valid" means
that each open parenthesis has a matching closed parenthesis.

Example:

>>> count_invalid_parentheses("()())()")
1

>>> count_invalid_parentheses(")(")
2
"""

import unittest


def count_invalid_parentheses(string: str) -> int:
    paren_count: int = 0
    invalid_count: int = 0
    for c in string:
        match c:
            case "(":
                paren_count += 1
            case ")":
                if paren_count > 0:
                    paren_count -= 1
                else:
                    invalid_count += 1
            case _:
                raise ValueError("string must only contain '(' and ')'")

    return invalid_count + paren_count


class Tests(unittest.TestCase):
    cases: list[tuple[str, int]] = [
        ("", 0),
        ("(", 1),
        (")", 1),
        ("()", 0),
        (")(", 2),
        ("())", 1),
        ("(()", 1),
        ("(())", 0),
        ("()()", 0),
        ("()())()", 1),
    ]

    def test_cases(self):
        for string, expected in self.cases:
            with self.subTest(string=string, expected=expected):
                self.assertEqual(expected, count_invalid_parentheses(string))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
