"""
You are given a hash table where the key is a course code, and the value is a
list of all the course codes that are prerequisites for the key. Return a valid
ordering in which we can complete the courses. If no such ordering exists,
return None.

Example:
    {
        'CSC300': ['CSC100', 'CSC200'],
        'CSC200': ['CSC100'],
        'CSC100': []
    }

    This input should return the order that we need to take the courses:
    ['CSC100', 'CSC200', 'CSC300']
"""

import unittest
from collections import deque, defaultdict
from typing import Callable
from itertools import product


def find_valid_course(incomplete: dict[str, list[str]]) -> str | None:
    for course, prereqs in incomplete.items():
        if all(prereq not in incomplete for prereq in prereqs):
            return course

    return None


def courses_to_take(course_to_prereqs: dict[str, list[str]]) -> list[str] | None:
    incomplete: dict[str, list[str]] = course_to_prereqs.copy()
    result: list[str] = []
    for _ in range(len(incomplete)):
        if course := find_valid_course(incomplete):
            del incomplete[course]
            result.append(course)
        else:
            return None

    return result


def courses_to_take_kahn(course_to_prereqs: dict[str, list[str]]) -> list[str] | None:
    """A solution given to me by ChatGPT."""
    in_degree: defaultdict[str, int] = defaultdict(lambda: 0)
    graph: defaultdict[str, list[str]] = defaultdict(lambda: [])

    for course, prereqs in course_to_prereqs.items():
        in_degree[course] += 0
        for prereq in prereqs:
            graph[prereq].append(course)
            in_degree[course] += 1

    queue: deque[str] = deque(
        course for course in in_degree.keys() if in_degree[course] == 0
    )
    result: list[str] = []

    if len(queue) > 0:
        course = queue.popleft()
        result.append(course)
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(in_degree) else None


class Tests(unittest.TestCase):
    solutions: list[Callable[[dict[str, list[str]]], list[str] | None]] = [
        courses_to_take,
        courses_to_take_kahn,
    ]

    cases: list[tuple[dict[str, list[str]], list[str] | None]] = [
        ({}, []),
        ({"a": []}, ["a"]),
        ({"a": ["a"]}, None),
        ({"a": ["b"], "b": ["a"]}, None),
        ({"c": ["a", "b"], "b": ["a"], "a": []}, ["a", "b", "c"]),
        (
            {"CSC300": ["CSC100", "CSC200"], "CSC200": ["CSC100"], "CSC100": []},
            ["CSC100", "CSC200", "CSC300"],
        ),
    ]

    def test_all(self):
        for solution, (course_to_prereqs, expected) in product(
            self.solutions, self.cases
        ):
            name = solution.__name__
            with self.subTest(
                solution=name, prereqs=course_to_prereqs, expected=expected
            ):
                self.assertEqual(expected, courses_to_take(course_to_prereqs))


if __name__ == "__main__":
    unittest.main()
