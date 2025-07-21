"""
Given a list of numbers, find if there exists a pythagorean triplet in that
list. A pythagorean triplet is 3 variables a, b, c where a**2 + b**2 = c**2

Example:

    Input: [3, 5, 12, 5, 13]
    Output: True

    Here, 5**2 + 12**2 = 13**2
"""

import unittest


def find_pythagorean_triplets(nums: list[int]) -> bool:
    """
    a pythagorean triplet:
    - never has two identical numbers
    - sets its largest number equal to the sum of the two smaller ones squared
    - the distance between the larger two are determined by the smaller one

    3, 4, 5
    5, 12, 13
    7, 24, 25
    8, 15, 17
    9, 40, 41
    11, 60, 61
    12, 35, 37
    13, 84, 85

    pattern matching:
    a pythagorean triple always has one of two structures:
    when a is odd: a, f'(a**2) - 1, f'(a**2)
    when a is even: a, g'(a**2) - 2, g'(a**2)

    where f is a function with an output equal to x**2 - (x-1)**2
    and g is a function with an output equal to x**2 - (x-2)**2
    f and g can be simplified to linear functions 2x - 1 and 4x - 4
    respectively, whose inverses are (x + 1)/2 and (x + 4)/4, also respectively.

    Not every triplet is accounted for with this function, specifically
    non-primitive triplets
    """

    if len(nums) < 3:
        return False

    set_nums = set(nums)
    for a in set_nums:
        if a % 2 == 0:  # even
            c = (a**2 + 4) // 4
            b = c - 2
            if b in set_nums and c in set_nums:
                return True
        else:  # a % 2 == 1, odd
            c = (a**2 + 1) // 2
            b = c - 1
            if b in set_nums and c in set_nums:
                return True

    return find_pythagorean_triplets_all(nums)


def find_pythagorean_triplets_all(nums: list[int]) -> bool:
    """brute-force function provided by ChatGPT"""
    squares = set(x * x for x in nums)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] != nums[j]:
                if nums[i] ** 2 + nums[j] ** 2 in squares:
                    return True
    return False


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], bool]] = [
        ([10], False),
        ([3, 4], False),
        ([1, 1, 1], False),
        ([4, 8, 9], False),
        ([3, 4, 5], True),
        ([3, 12, 5, 13], True),
        ([3, 5, 12, 5, 13], True),
        ([7, 24, 25], True),
    ]

    def test_all(self):
        for nums, expected in self.cases:
            with self.subTest(nums=nums, expected=expected):
                self.assertEqual(expected, find_pythagorean_triplets(nums))


if __name__ == "__main__":
    unittest.main()
