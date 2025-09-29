"""
Starting at index 0, for an element n at index i, you are allowed to jump at
most n indexes ahead. Given a list of numbers, find the minimum number of jumps
to reach the end of the list.

Example:

>>> jump_to_end([3, 2, 5, 1, 1, 9, 3, 4])
2
"""

import unittest


def jump_to_end(nums: list[int]) -> int:
    """
    Find the minimum number of jumps are needed to reach the end of `nums`,
    where each element holds the farthest one can jump.

    This has a worst case of O(n) time complexity and O(1) space.
    """

    n: int = len(nums)
    if n < 2:
        return 0

    index: int = 0
    max_index: int = nums[index]
    jumps: int = 1
    while max_index < n - 1:
        prev_index: int = index
        for i in range(index + 1, index + nums[index] + 1):
            v = nums[i]
            if i + v > max_index:
                max_index = i + v
                index = i

        if index <= prev_index:
            raise ValueError("end is unreachable")
        jumps += 1

    return jumps


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int | Exception]] = [
        ([], 0),
        ([0], 0),
        ([1], 0),
        ([1, 2], 1),
        ([1, 0], 1),
        ([0, 2], ValueError("end is unreachable")),
        ([1, 0, 2], ValueError("end is unreachable")),
        ([1, 2, 3], 2),
        ([1, 2, 3, 4], 2),
        ([1, 2, 3, 4, 5], 3),
        ([2, 2, -1, 3], 2),
        ([3, 2, 5, 1, 1, 9, 3, 4], 2),
        ([5, 4, 3, 2, 1, 1, 1, 1], 3),
    ]

    def test_cases(self):
        for nums, expected in self.cases:
            with self.subTest(nums=nums, expected=expected):
                if isinstance(expected, Exception):
                    with self.assertRaises(type(expected)) as e:
                        jump_to_end(nums)

                    self.assertEqual(expected.args, e.exception.args)
                else:
                    self.assertEqual(expected, jump_to_end(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
