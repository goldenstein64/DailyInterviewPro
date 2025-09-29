"""
Given a string, find the length of the longest substring without repeating
characters.

The takeaway from this is to think of substrings as "window functions" over a
string. You should think about how the substring should expand or contract while
giving you the answer you need.

Example:

>>> gpt_length_of_longest_substring_dict("abrkaabcdefghijjxxx")
10
"""

import unittest
from collections.abc import Callable
from itertools import product


def length_of_longest_substring(s: str) -> int:
    """
    Find the length of the longest substring with unique characters. This is
    incorrect for strings like `dvdfd`.
    """
    longest: int = 1
    longest_set: set[str] = set()

    for sub in s:
        if sub in longest_set:
            longest = max(longest, len(longest_set))
            longest_set.clear()

        longest_set.add(sub)

    longest = max(longest, len(longest_set))
    longest_set.clear()

    for sub in reversed(s):
        if sub in longest_set:
            longest = max(longest, len(longest_set))
            longest_set.clear()

        longest_set.add(sub)

    longest = max(longest, len(longest_set))

    return longest


def gpt_length_of_longest_substring_set(s: str) -> int:
    """
    I asked ChatGPT about this and it gave me this answer.
    """
    seen: set[str] = set()
    left: int = 0
    max_len: int = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len


def gpt_length_of_longest_substring_dict(s: str) -> int:
    """
    ChatGPT also made this more optimized answer.
    """
    last_seen: dict[str, int] = {}
    left: int = 0
    max_len: int = 0

    for right, char in enumerate(s):
        while char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len


class Tests(unittest.TestCase):
    solutions: list[Callable[[str], int]] = [
        # length_of_longest_substring,
        gpt_length_of_longest_substring_set,
        gpt_length_of_longest_substring_dict,
    ]

    cases: tuple[tuple[str, int], ...] = (
        ("dvdfd", 3),
        ("vdfd", 3),
        ("abrkaabcdefghijjxxx", 10),
    )

    def test_cases(self):
        for solution, (s, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, s=s, expected=expected):
                self.assertEqual(expected, solution(s))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
