"""
Given a list of words, group the words that are anagrams of each other.
(Anagrams are words made up of the same letters).

Example:

>>> groups = group_anagram_words(['abc', 'bcd', 'cba', 'cbd', 'efg'])
>>> type(groups) == list
True
>>> all(type(group) == list for group in groups)
True
>>> sorted(map(sorted, groups))
[['abc', 'cba'], ['bcd', 'cbd'], ['efg']]
"""

import unittest
from collections import Counter, defaultdict
from collections.abc import Callable
from itertools import product

_alphabet = "".join(map(chr, range(97, 123)))


def group_anagram_words(words: list[str]) -> list[list[str]]:
    """
    First instinct, use sorted(word) as the key and map them to a set.

    This has O(nk log k) time complexity and O(nk) space.
    """
    groups: defaultdict[str, set[str]] = defaultdict(set)
    for word in words:
        key = "".join(sorted(word))
        groups[key].add(word)

    return list(map(list, groups.values()))


def group_anagram_words_freq(words: list[str]) -> list[list[str]]:
    """
    A performance gain proposed by ChatGPT: use letter frequencies as the
    anagram key instead of simple sorting.
    """
    groups: defaultdict[tuple[tuple[str, int], ...], set[str]] = defaultdict(set)
    for word in words:
        key = tuple(sorted(Counter(word).items()))
        groups[key].add(word)

    return list(map(list, groups.values()))


def group_anagram_words_fixed_freq(words: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], set[str]] = defaultdict(set)
    for word in words:
        key = tuple(map(word.count, _alphabet))
        groups[key].add(word)

    return list(map(list, groups.values()))


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[str]], list[list[str]]]] = [
        group_anagram_words,
        group_anagram_words_freq,
    ]

    cases: list[tuple[list[str], list[list[str]]]] = [
        ([], []),
        (["a"], [["a"]]),
        (["a", "b"], [["a"], ["b"]]),
        (["a", "b", "ab"], [["a"], ["ab"], ["b"]]),
        (["a", "b", "ab", "ba"], [["a"], ["ab", "ba"], ["b"]]),
        (
            ["abc", "bcd", "cba", "cbd", "efg"],
            [["abc", "cba"], ["bcd", "cbd"], ["efg"]],
        ),
    ]

    def test_cases(self):
        for solution, (words, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, words=words, expected=expected):
                groups = solution(words)
                self.assertEqual(expected, sorted(map(sorted, groups)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
