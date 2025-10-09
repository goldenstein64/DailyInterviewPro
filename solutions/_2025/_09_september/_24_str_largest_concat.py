"""
Given a number of integers, concatenate them so it would create the largest
number.

Example:

>>> largest_num([17, 7, 2, 45, 72])
'77245217'

>>> largest_num([123, 4, 5, 6, 78, 9])
'978654123'

>>> largest_num([83, 830])
'83830'

>>> largest_num([3, 30, 34, 5, 9])
'9534330'

>>> largest_num([54, 546, 548, 60])
'6054854654'
"""

import unittest
from collections.abc import Callable
from functools import cmp_to_key
from itertools import product


def cmp_by_concat(a: str, b: str) -> int:
    return -1 if a + b > b + a else 1


def largest_num_cmp(nums: list[int]) -> str:
    """
    A solution given to me by both ChatGPT and GeeksForGeeks. This uses a
    similar sorting method to mine, except the key function compares between two
    strings by concatenation directly.

    This uses O(n log n) time and O(n) space.
    """
    strings: list[str] = list(map(str, nums))
    strings.sort(key=cmp_to_key(cmp_by_concat))
    return "0" if strings[0] == "0" else "".join(strings)


def largest_num(nums: list[int]) -> str:
    """
    Create the largest possible integer from concatenating the input list of
    non-negative integers. This is implemented by sorting the list
    lexicographically and padding with the last digit until all elements are
    equal in length. Once sorted, all the strings are simply concatenated.

    This uses O(n log n) time and O(n) space.
    """
    strings: list[str] = list(map(str, nums))
    max_len = max(map(len, strings))
    strings.sort(reverse=True, key=lambda s: s + s[-1] * (max_len - len(s)))
    return "0" if strings[0] == "0" else "".join(strings)


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], str]] = [
        largest_num,
        largest_num_cmp,
    ]

    cases: list[tuple[list[int], str]] = [
        ([17, 7, 2, 45, 72], "77245217"),
        ([123, 4, 5, 6, 78, 9], "978654123"),
        ([83, 830], "83830"),
        ([3, 30, 34, 5, 9], "9534330"),
        ([54, 546, 548, 60], "6054854654"),
        ([2, 3, 10], "3210"),
        ([20, 2, 3], "3220"),
        ([121, 12], "12121"),
        ([0, 0, 0], "0"),
    ]

    def test_cases(self):
        for solution, (nums, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, expected=expected):
                self.assertEqual(expected, solution(nums))


def benchmark():
    import tracemalloc
    from math import floor
    from random import randint, random
    from timeit import timeit

    nums: list[int] = []
    for _ in range(randint(8_000, 12_000)):
        choice = random() * 4
        nums.append(floor(10**choice))

    for solution in Tests.solutions:
        print(f"{solution.__name__}:")
        tracemalloc.start()
        solution(nums)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"(Current {current / 1024} KiB) (Peak {peak / 1024} KiB)")
        time = timeit(lambda: solution(nums), number=1_000)
        print(f"(Time {time} s)")


def test():
    import doctest

    doctest.testmod()
    unittest.main()


if __name__ == "__main__":
    test()
    # benchmark()
