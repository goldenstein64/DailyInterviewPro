"""
Given two arrays, write a function to compute their intersection - the
intersection means the numbers that are in both arrays.

Note:
Each element in the result must be unique.
The result can be in any order.

>>> inter1 = intersection([1, 2, 2, 1], [2])
>>> type(inter1)
<class 'list'>
>>> sorted(inter1)
[2]

>>> inter2 = intersection([4, 9, 5], [9, 4, 9, 8, 4])
>>> type(inter2)
<class 'list'>
>>> sorted(inter2)
[4, 9]
"""

from itertools import product
import unittest
from collections.abc import Callable


def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Return all numbers that belong to both lists. This uses a simple
    algorithm that turns both lists into sets and creates an intersection.
    """
    return list(set(nums1) & set(nums2))


def intersection_sorted(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Return all numbers that belong to both lists. This sorts both lists and
    tries to keep their indexes "balanced" by incrementing their independent
    pointers until one reaches the end of the list
    """
    if not nums1 or not nums2:
        return []

    result: list[int] = []
    nums1 = sorted(nums1)
    nums2 = sorted(nums2)
    i: int = 0
    j: int = 0
    while i < len(nums1) and j < len(nums2):
        num1: int = nums1[i]
        num2: int = nums2[j]
        if num1 > num2:
            j += 1
        else:
            i += 1

        if num1 == num2 and (not result or result[-1] != num1):
            result.append(num1)

    return result


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int], list[int]], list[int]]] = [
        intersection,
        intersection_sorted,
    ]

    cases: list[tuple[list[int], list[int], list[int]]] = [
        ([1], [], []),
        ([1, 2], [2, 3], [2]),
        ([1, 2, 2, 1], [2], [2]),
        ([4, 9, 5], [9, 4, 9, 8, 4], [4, 9]),
    ]

    def test_cases(self):
        for solution, (nums1, nums2, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(
                solution=sol, nums1=nums1, nums2=nums2, expected=expected
            ):
                result = solution(nums1, nums2)
                self.assertEqual(list, type(result))
                self.assertEqual(expected, sorted(result))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
