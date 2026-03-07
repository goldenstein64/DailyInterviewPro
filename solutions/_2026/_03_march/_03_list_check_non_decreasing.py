"""
You are given an array of integers in an arbitrary order. Return whether or not
it is possible to make the array non-decreasing by modifying at most 1 element to any value.

We define an array is non-decreasing if array[i] <= array[i + 1] holds for every
i (1 <= i < n).

Can you find a solution in O(n) time?

Examples:

>>> # true, since we can modify 13 to any value 4 or less
>>> check_non_decreasing([13, 4, 7])
True

>>> # false, since there is no way to modify just one element to make the array
>>> # non-decreasing
>>> check_non_decreasing([13, 4, 1])
False
"""


def check_non_decreasing(ls: list[int]) -> bool:
    changed: bool = True
    for i in range(len(ls) - 1):
        if ls[i] <= ls[i + 1]:  # nothing wrong
            continue

        if changed:
            return False

        if i == 0 or ls[i - 1] <= ls[i + 1]:
            ls[i] = ls[i + 1]
        else:  # i != 0 and ls[i - 1] > ls[i + 1]
            ls[i + 1] = ls[i]

        changed = True

    return True
