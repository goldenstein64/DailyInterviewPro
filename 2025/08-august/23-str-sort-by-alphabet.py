"""
Given a list of words, and an arbitrary alphabetical order, verify that the
words are in order of the alphabetical order.

Examples:

>>> is_sorted(["abcd", "efgh"], "zyxwvutsrqponmlkjihgfedcba")
False

>>> is_sorted(["zyx", "zyxw", "zyxwy"], "zyxwvutsrqponmlkjihgfedcba")
True
"""

import unittest
from typing import cast
from collections.abc import Callable
from itertools import pairwise, dropwhile, product
from functools import partial


def are_words_ordered(order_map: dict[str, int], pair: tuple[str, str]) -> bool:
    a, b = pair
    zipped = zip((order_map[c] for c in a), (order_map[c] for c in b))
    compared = (False if ka > kb else True if ka < kb else None for ka, kb in zipped)
    dropped_none = dropwhile(lambda cmp: cmp is None, compared)
    return next(cast("dropwhile[bool]", dropped_none), len(a) <= len(b))


def is_sorted_func(words: list[str], order: str) -> bool:
    """
    Verify that `words` is in the given `order`. This uses a functional
    implementation.
    """
    order_map: dict[str, int] = {v: i for i, v in enumerate(order)}
    predicate = cast(
        Callable[[tuple[str, str]], bool], partial(are_words_ordered, order_map)
    )
    return all(map(predicate, pairwise(words)))


def is_sorted_iter(words: list[str], order: str) -> bool:
    """
    Verify that `words` is in the given `order`. This uses an for-loop
    implementation.
    """
    order_map: dict[str, int] = {v: i for i, v in enumerate(order)}
    for a, b in pairwise(words):
        for ca, cb in zip(a, b):
            ka, kb = order_map[ca], order_map[cb]
            if ka > kb:
                return False
            elif ka < kb:
                break

        if len(a) > len(b):
            return False

    return True


is_sorted = is_sorted_iter


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[str], str], bool]] = [
        is_sorted_func,
        is_sorted_iter,
    ]

    cases: list[tuple[list[str], str, bool]] = [
        ([], "", True),
        (["a"], "a", True),
        (["a", "a"], "a", True),
        (["a", "aa"], "a", True),
        (["aa", "a"], "a", False),
        (["a", "b"], "ab", True),
        (["a", "b"], "ba", False),
        (["a", "b", "c"], "abc", True),
        (["a", "b", "c"], "acb", False),
        (["a", "b", "c"], "cba", False),
        (["abcd", "efgh"], "zyxwvutsrqponmlkjihgfedcba", False),
        (["zyx", "zyxw", "zyxwy"], "zyxwvutsrqponmlkjihgfedcba", True),
    ]

    def test_all(self):
        for solution, (words, order, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(
                solution=sol, words=words, order=order, expected=expected
            ):
                self.assertEqual(expected, is_sorted_func(words, order))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
