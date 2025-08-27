"""
Given a 2-dimensional grid consisting of 1's (land blocks) and 0's (water
blocks), count the number of islands present in the grid. The definition of an
island is as follows:

- Must be surrounded by water blocks.
- Consists of land blocks (1's) connected to adjacent land blocks (either vertically or horizontally).

Assume all edges outside of the grid are water.

Examples:

>>> grid = matrix_of([
...     "10001",
...     "11000",
...     "10110",
...     "00000",
... ])
>>> num_islands(grid)
3

>>> grid = matrix_of([
...     "11000",
...     "01001",
...     "10011",
...     "00000",
... ])
>>> num_islands(grid)
3
"""

from itertools import count, islice
from enum import Enum
import unittest


class Block(Enum):
    LAND = 1
    WATER = 0


def matrix_of(strings: list[str]) -> list[list[Block]]:
    return [[Block(int(c)) for c in line] for line in strings]


def num_islands(grid: list[list[Block]]) -> int:
    """
    Calculate the number of islands on a grid. Islands are defined as groups of
    `Block.LAND`. Any land adjacent to each other are considered part of the
    same island.
    """
    if not grid:
        return 0

    labels = count(start=1)
    above: list[int] = []
    left_label: int = 0
    result: int = 0
    for block in grid[0]:
        match block:
            case Block.WATER:
                left_label = 0
            case Block.LAND:
                if left_label == 0:
                    left_label = next(labels)
                    result += 1
        above.append(left_label)

    for row in islice(grid, 1, len(grid)):
        left_label: int = 0
        for i, block in enumerate(row):
            match block:
                case Block.WATER:
                    above[i] = left_label = 0
                case Block.LAND:
                    match (left_label, above[i]):
                        case (0, 0):
                            above[i] = left_label = next(labels)
                            result += 1
                        case (0, top_label):
                            above[i] = left_label = top_label
                        case (left_label, 0):
                            above[i] = left_label
                        case (left_label, top_label):
                            if left_label != top_label:
                                # merge two masses together
                                result -= 1
                                above[i] = left_label = min(left_label, top_label)
                            else:
                                above[i] = left_label

    return result


class Tests(unittest.TestCase):
    cases: list[tuple[list[str], int]] = [
        ([], 0),
        ([""], 0),
        (["0"], 0),
        (["1"], 1),
        (["11"], 1),
        (["101"], 2),
        (["11", "11"], 1),
        (["01", "10"], 2),
        (["10", "01"], 2),
        (["101", "010", "101"], 5),
        (["101", "111"], 1),
        (["110", "011"], 1),
        (
            [
                "11",
                "01",
                "11",
                "10",
                "11",
            ],
            1,
        ),
        (["0101", "1111"], 1),
        (
            [
                "10001",
                "11000",
                "10110",
                "00000",
            ],
            3,
        ),
        (
            [
                "11000",
                "01001",
                "10011",
                "00000",
            ],
            3,
        ),
    ]

    def test_all(self):
        for grid, expected in self.cases:
            with self.subTest(grid=grid, expected=expected):
                self.assertEqual(expected, num_islands(matrix_of(grid)))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
