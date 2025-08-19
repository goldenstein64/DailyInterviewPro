"""
You are given a string s, and an integer k. Return the length of the longest
substring in s that contains at most k distinct characters.

Example:
    Input: ("aabcdefff", 3)
    Output: 5
    Because the longest substring with 3 distinct characters is "defff"
"""

import unittest
from collections import Counter


def longest_k_distinct(s: str, k: int) -> int:
    """
    Find the longest substring in s with at most k distinct characters.

    This has O(len(s)) time complexity and O(k) space. This uses the sliding
    window method to complete in linear time.
    """
    if k == 0:
        return 0
    elif k >= len(s):
        return len(s)

    counter: Counter[str] = Counter()
    max_len: int = 0
    i: int = 0  # represents s[i:(j + 1)]
    for j, ch in enumerate(s):
        counter[ch] += 1
        while len(counter) > k:
            if counter[s[i]] == 1:
                del counter[s[i]]
            else:
                counter[s[i]] -= 1
            i += 1

        max_len = max(max_len, j - i + 1)

    return max_len


class Tests(unittest.TestCase):
    cases: list[tuple[str, int, int]] = [
        # simple cases
        ("", 0, 0),  # ""
        ("", 3, 0),  # ""
        ("a", 1, 1),  # a
        ("aa", 1, 2),  # aa
        ("aab", 1, 2),  # aa
        ("abb", 1, 2),  # bb
        ("abbcc", 2, 4),  # bbcc
        ("aabbc", 2, 4),  # aabb
        # interleaving repeats
        ("abacbabb", 2, 4),  # babb
        ("abcabcabc", 2, 2),  # ab or bc or ca
        ("abaccc", 2, 4),  # accc
        ("aaabbbccc", 2, 6),  # aaabbb or bbbccc
        # edge interleaving near boundaries
        ("aabbaaccc", 2, 6),  # aabbaa
        ("aabbaacc", 3, 8),  # aabbaacc
        # "aabccdeeeffg"
        ("aabccdeeeffg", 0, 0),  # ""
        ("aabccdeeeffg", 1, 3),  # eee
        ("aabccdeeeffg", 2, 5),  # eeeff
        ("aabccdeeeffg", 3, 6),  # deeeff or eeeffg
        ("aabccdeeeffg", 4, 8),  # ccdeeeff
        ("aabccdeeeffg", 5, 9),  # bccdeeeff or ccdeeeffg
        ("aabccdeeeffg", 6, 11),  # aabccdeeeffg
        # example case, "aabcdefff"
        ("aabcdefff", 0, 0),  # ""
        ("aabcdefff", 1, 3),  # fff
        ("aabcdefff", 2, 4),  # efff
        ("aabcdefff", 3, 5),  # defff
        ("aabcdefff", 4, 6),  # cdefff
        ("aabcdefff", 5, 7),  # bcdefff
        ("aabcdefff", 6, 9),  # aabcdefff
        ("aabcdefff", 9, 9),  # aabcdefff
    ]

    def test_all(self):
        for s, k, expected in self.cases:
            with self.subTest(s=s, k=k, expected=expected):
                self.assertEqual(expected, longest_k_distinct(s, k))


if __name__ == "__main__":
    unittest.main()
