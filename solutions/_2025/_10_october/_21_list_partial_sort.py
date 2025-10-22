"""
You are given a list of n numbers, where every number is at most k indexes away
from its properly sorted index. Write a sorting algorithm (that will be given
the number k) for this list that can solve this in `O(n log k)`

Example:

>>> partial_sorted([3, 2, 6, 5, 4], k=2)
[2, 3, 4, 5, 6]
"""

from typing import TYPE_CHECKING
from heapq import heappushpop, heappop, heapify

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


def partial_sorted[T: SupportsRichComparison](ls: list[T], k: int) -> list[T]:
    """
    Sort `ls`, a list whose elements are at most `k` indices away from their
    sorted position.

    This uses O(n log k) time and O(n + k) space.
    """
    # create a heap up to k + 1. Once it's filled, pop from the heap and push a
    # new value until the input and heap are exhausted.
    result: list[T] = []

    heap: list[T] = ls[: k + 1]
    heapify(heap)
    for v in ls[k + 1 :]:
        result.append(heappushpop(heap, v))

    while heap:
        result.append(heappop(heap))

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
