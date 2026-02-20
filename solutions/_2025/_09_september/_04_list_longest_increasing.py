"""
You are given a list of integers. Return the length of the longest increasing
subsequence (not necessarily contiguous) in the list.

Example:

>>> longest_increasing([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])
6
"""

import unittest
from bisect import bisect_left
from collections.abc import Callable
from itertools import islice, product, takewhile


def longest_increasing(nums: list[int]) -> int:
    """
    Find the longest increasing subsequence of numbers. This uses a combination
    of a greedy and brute-force approach, where the greedy sequence
    always appends the latest element and removes previous elements until it is
    valid, and all sequences with a length greater than the greedy sequence are
    discovered and maintained in a brute-force list, copied when necessary.

    The worst case is hard to calculate, but I suspect it to be a list with
    multiple increasing subsequences that decrease in length, i.e.
    [0, 1, ..., n, 0, 1, ..., n-1, 0, 1, ..., n-2, ...]. This requires
    maintaining every input element in brute-force sequences.

    The best case is likely a list of [k, k, k, ...], which discovers no
    brute-force sequences and just uses the greedy sequence. This has O(n) time
    and O(1) space complexity.
    """
    if not nums:
        return 0

    greedy_seq: list[int] = [nums[0]]
    sequences: list[list[int]] = []

    for num in islice(nums, 1, len(nums)):
        if not sequences:
            if greedy_seq[-1] < num:
                # net gain
                greedy_seq.append(num)
            elif len(greedy_seq) == 1 or greedy_seq[-2] < num:
                # net neutral
                greedy_seq[-1] = num
            else:
                # net loss, create a copy and make it a brute-force sequence
                sequences.append(greedy_seq.copy())

                greedy_seq.pop()
                greedy_seq.pop()
                while greedy_seq and greedy_seq[-1] >= num:
                    greedy_seq.pop()
                greedy_seq.append(num)
        else:
            for seq in sequences:
                if seq[-1] < num:
                    # net gain
                    seq.append(num)
                elif len(seq) == 1 or seq[-2] < num:
                    # net neutral
                    # just write over the last element
                    seq[-1] = num
                else:
                    # net loss, create a copy with the removed elements
                    sequences.append([*takewhile(lambda x: x < num, seq), num])

            while greedy_seq and greedy_seq[-1] >= num:
                greedy_seq.pop()
            greedy_seq.append(num)

            for i in reversed(range(len(sequences))):
                seq = sequences[i]
                if len(seq) <= len(greedy_seq):
                    sequences.pop(i)

    if not sequences:
        return len(greedy_seq)
    else:
        return max(len(greedy_seq), *map(len, sequences))


def longest_increasing_dynamic(nums: list[int]) -> int:
    """
    An implementation given to me by ChatGPT, marked as the "dynamic
    programming" approach.

    `lengths` is a list of the lengths of the longest increasing subsequences
    that can be created at a certain index, with `lengths[k]` referring to the
    longest increasing subsequence that ends with `nums[k]`.

    This has O(n^2) time and O(n) space complexity.

    Source: https://chatgpt.com/share/69988640-55dc-8007-89df-85866957fa29
    """
    if not nums:
        return 0

    lengths: list[int] = [1] * len(nums)
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                lengths[i] = max(lengths[i], lengths[j] + 1)

    return max(lengths)


def longest_increasing_patience(nums: list[int]) -> int:
    """
    An implementation given to me by ChatGPT, marked as the "patience sorting"
    approach.

    `tails` is a list of input elements where `tails[k]` refers to the last
    element of a subsequence of length `k + 1`. Each input element `num` is
    "replaced" into the longest subsequence whose last value is at most `num`.
    If no such subsequence exists because `num` is greater than all values seen
    so far, a new entry is appended to the end.

    This has O(n log n) time and O(n) worst case space complexity.

    Source: https://chatgpt.com/share/69988640-55dc-8007-89df-85866957fa29
    """
    tails: list[int] = []
    for num in nums:
        idx = bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num

    return len(tails)


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], int]] = [
        longest_increasing,
        longest_increasing_dynamic,
        longest_increasing_patience,
    ]

    cases: list[tuple[list[int], int]] = [
        ([], 0),
        ([1], 1),
        ([1, 1], 1),
        ([2, 1], 1),
        ([1, 2], 2),
        ([1, 0, -1], 1),  # [-1]
        ([1, -1, 0], 2),  # [-1, 0]
        ([0, -1, 1], 2),  # [-1, 1]
        ([0, 1, -1], 2),  # [0, 1]
        ([-1, 1, 0], 2),  # [-1, 1]
        ([-1, 0, 1], 3),  # [-1, 0, 1]
        ([3, 2, 1], 1),
        ([3, 1, 2], 2),
        ([2, 1, 3], 2),
        ([2, 3, 1], 2),
        ([1, 3, 2], 2),
        ([1, 2, 3], 3),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
        ([5, 3, 4, 2, 1], 2),
        ([-5, -4, -3, -2, -1], 5),
        ([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15], 6),
        ([0, 8, 4, 12, 2, 10, 6, 14], 4),
    ]

    def test_cases(self):
        for solution, (nums, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, nums=nums, expected=expected):
                self.assertEqual(expected, solution(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
