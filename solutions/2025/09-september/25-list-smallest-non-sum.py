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
