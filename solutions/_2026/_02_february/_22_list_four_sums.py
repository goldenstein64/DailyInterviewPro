"""
Given a list of numbers, and a target number n, find all unique combinations of
a, b, c, d, such that a + b + c + d = n.

Examples:

>>> four_sum([1, 1, -1, 0, -2, 1, -1], 0) == {(-1, -1, 1, 1), (-2, 0, 1, 1)}
True

>>> four_sum([3, 0, 1, -5, 4, 0, -1], 1) == {(-5, -1, 3, 4)}
True

>>> four_sum([0, 0, 0, 0, 0], 0) == {(0, 0, 0, 0)}
True
"""

from itertools import combinations
from typing import cast

type Quadruple = tuple[int, int, int, int]

# this has been done before!
from solutions._2026._01_january._08_list_four_sums import four_sum as four_sum_old


def four_sum_old_wrapper(nums: list[int], target: int) -> set[Quadruple]:
    result: list[list[int]] = four_sum_old(nums, target)
    assert all(len(quad) == 4 for quad in result)
    return {cast(Quadruple, tuple(sorted(quad))) for quad in result}


def four_sum(nums: list[int], target: int) -> set[Quadruple]:
    result: set[Quadruple] = set()
    for tup in combinations(nums, 4):
        if sum(tup) == target:
            result.add(cast(Quadruple, tuple(sorted(tup))))

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    four_sum = four_sum_old_wrapper
    doctest.testmod()
