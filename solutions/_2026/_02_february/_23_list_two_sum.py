"""
You are given a list of numbers, and a target number k. Return whether or not
there are two numbers in the list that add up to k.

Example:

>>> two_sum([4,7,1,-3,2], 5)
True
"""

# this has been done before!
from solutions._2025._07_july._13_list_two_sum import two_sum as two_sum_old


def two_sum(ls: list[int], k: int) -> bool:
    seen: set[int] = set()
    for num in ls:
        if num in seen:
            return True
        else:
            seen.add(k - num)

    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    two_sum = two_sum_old
    doctest.testmod()
