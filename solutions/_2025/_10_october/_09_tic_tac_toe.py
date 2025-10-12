"""
Design a Tic-Tac-Toe game played between two players on an n x n grid. A move is
guaranteed to be valid, and a valid move is one placed on an empty block in the
grid. A player who succeeds in placing n of their marks in a horizontal,
diagonal, or vertical row wins the game. Once a winning condition is reached,
the game ends and no more moves are allowed. Below is an example game which ends
in a winning condition:

>>> board = TicTacToe(3)
>>> print(board.move(0, 0, "X"))
|X| | |
| | | |
| | | |
>>> print(board.move(0, 2, "O"))
|X| |O|
| | | |
| | | |
>>> print(board.move(2, 2, "X"))
|X| |O|
| | | |
| | |X|
>>> print(board.move(1, 1, "O"))
|X| |O|
| |O| |
| | |X|
>>> print(board.move(2, 0, "X"))
|X| |O|
| |O| |
|X| |X|
>>> print(board.move(1, 0, "O"))
|X| |O|
|O|O| |
|X| |X|
>>> print(board.move(2, 1, "X"))
|X| |O|
|O|O| |
|X|X|X|
>>> try:
...     board.move(0, 1, "O")
... except ValueError as e:
...     print(f"cannot make move: {e.args}")
cannot make move: ('board is finished',)

>>> board.won("X")
True
>>> board.won("O")
False
"""

from typing import Literal, Self
from itertools import batched
from dataclasses import dataclass

type Mark = Literal["X", "O"]


@dataclass
class EndedResult:
    winner: Mark | None


class TicTacToe:
    WIN_PATTERNS: list[tuple[int, int, int]] = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (1, 5, 9),
        (3, 5, 7),
    ]

    def __init__(self, n: int) -> None:
        self.n: int = n
        self.cells: list[Mark | None] = [None] * (n * n)
        self.ended: EndedResult | None = None

    def won(self, mark: Mark) -> bool:
        return any(
            all(self.cells[p] == mark for p in pattern)
            for pattern in TicTacToe.WIN_PATTERNS
        )

    def full(self) -> bool:
        return all(self.cells)

    def move(self, row: int, col: int, mark: Mark) -> Self:
        if self.ended:
            raise ValueError("board is finished")

        self.cells[row * self.n + col] = mark
        if self.won(mark):
            self.ended = EndedResult(winner=mark)
        elif self.full():
            self.ended = EndedResult(winner=None)
        return self

    def __str__(self) -> str:
        return "\n".join(
            f"|{"|".join(p or " " for p in row)}|"
            for row in batched(self.cells, self.n)
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
