"""
A look-and-say sequence is defined as the integer sequence beginning with a
single digit in which the next term is obtained by describing the previous term.
An example is easier to understand:

Each consecutive value describes the prior value.

1      # one 1
11     # two 1s
21     # one 2 and one 1
1211   # one 1, one 2, and two 1s
111221 #
"""

from itertools import islice, chain, product
import unittest
import re
from typing import Callable

_repeating = re.compile(r"(.)\1*")


def look_and_say_regex(n: int) -> str:
    """
    Retrieve the nth term of the look-and-say sequence, starting with a seed of
    1. This uses RegEx to find sets of repeating characters
    """
    if n == 1:
        return "1"

    last_n: str = look_and_say_regex(n - 1)
    gen = ((str(len(match[0])), match[1]) for match in _repeating.finditer(last_n))
    return "".join(chain.from_iterable(gen))


def look_and_say(n: int) -> str:
    """
    Retrieve the nth term of the look-and-say sequence, starting with a seed of
    1.
    """
    if n == 1:
        return "1"

    last_n: str = look_and_say(n - 1)
    last_count = 1
    last_c = last_n[0]
    result: list[str] = []
    for c in islice(last_n, 1, len(last_n)):
        if c == last_c:
            last_count += 1
        else:
            result.append(str(last_count))
            result.append(last_c)
            last_count = 1
            last_c = c

    result.append(str(last_count))
    result.append(last_c)

    return "".join(result)


def look_and_say_int(n: int) -> int:
    """
    Retrieve the nth term of the look-and-say sequence, starting with a seed of
    1. This computes the result iteratively and stores the result in an integer
    to save on space.
    """
    result: int = 1
    for _ in range(n - 1):
        sub_result: int = 0
        total_count: int = 0
        last_count: int = 1
        last_digit: int = result % 10
        result //= 10
        while result >= 1:
            digit: int = result % 10
            if digit == last_digit:
                last_count += 1
            else:
                sub_result += (last_count * 10 + last_digit) * 10**total_count
                last_count = 1
                last_digit = digit
                total_count += 2
            result //= 10

        sub_result += (last_count * 10 + last_digit) * 10**total_count
        result = sub_result

    return result


def look_and_say_base4(n: int) -> int:
    """
    Retrieve the nth term of the look-and-say sequence, starting with a seed of
    1. This computes the result iteratively and stores the result in a base-4 integer
    to save on space.

    Usage of base-4 is dependent on the fact that any term of the look-and-say
    sequence is composed solely of the digits 1, 2, and 4.
    """

    # perform the actual calculation in base-4
    base4_result: int = 1
    for _ in range(n - 1):
        sub_result: int = 0
        sub_length: int = 0
        last_count: int = 1
        last_digit: int = base4_result % 4
        base4_result //= 4
        while base4_result >= 1:
            digit: int = base4_result % 4
            if digit == last_digit:
                last_count += 1
            else:
                sub_result += (last_count * 4 + last_digit) * 4**sub_length
                last_count = 1
                last_digit = digit
                sub_length += 2
            base4_result //= 4

        sub_result += (last_count * 4 + last_digit) * 4**sub_length
        base4_result = sub_result

    # expand the result into base-10 after the computation is finished
    result = 0
    length = 0
    while base4_result >= 1:
        digit = base4_result % 4
        result += digit * 10**length
        length += 1
        base4_result //= 4

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[int], str]] = [
        look_and_say,
        look_and_say_regex,
        lambda n: str(look_and_say_int(n)),
        lambda n: str(look_and_say_base4(n)),
    ]

    cases: list[tuple[int, str]] = [
        # (1, "1"),
        (2, "11"),
        # (3, "21"),
        # (4, "1211"),
        # (5, "111221"),
        # (6, "312211"),
    ]

    def test_all(self):
        for solution, (n, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, n=n, expected=expected):
                self.assertEqual(expected, solution(n))


if __name__ == "__main__":
    unittest.main()
