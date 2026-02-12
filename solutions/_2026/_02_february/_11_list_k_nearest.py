"""
Given a list of points, an integer `k`, and a point `p`, find the `k` closest
points to `p`.

Example:

>>> k_nearest(
...     [(0, 0), (1, 1), (2, 2), (3, 3)],
...     3,
...     (0, 2)
... )
[(0, 0), (1, 1), (2, 2)]

>>> k_nearest(
...     [(1, 3), (-2, 2), (5, 8), (0, 1)],
...     2,
...     (0, 0)
... )
[(-2, 2), (0, 1)]
"""

from heapq import heappush, heappushpop
from collections.abc import Iterator
from itertools import islice

type Point = tuple[int, int]


def magnitude_sq(x: int, y: int) -> float:
    return x * x + y * y


def k_nearest(points: list[Point], k: int, p: Point) -> list[Point]:
    """
    Given a list of points, return the k nearest points to p.

    This has O(n log k) time and O(k) space.
    """
    if k == 0:
        return []

    k_points: list[tuple[float, Point]] = []
    it: Iterator[Point] = iter(points)
    for pt in islice(it, k):
        heappush(k_points, (-magnitude_sq(pt[0] - p[0], pt[1] - p[1]), pt))

    for pt in it:
        heappushpop(k_points, (-magnitude_sq(pt[0] - p[0], pt[1] - p[1]), pt))

    return [pt for _, pt in k_points]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
