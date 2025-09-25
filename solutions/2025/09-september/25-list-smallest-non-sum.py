"""
Given a sorted list of positive numbers, find the smallest positive number that
cannot be a sum of any subset in the list.

Example:

>>> find_smallest([1, 2, 3, 8, 9, 10])
7

Explanation:
0 -> []
1 -> [1]
2 -> [2]
3 -> [3]
4 -> [1, 3]
5 -> [2, 3]
6 -> [1, 2, 3]
7 -> DNE
"""

import unittest


def find_smallest(nums: list[int]) -> int:
    """
    Find the smallest positive integer that cannot be represented as a sum of a
    subset of the input list, which is a sorted list of positive integers. This
    was adapted from a Geeks for Geeks tutorial.

    This has O(n) time complexity and O(1) space.

    See:
    https://www.geeksforgeeks.org/dsa/find-smallest-value-represented-sum-subset-given-array/
    https://www.youtube.com/watch?v=0fo1GoekyaY
    """
    result: int = 1
    for num in nums:
        if result < num:
            return result
        else:
            result += num

    return result


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int]] = [
        ([], 1),
        ([1], 2),
        ([2], 1),
        ([1, 3], 2),
        ([1, 3, 6, 10, 11, 15], 2),
        ([1, 1, 1, 1], 5),
        ([1, 1, 3, 4], 10),
        ([1, 2, 3, 8, 9, 10], 7),
    ]

    def test_cases(self):
        for nums, expected in self.cases:
            with self.subTest(nums=nums, expected=expected):
                self.assertEqual(expected, find_smallest(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
