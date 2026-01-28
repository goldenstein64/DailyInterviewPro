"""
Find all words that are concatenations of a list.

Example:

>>> find_all_concatenated_words_in_a_dict(
...     ["tech", "lead", "techlead", "cat", "cats", "dog", "catsdog"]
... )
['techlead', 'catsdog']

>>> TrieSolution.find_all_concatenated_words_in_a_dict(
...     ["tech", "lead", "techlead", "cat", "cats", "dog", "catsdog"]
... )
['techlead', 'catsdog']

Note: This question is classified as "hard."
HINT: Start with a brute-force solution.
"""

from itertools import permutations
from collections import deque
from collections.abc import Iterable


def find_all_concatenated_words_in_a_dict(words: list[str]) -> list[str]:
    """
    Find all words in the list that are a concatenation of two other words in
    the list. This is just a brute-force algorithm.

    This uses O(n!) time and O(n!) space due to checking every permutation.
    """

    words_set: set[str] = set(words)
    result: list[str] = []
    for a, b in permutations(words, 2):
        if (word := a + b) in words_set:
            result.append(word)

    return result


class TrieNode:
    def __init__(self, words: Iterable[str] | None = None) -> None:
        self.children: list[TrieNode | None] = [None] * 26
        self.is_leaf: bool = False
        if words is not None:
            self.extend(words)

    @staticmethod
    def char_to_int(ch: str) -> int:
        return ord(ch) - ord("a")

    def insert(self, key: str) -> None:
        p_crawl: TrieNode | None = self
        for ch in key:
            index: int = TrieNode.char_to_int(ch)
            next_child: TrieNode | None = p_crawl.children[index]
            if not next_child:
                p_crawl.children[index] = next_child = TrieNode()

            p_crawl = next_child

        p_crawl.is_leaf = True

    def extend(self, keys: Iterable[str]) -> None:
        for key in keys:
            self.insert(key)


class TrieSolution:
    """
    This was taken from GeeksForGeeks.

    See: https://www.geeksforgeeks.org/dsa/word-formation-using-concatenation-of-two-dictionary-words
    """

    @staticmethod
    def find_prefix(root: TrieNode, key: str) -> int | None:
        pos: int | None = None
        p_crawl: TrieNode = root
        for i, ch in enumerate(key):
            index: int = TrieNode.char_to_int(ch)
            if p_crawl.is_leaf:
                pos = i

            next_child: TrieNode | None = p_crawl.children[index]
            if not next_child:
                return pos

            p_crawl = next_child

        return len(key)

    @staticmethod
    def is_possible(root: TrieNode, word: str) -> bool:
        len1: int | None = TrieSolution.find_prefix(root, word)
        if len1 is None or len1 == 0:
            return False

        split_word: str = word[len1:]
        len2: int | None = TrieSolution.find_prefix(root, split_word)

        return len2 is not None and len2 != 0 and len1 + len2 == len(word)

    @staticmethod
    def find_all_concatenated_words_in_a_dict(words: list[str]) -> list[str]:
        result: list[str] = []
        word_queue: deque[str] = deque(words)
        for _ in range(len(word_queue)):
            word: str = word_queue.popleft()
            root: TrieNode = TrieNode(word_queue)
            if TrieSolution.is_possible(root, word):
                result.append(word)

            word_queue.append(word)
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
