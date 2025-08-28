"""
Given a string with the initial condition of dominoes, where:

. represents that the domino is standing still
L represents that the domino is falling to the left side
R represents that the domino is falling to the right side

Figure out the final position of the dominoes. If there are dominoes that get
pushed on both ends, the force cancels out and that domino remains upright.

Example:

>>> push_dominoes_loop("..R...L..R.")
'..RR.LL..RR'
"""

import re
import unittest
from itertools import product
from typing import Callable

push_left_once = re.compile(r"([^R])\.L")
push_right_once = re.compile(r"R\.([^L])")


def push_dominoes_once(dominoes: str) -> str:
    if dominoes.startswith(".L"):
        dominoes = "LL" + dominoes[2:]

    if dominoes.endswith("R."):
        dominoes = dominoes[:-2] + "RR"

    dominoes = dominoes.replace("R..L", "RRLL")
    dominoes = push_left_once.sub(r"\1LL", dominoes)
    dominoes = push_right_once.sub(r"RR\1", dominoes)
    return dominoes


def push_dominoes_loop(dominoes: str) -> str:
    """
    Determine the final position of a row of dominoes by simulating time
    steps.
    """
    old_dominoes = None
    while old_dominoes != dominoes:
        old_dominoes = dominoes
        dominoes = push_dominoes_once(dominoes)

    return dominoes


push_pairs = re.compile(r"R\.+L")
push_left_end = re.compile(r"^\.+L")
push_right_end = re.compile(r"R\.+$")
push_left = re.compile(r"L\.+L")
push_right = re.compile(r"R\.+R")


@staticmethod
def replace_pairs(match: re.Match[str]) -> str:
    old_str: str = match[0]
    push_len = len(old_str) // 2
    return "R" * push_len + "." * (len(old_str) % 2) + "L" * push_len


def push_dominoes_pairs(dominoes: str) -> str:
    """
    Determine the final position of a row of dominoes by applying a few
    rules in the form of RegEx replacements
    """
    dominoes = push_pairs.sub(replace_pairs, dominoes)
    dominoes = push_left_end.sub(lambda m: "L" * len(m[0]), dominoes)
    dominoes = push_right_end.sub(lambda m: "R" * len(m[0]), dominoes)
    dominoes = push_left.sub(lambda m: "L" * len(m[0]), dominoes)
    dominoes = push_right.sub(lambda m: "R" * len(m[0]), dominoes)
    return dominoes


def push_dominoes_force_accum(dominoes: str) -> str:
    """An implementation given to me by ChatGPT."""
    n = len(dominoes)
    forces: list[int] = [0] * n

    # rightward forces
    force: int = 0
    for i, c in enumerate(dominoes):
        force = n if c == "R" else 0 if c == "L" else max(force - 1, 0)
        forces[i] += force

    # leftward forces
    force: int = 0
    for i, c in reversed([*enumerate(dominoes)]):
        force = n if c == "L" else 0 if c == "R" else max(force - 1, 0)
        forces[i] -= force

    return "".join("R" if f > 0 else "L" if f < 0 else "." for f in forces)


class Tests(unittest.TestCase):
    solutions: list[Callable[[str], str]] = [
        push_dominoes_loop,
        push_dominoes_pairs,
        push_dominoes_force_accum,
    ]

    cases: list[tuple[str, str]] = [
        (".", "."),
        ("...", "..."),
        ("L.", "L."),
        (".L", "LL"),
        ("R.", "RR"),
        (".L.", "LL."),
        (".R.", ".RR"),
        ("RL", "RL"),
        ("R.L", "R.L"),
        ("R..L", "RRLL"),
        ("R...L", "RR.LL"),
        ("R....L", "RRRLLL"),
        ("R.....L", "RRR.LLL"),
        ("R......L", "RRRRLLLL"),
        ("R.......L", "RRRR.LLLL"),
        ("..R...L..R.", "..RR.LL..RR"),
        ("R...R...L", "RRRRRR.LL"),
        ("R.R.L", "RRR.L"),
        ("R.L.L", "R.LLL"),
    ]

    def test_cases(self):
        for solution, (dominoes, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, dominoes=dominoes, expected=expected):
                self.assertEqual(expected, solution(dominoes))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
