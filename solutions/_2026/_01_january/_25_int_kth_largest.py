"""
Find the k-th largest number in a sequence of unsorted numbers.

Example:

>>> find_kth_largest([8, 7, 2, 3, 4, 1, 5, 6, 9, 0], 3)
7
"""

from heapq import heapify, heappop


def find_kth_largest(nums: list[int], k: int) -> int:
    if len(nums) < k:
        raise ValueError("length of list must be at least as large as k")
    elif k == 1:
        return max(nums)

    heap: list[int] = [-num for num in nums]
    heapify(heap)
    result: int | None = None
    for _ in range(k):
        result = heappop(heap)

    if result is None:
        # this should be unreachable
        raise ValueError("could not find kth largest number")

    return -result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
