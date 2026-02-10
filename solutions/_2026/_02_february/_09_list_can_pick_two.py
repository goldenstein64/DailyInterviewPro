"""
Given an array containing only positive integers, return if you can pick two
integers from the array which cuts the array into three pieces such that the sum
of elements in all pieces is equal.

Example 1:

>>> # choosing the numbers 5 and 9 result in three pieces [2, 4], [3, 3] and
>>> # [2, 2, 2]. Sum = 6.
>>> can_pick_two([2, 4, 5, 3, 3, 9, 2, 2, 2])
True

>>> can_pick_two([1, 1, 1, 1])
False
>>> can_pick_two([1, 1, 1, 1, 1])
True
>>> can_pick_two([1, 1])
True
>>> can_pick_two([1, 200, 1, 400, 1])
True
>>> can_pick_two([1, 5, 9, 50, 3, 5, 7, 50, 2, 5, 8])
True
>>> # [1] * 10, [2] * 5 and [10]
>>> can_pick_two([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 10])
True
"""


def can_pick_two(nums: list[int]) -> bool:
    """
    Pick two indexes such that the three partitions around them sum up to the
    same value.

    This has worst case O(n^2) time and O(n) space, best case O(n) time and O(n)
    space.
    """
    n: int = len(nums)
    if n == 2:
        return True
    elif n < 5:  # they all have to be positive integers, so no 0s
        return False

    a: int = nums[0]
    c_sum: int = sum(nums[4:])
    for i in range(1, n - 3):
        b: int = nums[i + 1]
        c: int = c_sum
        for j in range(i + 2, n - 1):
            if a == b == c:
                return True
            elif b > a or b > c:
                break

            b += nums[j]
            c -= nums[j + 1]

        a += nums[i]
        c_sum -= nums[i + 3]

    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
