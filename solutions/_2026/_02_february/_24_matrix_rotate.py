"""
Given a square 2D matrix (n x n), rotate the matrix by 90 degrees clockwise.

Example:

>>> from pprint import pprint
>>>
>>> actual = rotate(
...     [[1, 2, 3],
...      [4, 5, 6],
...      [7, 8, 9]]
... )
>>> pprint(actual, width=11)
[[7, 4, 1],
 [8, 5, 2],
 [9, 6, 3]]
"""


def rotate(mat: list[list[int]]) -> list[list[int]]:
    n: int = len(mat)
    result: list[list[int]] = [[-1] * n for _ in range(n)]
    for i, row in enumerate(mat):
        for j, value in enumerate(row):
            result[j][n - i - 1] = value

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
