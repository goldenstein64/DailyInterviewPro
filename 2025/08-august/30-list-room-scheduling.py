"""
You are given an array of tuples (start, end) representing time intervals for
lectures. The intervals may be overlapping. Return the number of rooms that are
required.

Example:

>>> min_rooms([(30, 75), (0, 50), (60, 150)])
2
"""

from itertools import islice, product
from sys import maxsize
from heapq import heappush, heappop
import unittest
from typing import Callable


def min_rooms(schedule: list[tuple[int, int]]) -> int:
    """
    Determine the minimum number of rooms required to fit these lectures' time
    intervals without overlapping.

    This has O(nk) time complexity and O(n) space, where n is the number of
    intervals and k is the resulting number of rooms. In this worst case, k = n,
    making the algorithm O(n^2) time worst case.
    """
    intervals: list[tuple[int, int]] = sorted(schedule)

    rooms: list[list[tuple[int, int]]] = [[intervals[0]]]

    for interval in islice(intervals, 1, len(intervals)):
        # put this interval in the one with the least room
        min_diff: int = maxsize
        min_room: list[tuple[int, int]] | None = None
        for room in rooms:
            last_interval = room[-1]
            diff = interval[0] - last_interval[1]
            if 0 < diff < min_diff:
                min_diff = diff
                min_room = room

        if min_room is None:
            rooms.append([interval])
        else:
            min_room.append(interval)

    return len(rooms)


def min_rooms_gpt(schedule: list[tuple[int, int]]) -> int:
    if not schedule:
        return 0

    start_times: list[tuple[int, int]] = sorted(schedule, key=lambda i: i[0])
    end_times: list[int] = []

    for start, end in start_times:
        if end_times and end_times[0] <= start:
            heappop(end_times)

        heappush(end_times, end)

    return len(end_times)


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[tuple[int, int]]], int]] = [
        min_rooms,
        min_rooms_gpt,
    ]

    cases: list[tuple[list[tuple[int, int]], int]] = [
        ([(0, 1)], 1),
        ([(0, 2), (1, 3)], 2),
        ([(0, 2), (1, 4), (3, 5)], 2),
        ([(30, 75), (0, 50), (60, 150)], 2),
    ]

    def test_cases(self):
        for solution, (schedule, expected) in product(self.solutions, self.cases):
            sol = solution.__name__
            with self.subTest(solution=sol, schedule=schedule, expected=expected):
                self.assertEqual(expected, solution(schedule))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
