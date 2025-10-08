"""
Given a non-empty list of words, return the k most frequent words. The output
should be sorted from highest to lowest frequency, and if two words have the
same frequency, the word with lower alphabetical order comes first. Input will
contain only lower-case letters.

Example:

>>> words = [
...     "daily",
...     "interview",
...     "pro",
...     "pro",
...     "for",
...     "daily",
...     "pro",
...     "problems",
... ]
>>> k_most_common(words, k=2)
['pro', 'daily']
"""

from collections import Counter


def k_most_common(words: list[str], k: int) -> list[str]:
    """
    Find the `k` most common words in `words`. This just leverages the
    `Counter.most_common` method.

    This has O(n log k) time complexity and O(n + k) space, where k = min(n, k)
    """
    counter: Counter[str] = Counter(words)
    return [k for k, _ in counter.most_common(k)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
