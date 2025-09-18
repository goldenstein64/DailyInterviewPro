"""
Given a list of numbers of size n, where n is greater than 3, find the maximum
and minimum of the list using less than 2 * (n - 1) comparisons.

Example:

>>> min_max([3, 5, 1, 2, 4, 8])
(1, 8)
"""

from heapq import heappush


def min_max_sorted(nums: list[int]) -> tuple[int, int] | None:
    """
    Get the smallest and largest element of a list. This is a naive
    implementation that sorts the list and gets the minimum and maximum
    from it.
    """
    if len(nums) == 0:
        return None
    elif len(nums) == 1:
        return (nums[0], nums[0])

    sort = sorted(nums)
    return (sort[0], sort[-1])


def min_max(nums: list[int]) -> tuple[int, int] | None:
    """
    Get the smallest and largest element of a list, optimizing for number of
    comparisons. This tries to use two heaps to keep track of minimums and
    maximums, which should reduce comparison count to about `2 log n`. However,
    my calculation is wrong, as it's `2 log n` _per element_, which totals
    `2 n log n` comparisons.
    """
    if len(nums) == 0:
        return None
    elif len(nums) == 1:
        return (nums[0], nums[0])

    min_heap: list[int] = []
    max_heap: list[int] = []

    for num in nums:
        heappush(min_heap, num)
        heappush(max_heap, -num)

    return (min_heap[0], -max_heap[0])


def min_max_pairs(nums: list[int]) -> tuple[int, int] | None:
    """
    Get the smallest and largest element of a list, optimizing for number of
    comparisons. This uses an implementation suggested by ChatGPT, where
    elements are compared in pairs, totaling about `3n/2` comparisons.
    """
    if len(nums) == 0:
        return None
    elif len(nums) == 1:
        return (nums[0], nums[0])

    it = iter(nums)
    first: int = next(it)
    second: int = next(it)

    min_val: int
    max_val: int
    if first < second:
        min_val, max_val = first, second
    else:
        min_val, max_val = second, first

    for v1, v2 in zip(it, it):
        if v1 < v2:
            min_val = min(min_val, v1)
            max_val = max(max_val, v2)
        else:
            min_val = min(min_val, v2)
            max_val = max(max_val, v1)

    for v in it:
        min_val = min(min_val, v)
        max_val = max(max_val, v)

    return (min_val, max_val)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
