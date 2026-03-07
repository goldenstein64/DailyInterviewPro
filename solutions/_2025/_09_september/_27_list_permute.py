"""
You are given an array of integers. Return all the permutations of this array.

Example:

>>> sorted(permute([1, 2, 3]))
[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
"""

import unittest
from collections.abc import Callable, Generator, Sequence
from itertools import permutations, product


def cycles_of(nums: list[int]) -> Generator[list[int]]:
    n: int = len(nums)
    for i in range(n):
        yield [nums[(i + j) % n] for j in range(n)]


def permute_inner(n: int) -> Generator[list[int]]:
    """
    Produce an n-sized permutation of indexes.

    This uses precisely O(n!) time and O(n!) space. It would be O(n) space if
    the lists produced by `cycles_of` were reused.
    """

    if n == 1:
        yield [0]
        return

    for permutation in permute_inner(n - 1):
        permutation.append(n - 1)
        yield from cycles_of(permutation)


def permute[T](nums: Sequence[T]) -> list[list[T]]:
    """
    My implementation of the solution, which produces every permutation of
    indexes for a list of size `len(nums)` and maps it over `nums`.

    This uses O(n!) time and O(n!) space.
    """
    return [[nums[i] for i in perm] for perm in permute_inner(len(nums))]


def permute_heap_rec_inner[T](k: int, nums: list[T]) -> Generator[list[T]]:
    if k == 1:
        yield nums.copy()
        return

    k_decr: int = k - 1
    yield from permute_heap_rec_inner(k_decr, nums)
    if k % 2 == 0:
        for i in range(k_decr):
            nums[i], nums[k_decr] = nums[k_decr], nums[i]
            yield from permute_heap_rec_inner(k_decr, nums)
    else:
        for _ in range(k_decr):
            nums[0], nums[k_decr] = nums[k_decr], nums[0]
            yield from permute_heap_rec_inner(k_decr, nums)


def permute_heap_rec[T](nums: list[T]) -> list[list[T]]:
    """
    A recursive implementation of Heap's algorithm for permutations, taken from
    Wikipedia.

    This uses O(n!) time and O(n!) space. It would use O(n) space if `nums`
    wasn't copied on every iteration.

    Source: https://en.wikipedia.org/wiki/Heap%27s_algorithm
    """
    return list(permute_heap_rec_inner(len(nums), nums))


def permute_heap_inner[T](k: int, nums: list[T]) -> Generator[list[T]]:
    c: list[int] = [0] * k

    result: list[T] = nums.copy()
    yield result.copy()

    i: int = 1
    while i < k:
        if c[i] < i:
            j: int = 0 if i % 2 == 0 else c[i]
            result[j], result[i] = result[i], result[j]
            yield result.copy()

            # swap has occurred ending the while-loop. Simulate the increment of
            # the while-loop counter
            c[i] += 1
            # simulate recursive call reaching the base case by bringing the
            # pointer to the base case analog in the array
            i = 1
        else:
            # calling permutations(i + 1, nums) has ended as the while-loop
            # terminated. Reset the state and simulate popping the stack by
            # incrementing the pointer
            c[i] = 0
            i += 1


def permute_heap[T](nums: list[T]) -> list[list[T]]:
    """
    An iterative implementation of Heap's algorithm for permutations, taken from
    the same Wikipedia page.

    This uses O(n!) time and O(n!) space. It would use O(n) space if `nums`
    wasn't copied on every iteration.

    Source: https://en.wikipedia.org/wiki/Heap%27s_algorithm
    """
    return list(permute_heap_inner(len(nums), nums))


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[int]], list[list[int]]]] = [
        permute,
        permute_heap,
        permute_heap_rec,
    ]

    cases: list[list[int]] = [
        list(range(1)),
        list(range(2)),
        list(range(3)),
        list(range(4)),
    ]

    def test_cases(self):
        for solution, values in product(self.solutions, self.cases):
            sol: str = solution.__name__
            with self.subTest(solution=sol, values=values):
                expected: list[tuple[int, ...]] = list(permutations(values))
                actual: list[tuple[int, ...]] = sorted(map(tuple, solution(values)))
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
