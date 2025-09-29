"""
Two words can be 'chained' if the last character of the first word is the same
as the first character of the second word.

Given a list of words, determine if there is a way to 'chain' all the words in a
cycle.

Example:

>>> chained_words(['eggs', 'karat', 'apple', 'snack', 'tuna'])
True

A valid cycle exists, `['apple', 'eggs', 'snack', 'karat', 'tuna']`
"""

from collections import defaultdict, Counter
from collections.abc import Callable
from itertools import product
import unittest


def chained_words(words: list[str]) -> bool:
    """
    Determine whether every word in `words` can be chained into one cycle. This
    uses a brute-force algorithm that checks whether all words would be seen
    when iterating through `words` once.

    This has around O(n^2) time complexity and O(n) space.
    """
    sorted_words = sorted(words)
    reverse_map2: defaultdict[str, set[int]] = defaultdict(set)
    for i, v in enumerate(sorted_words):
        reverse_map2[v[0]].add(i)

    indexes: set[int] = reverse_map2[sorted_words[0][-1]]
    seen: set[int] = indexes
    for _ in range(len(reverse_map2)):
        new_indexes: set[int] = set()
        for i in indexes:
            new_indexes |= reverse_map2[sorted_words[i][-1]]
        indexes = new_indexes
        seen |= indexes

    return len(seen) == len(words)


def chained_words_eulerian(words: list[str]) -> bool:
    """
    A solution suggested by ChatGPT using the concept of Eulerian cycles.

    This roughly has O(n) time complexity and O(1) space.
    """
    in_degree: Counter[str] = Counter()
    out_degree: Counter[str] = Counter()
    adjacent: defaultdict[str, set[str]] = defaultdict(set)
    for word in words:
        start, end = word[0], word[-1]
        in_degree[start] += 1
        out_degree[end] += 1
        adjacent[start].add(end)
        adjacent[end].add(start)

    if in_degree != out_degree:
        return False

    visited: set[str] = set()
    stack: list[str] = [next(iter(adjacent))]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        stack.extend(adjacent[u] - visited)

    active = {c for c in adjacent if in_degree[c] or out_degree[c]}
    return visited >= active


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[str]], bool]] = [
        chained_words,
        chained_words_eulerian,
    ]

    cases: list[tuple[list[str], bool]] = [
        (["eggs", "karat", "apple", "snack", "tuna"], True),
        (["level", "shall", "tools", "lariat"], True),
        (["racecar"], True),
        (["racecar", "shares"], False),
        (["racecar", "rarer"], True),
        (["racecer", "rerar"], True),
        (["ab", "bc", "de", "ef"], False),
        (["ab", "cd", "ef", "gh"], False),
        (["ab", "ba", "cd", "dc"], False),
    ]

    def test_cases(self):
        for solution, (words, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, words=words, expected=expected):
                self.assertEqual(expected, solution(words))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
