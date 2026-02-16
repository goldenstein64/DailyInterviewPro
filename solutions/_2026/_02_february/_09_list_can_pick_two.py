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

import unittest


def can_pick_two(nums: list[int]) -> bool:
    """
    Given a list of positive integers, determine whether there exist two indexes
    such that the three partitions around them sum up to the same value.

    This has worst case O(n^2) time and O(n) space, best case O(n) time and O(n)
    space.
    """
    n: int = len(nums)
    if n == 2:  # no elements in all partitions
        return True
    elif n < 5:
        # Having less than 5 elements means there must be at least one partition
        # with no elements, which means every element would have to be equal to
        # zero. That's impossible since every integer must be positive
        return False

    # minimal non-trivial case: [left_sum, i, middle_sum, j, right_sum]

    left_sum: int = nums[0]  # sum(nums[:i])
    right_starting_sum: int = sum(nums[4:])
    for i in range(1, n - 3):
        if left_sum > right_starting_sum:
            break

        middle_sum: int = nums[i + 1]  # sum(nums[i+1:j])
        right_sum: int = right_starting_sum  # sum(nums[j+1:])

        for j in range(i + 2, n - 1):
            if left_sum == middle_sum == right_sum:
                return True
            elif middle_sum > left_sum or middle_sum > right_sum:
                break

            middle_sum += nums[j]
            right_sum -= nums[j + 1]

        left_sum += nums[i]
        right_starting_sum -= nums[i + 3]

    return False


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], bool]] = [
        ([], False),
        ([1], False),
        ([1, 1], True),
        ([1, 1, 1], False),
        ([1, 1, 1, 1], False),
        ([1, 1, 1, 1, 1], True),
        ([2, 4, 5, 3, 3, 9, 2, 2, 2], True),
        ([1, 200, 1, 400, 1], True),
        ([1, 5, 9, 50, 3, 5, 7, 50, 2, 5, 8], True),
        ([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 10], True),
    ]

    def test_cases(self):
        for nums, expected in self.cases:
            with self.subTest(nums=nums, expected=expected):
                self.assertEqual(expected, can_pick_two(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
