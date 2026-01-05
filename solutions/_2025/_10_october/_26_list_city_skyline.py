"""
Given a list of building in the form of (left, right, height), return what the
skyline should look like. The skyline should be in the form of a list of
(x-axis, height), where x-axis is the next point where there is a change in
height starting from 0, and height is the new height starting from the x-axis.

Example:

#            2 2 2
#            2 2 2
#        1 1 2 2 2 1 1
#        1 1 2 2 2 1 1
#        1 1 2 2 2 1 1
# pos: 1 2 3 4 5 6 7 8 9
>>> generate_skyline([(2, 8, 3), (4, 6, 5)])
[(2, 3), (4, 5), (6, 3), (8, 0)]

>>> generate_skyline_gpt([(2, 8, 3), (4, 6, 5)])
[(2, 3), (4, 5), (6, 3), (8, 0)]
"""

from collections import defaultdict
from heapq import heappop, heappush
from math import inf


def generate_skyline(buildings: list[tuple[int, int, int]]) -> list[tuple[int, int]]:
    """
    Given a list of building positions and heights, generate what the skyline
    would look like. This feels like a very naive way to implement this.

    This uses O(sum(b[1] - b[0] for b in buildings) + n) time and O(n - m) space, where:
    m = min(b[0] for b in buildings)
    n = max(b[1] for b in buildings)
    b = len(buildings)
    """
    heights: defaultdict[int, int] = defaultdict(lambda: 0)
    max_pos: int = 0
    for left, right, height in buildings:
        max_pos = max(max_pos, right)
        for i in range(left, right):
            heights[i] = max(heights[i], height)

    current: int = 0
    result: list[tuple[int, int]] = []
    for i in range(1, max_pos):
        height: int = heights[i]
        if current != height:
            result.append((i, height))
            current = height

    result.append((max_pos, 0))

    return result


def generate_skyline_gpt(
    buildings: list[tuple[int, int, int]],
) -> list[tuple[int, int]]:
    # create critical points (what is a critical point?)
    events: list[tuple[int, int, int]] = []
    for left, right, height in buildings:
        events.append((left, -height, right))  # entering event
        events.append((right, 0, 0))  # leaving event (what does this mean?)

    events.sort()  # sort by x position

    result: list[tuple[int, int]] = []
    heap: list[tuple[int, float]] = [(0, inf)]  # (negative height, right boundary)
    prev_height: int = 0

    for x, neg_height, right in events:
        # remove buildings that have ended
        while heap and heap[0][1] <= x:
            heappop(heap)

        # if starting a new building, add it to the heap
        if neg_height != 0:
            heappush(heap, (neg_height, right))

        current_height: int = -heap[0][0]
        if current_height != prev_height:
            result.append((x, current_height))
            prev_height = current_height

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
