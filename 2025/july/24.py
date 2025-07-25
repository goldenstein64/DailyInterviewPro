"""
You are given a 2D array of characters, and a target string. Return whether or
not the word target word exists in the matrix. Unlike a standard word search,
the word must be either going left-to-right, or top-to-bottom in the matrix.

Example:

    [['F', 'A', 'C', 'I'],
     ['O', 'B', 'Q', 'P'],
     ['A', 'N', 'O', 'B'],
     ['M', 'A', 'S', 'S']]

    Given this matrix, and the target word `FOAM`, you should return true, as it
    can be found going up-to-down in the first column.
"""

import unittest
from itertools import product, chain
from typing import Generator


def word_search_down(matrix: list[list[str]], word: str, i: int, j: int) -> bool:
    return len(word) + i <= len(matrix) and all(
        matrix[i + k][j] == word[k] for k in range(len(word))
    )


def word_search_right(matrix: list[list[str]], word: str, i: int, j: int) -> bool:
    return len(word) + j <= len(matrix[0]) and all(
        matrix[i][j + k] == word[k] for k in range(len(word))
    )


def word_search_point(matrix: list[list[str]], word: str, i: int, j: int) -> bool:
    return word_search_down(matrix, word, i, j) or word_search_right(matrix, word, i, j)


def word_search(matrix: list[list[str]], word: str) -> bool:
    """naive implementation"""
    if word == "":
        return True

    if len(matrix) <= 0:
        return False

    # horizontal search first
    for i, j in product(range(len(matrix)), range(len(matrix[0]))):
        if word_search_point(matrix, word, i, j):
            return True

    return False


def word_search_gpt(matrix: list[list[str]], word: str) -> bool:
    """
    an implementation given to me by ChatGPT. I was told (by ChatGPT) that it's
    faster in practice because it uses Python's built-in substring search
    algorithm
    """
    if word == "":
        return True
    elif len(matrix) <= 0:
        return False

    rows: Generator[str] = ("".join(row) for row in matrix)
    columns: Generator[str] = ("".join(column) for column in zip(*matrix))
    return any(word in line for line in chain(rows, columns))


class Tests(unittest.TestCase):
    matrices: dict[str, list[list[str]]] = {
        "empty": [],
        "matrix": [
            ["F", "A", "C", "I"],
            ["O", "B", "Q", "P"],
            ["A", "N", "O", "B"],
            ["M", "A", "S", "S"],
        ],
    }

    cases: list[tuple[str, str, bool]] = [
        ("empty", "", True),
        ("matrix", "", True),
        ("matrix", "A", True),
        ("matrix", "AM", True),
        ("matrix", "NO", True),
        ("matrix", "NOB", True),
        ("matrix", "NOB", True),
        ("matrix", "FOAM", True),
        ("matrix", "MASS", True),
        ("matrix", "FRET", False),
        ("matrix", "SHUN", False),
        ("matrix", "IFRIT", False),
        ("matrix", "FACIT", False),
    ]

    def test_all(self):
        for solution in (word_search, word_search_gpt):
            for mat_key, word, expected in self.cases:
                with self.subTest(
                    solution=solution.__name__, matrix=mat_key, word=word
                ):
                    matrix = self.matrices[mat_key]
                    self.assertEqual(expected, solution(matrix, word))


if __name__ == "__main__":
    unittest.main()
