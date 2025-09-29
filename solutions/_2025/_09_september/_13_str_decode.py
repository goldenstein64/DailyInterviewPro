"""
Given a string with a certain rule: `k[string]` should be expanded to `string` k
times. So for example, 3[abc] should be expanded to abcabcabc. Nested expansions
can happen, so 2[a2[b]c] should be expanded to abbcabbc.

Examples:

>>> decode_string("3[abc]")
'abcabcabc'
>>> decode_string("2[a2[b]c]")
'abbcabbc'
"""

from __future__ import annotations

from enum import Enum, auto
from dataclasses import dataclass, field
import unittest

# expr = (ALPHA+ | DIGIT+ "[" expr "]") expr?


class State(Enum):
    DIGIT = auto()
    LETTER = auto()


@dataclass
class RepeatEntry:
    times: int = 1
    strings: list[str] = field(default_factory=list[str])


def decode_string(string: str) -> str:
    repeat_stack: list[RepeatEntry] = [RepeatEntry()]
    digits: list[str] = []
    state: State = State.LETTER
    for c in string:
        match (state, c):
            case (State.DIGIT, "["):
                times = int("".join(digits))
                digits = []
                repeat_stack.append(RepeatEntry(times))
                state = State.LETTER
            case (State.LETTER, "["):
                raise ValueError("no string count")
            case (State.LETTER, "]"):
                if len(repeat_stack) < 2:
                    raise ValueError("not enough '['s")

                entry = repeat_stack.pop()
                substring: str = "".join(entry.strings) * entry.times
                repeat_stack[-1].strings.append(substring)
                state = State.LETTER
            case (_, digit) if digit.isdigit():
                digits.append(digit)
                state = State.DIGIT
            case (State.LETTER, alpha) if alpha.isalpha():
                repeat_stack[-1].strings.append(alpha)
            case _:
                raise ValueError(f"unknown combination ({state}, '{c}')")

    if len(repeat_stack) != 1:
        raise ValueError("too many '['s")

    return "".join(repeat_stack[-1].strings)


class Tests(unittest.TestCase):
    cases: list[tuple[str, str | Exception]] = [
        ("", ""),
        ("a", "a"),
        ("abc", "abc"),
        ("1[ab]", "ab"),
        ("2[ab]", "abab"),
        ("0[ab]", ""),
        ("10[]", ""),
        ("a2[b]c", "abbc"),
        ("a2[b2[c]d]e", "abccdbccde"),
        ("3[abc]", "abcabcabc"),
        ("2[a2[b]c]", "abbcabbc"),
        ("[a]", ValueError("no string count")),
        ("4[abc", ValueError("too many '['s")),
        ("a]", ValueError("not enough '['s")),
    ]

    def test_cases(self):
        for string, expected in self.cases:
            with self.subTest(string=string, expected=expected):
                if isinstance(expected, Exception):
                    with self.assertRaises(type(expected)) as exception:
                        decode_string(string)

                    self.assertEqual(expected.args, exception.exception.args)
                else:
                    self.assertEqual(expected, decode_string(string))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
