"""
Imagine you are building a compiler. Before running any code, the compiler must
check that the parentheses in the program are balanced. Every opening bracket
must have a corresponding closing bracket. We can approximate this using
strings.

Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
- Open brackets are closed by the same type of brackets.
- Open brackets are closed in the correct order.
- Note that an empty string is also considered valid.

Examples:

>>> is_valid("((()))")
True

>>> is_valid("[()]{}")
True

>>> is_valid("({[)]")
False
"""

import unittest


def is_valid(s: str) -> bool:
    """
    Determine whether all parentheses in a string made up of the characters
    '()[]{}' are properly balanced.
    """
    brackets: list[str] = []
    for char in s:
        check: str
        match char:
            case ")":
                check = "("
            case "]":
                check = "["
            case "}":
                check = "{"
            case "(" | "[" | "{":
                brackets.append(char)
                continue
            case _:
                continue

        if len(brackets) == 0 or brackets.pop() != check:
            return False

    return len(brackets) == 0


class Tests(unittest.TestCase):
    cases: list[tuple[str, bool]] = [
        ("", True),
        ("(", False),
        (")", False),
        ("({})[", False),
        (")(", False),
        ("((()))", True),
        ("[()]{}", True),
        ("({[)]", False),
        ("()(){(())", False),
        ("([{}])()", True),
    ]

    def test_cases(self):
        for s, expected in self.cases:
            with self.subTest(s=s, expected=expected):
                self.assertEqual(expected, is_valid(s))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
