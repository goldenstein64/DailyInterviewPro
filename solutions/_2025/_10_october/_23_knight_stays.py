"""
A chess board is an 8x8 grid. Given a knight at any position (x, y) and a number
of moves k, we want to figure out after k random moves by a knight, the
probability that the knight will still be on the chessboard. Once the knight
leaves the board it cannot move again and will be considered off the board.

Example:

>>> knight_stays((0, 0), 1)
0.25

>>> knight_stays((0, 0), 3)
0.125
"""

from collections import Counter
from typing import Final
from itertools import product

moves: list[tuple[int, int]] = [
    (1, 2),
    (2, 1),
    (-1, 2),
    (2, -1),
    (1, -2),
    (-2, 1),
    (-1, -2),
    (-2, -1),
]

board_len: Final[range] = range(8)


def knight_stays(pos: tuple[int, int], k: int) -> float:
    x, y = pos
    if x not in board_len or y not in board_len:
        return 0

    valid_moves: Counter[tuple[int, int]] = Counter()
    valid_moves[pos] += 1
    for _ in range(k):
        new_valid_moves: Counter[tuple[int, int]] = Counter()
        for ((x, y), c), (u, v) in product(valid_moves.items(), moves):
            if x + u in board_len and y + v in board_len:
                new_valid_moves[(x + u, y + v)] += c

        valid_moves = new_valid_moves

    return sum(valid_moves.values()) / len(moves) ** k


if __name__ == "__main__":
    import doctest

    doctest.testmod()
