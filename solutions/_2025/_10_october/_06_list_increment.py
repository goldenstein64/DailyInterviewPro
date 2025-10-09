"""
Given a non-empty array where each element represents a digit of a non-negative
integer, add one to the integer. The most significant digit is at the front of
the array and each element in the array contains only one digit. Furthermore,
the integer does not have leading zeros, except in the case of the number '0'.

Example:

>>> increment([0])
[1]

>>> increment([2, 3, 4])
[2, 3, 5]

>>> increment([2, 9, 9])
[3, 0, 0]

>>> increment([9, 9, 9])
[1, 0, 0, 0]
"""


def increment(number: list[int]) -> list[int]:
    """
    Increment a number represented as a list of digits, returning the new
    number.

    This uses O(n) time and O(n) space. If this were to operate on the
    input in-place, time complexity would have an average case of O(1).
    """

    result: list[int] = number.copy()
    for i in range(len(result) - 1, -1, -1):
        digit: int = number[i]
        if digit == 9:
            result[i] = 0
        else:
            result[i] = digit + 1
            break

    if result[0] == 0:  # the entire number consisted of 9s
        result.insert(0, 1)

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
