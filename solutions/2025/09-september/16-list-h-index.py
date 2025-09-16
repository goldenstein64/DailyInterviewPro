"""
The h-index is a metric that attempts to measure the productivity and citation
impact of the publication of a scholar. The definition of the h-index is if a
scholar has at least h of their papers cited h times.

Given a list of publications of the number of citations a scholar has, find
their h-index.

Example:

>>> h_index([3, 5, 0, 1, 3])
3
"""

import unittest


def h_index(publications: list[int]) -> int:
    """
    Determine the h-index of a scholar by how many citations each of their
    papers have received.

    This has O(n log n) time complexity and O(n) space. Space can be O(1) if the
    input list can be modified.
    """
    by_count = sorted(publications, reverse=True)
    for i, v in enumerate(by_count, start=1):
        if i > v:
            return i - 1

    return len(publications)


class Tests(unittest.TestCase):
    cases: list[tuple[list[int], int]] = [
        ([], 0),
        ([0], 0),
        ([0, 0], 0),
        ([10], 1),
        ([1, 4, 4], 2),
        ([3, 3, 3], 3),
        ([3, 3, 1, 3, 3], 3),
        ([3, 5, 1, 5, 5], 3),
        ([4, 5, 1, 5, 5], 4),
        ([5, 5, 1, 5, 5], 4),
        ([3, 5, 0, 1, 3], 3),
    ]

    def test_cases(self):
        for publications, expected in self.cases:
            with self.subTest(publications=publications, expected=expected):
                self.assertEqual(expected, h_index(publications))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
