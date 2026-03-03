"""
Given a string `s` and a character `c`, find the distance for all characters in
the string to the character `c` in the string `s`. You can assume that the
character `c` will appear at least once in the string.

Example:

>>> distance_from_char("helloworld", "l")
[2, 1, 0, 0, 1, 2, 2, 1, 0, 1]

>>> distance_from_char("gerald", "g")
[0, 1, 2, 3, 4, 5]

>>> distance_from_char("signage", "e")
[6, 5, 4, 3, 2, 1, 0]
"""


def distance_from_char(s: str, c: str) -> list[int]:
    """
    For every character in `s`, return its distance to the nearest character
    `c`. It first iterates through the string to get its distance to the
    nearest character `c` left of it, and then compares right-ward distance
    while iterating backwards, taking the minimum.

    This uses O(n) time and O(n) space.
    """
    if not s:
        return []
    elif s == c:
        return [0]

    result: list[int] = list(range(len(s))) if s[0] == c else [len(s)] * len(s)

    for i in range(1, len(s)):
        result[i] = 0 if s[i] == c else result[i - 1] + 1

    for i in reversed(range(len(s) - 1)):
        result[i] = min(result[i], result[i + 1] + 1)

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
