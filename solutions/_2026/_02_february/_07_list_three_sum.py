"""
Given an array of numbers, determine whether it can be partitioned into 3 arrays
of equal sums.

Example:

>>> # [0, 2, 1] == [-6, 6, -7, 9, 1] == [2, 0, 1]
>>> has_three_equal_sums([0, 2, 1, -6, 6, -7, 9, 1, 2, 0, 1])
True

>>> # [] == [] == []
>>> has_three_equal_sums([])
True

>>> # [3, -3] == [1, -1] == []
>>> has_three_equal_sums([3, -3, 1, -1])
True

>>> has_three_equal_sums([3, 4, 5, 6])
False

>>> # [3, -4] == [5, -6] == [-1]
>>> has_three_equal_sums([3, -4, 5, -6, -1])
True
"""

from itertools import accumulate


def has_three_equal_sums(nums: list[int]) -> bool:
    total: int = sum(nums)
    if total % 3 != 0:
        return False

    target: int = total // 3
    target_count: int = 1
    for rolling_sum in accumulate(nums):
        if rolling_sum != target_count * target:
            continue

        target_count += 1
        if target_count == 3:
            return True

    return total == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
