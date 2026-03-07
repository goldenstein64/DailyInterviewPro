"""
You are given a list of n numbers, where every number is at most k indexes away
from its properly sorted index. Write a sorting algorithm (that will be given
the number k) for this list that can solve this in O(n log k).

Example:

>>> list(partial_sorted([3, 2, 6, 5, 4], k=2))
[2, 3, 4, 5, 6]
"""

from heapq import heappush, heappushpop, heappop
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison

# This has been done before!
from solutions._2025._10_october._21_list_partial_sort import (
    partial_sorted as partial_sorted_old,
)


def partial_sorted[T: SupportsRichComparison](nums: list[T], k: int) -> Iterable[T]:
    heap: list[T] = []
    for num in nums:
        if len(heap) < k:
            heappush(heap, num)
        else:
            yield heappushpop(heap, num)

    while heap:
        yield heappop(heap)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    partial_sorted = partial_sorted_old
    doctest.testmod()
