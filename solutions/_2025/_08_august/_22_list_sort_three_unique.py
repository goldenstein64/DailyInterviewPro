"""
Given an array with n objects colored red, white or blue, sort them in-place so
that objects of the same color are adjacent, with the colors in the order red,
white and blue.

Can you do this in a single pass?

Example:

>>> colors = [Color.BLUE, Color.RED, Color.WHITE]
>>> sort_colors(colors)
>>> colors
[<Color.RED: 0>, <Color.WHITE: 1>, <Color.BLUE: 2>]

>>> colors = [Color.BLUE, Color.RED, Color.BLUE, Color.WHITE, Color.WHITE, Color.RED]
>>> sort_colors(colors)
>>> colors
[<Color.RED: 0>, <Color.RED: 0>, <Color.WHITE: 1>, <Color.WHITE: 1>, <Color.BLUE: 2>, <Color.BLUE: 2>]

>>> colors = [Color.BLUE, Color.BLUE, Color.WHITE, Color.RED, Color.BLUE, Color.WHITE, Color.RED]
>>> sort_colors(colors)
>>> colors
[<Color.RED: 0>, <Color.RED: 0>, <Color.WHITE: 1>, <Color.WHITE: 1>, <Color.BLUE: 2>, <Color.BLUE: 2>, <Color.BLUE: 2>]
"""

from enum import Enum


class Color(Enum):
    RED = 0
    WHITE = 1
    BLUE = 2


def sort_colors(colors: list[Color]) -> None:
    """
    Sort a list of colors containing only red, white, and blue.

    This uses O(n) time and O(1) space.

    This follows Dijkstra's three-way partitioning algorithm.
    See: https://en.wikipedia.org/wiki/Dutch_national_flag_problem#Pseudocode

    Also see an earlier implementation: ./2025/07-july/12-sort-three-unique.py
    """
    low = 0
    mid = 0
    high = len(colors) - 1
    while mid <= high:
        match colors[mid]:
            case Color.RED:
                colors[low], colors[mid] = colors[mid], colors[low]
                low += 1
                mid += 1
            case Color.BLUE:
                colors[mid], colors[high] = colors[high], colors[mid]
                high -= 1
            case Color.WHITE:
                mid += 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
