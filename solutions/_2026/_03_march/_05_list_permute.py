"""
You are given an array of integers. Return all the permutations of this array.

Example:

>>> sorted(permute_brute([1, 2, 3]))
[(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
"""

from collections.abc import Iterable

# This has been done before!
from solutions._2025._09_september._27_list_permute import (
    permute as _,
    permute_heap as _,
    permute_heap_rec as _,
)


def permute_brute[T](values: list[T]) -> Iterable[tuple[T, ...]]:
    if len(values) == 1:
        yield (values[0],)
        return

    for i, v in enumerate(values):
        sub_values = values[:i] + values[i + 1 :]
        for t in permute_brute(sub_values):
            yield (v, *t)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
