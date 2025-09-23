"""
Given an array of characters with repeats, compress it in-place. The length
after compression should be less than or equal to the original array.

Example:

>>> chars = ['a', 'a', 'b', 'c', 'c', 'c']
>>> compress(chars)
>>> chars
['a', '2', 'b', 'c', '3']
"""

from itertools import islice


def compress_pure(chars: list[str]) -> list[str]:
    """
    Compress a string by encoding repeats. This is a pure implementation that
    doesn't modify the character array in-place.

    This has O(n) time complexity and O(n) space.

    Example:

    >>> compress_pure(['a', 'a', 'b', 'c', 'c', 'c'])
    ['a', '2', 'b', 'c', '3']
    """
    last_char: str = chars[0]
    count: int = 1
    result: list[str] = []

    def result_append() -> None:
        result.append(last_char)
        if count > 1:
            result.append(str(count))

    for c in islice(chars, 1, len(chars)):
        if last_char == c:
            count += 1
        else:
            result_append()
            last_char = c
            count = 1

    result_append()

    return result


def compress(chars: list[str]) -> None:
    last_char = chars[0]
    count: int = 1
    i: int = 0

    def replace_chars() -> None:
        nonlocal i
        if count == 1:
            chars[i] = last_char
            i += 1
        else:
            chars[i : i + 2] = last_char, str(count)
            i += 2

    for c in islice(chars, 1, len(chars)):
        if last_char == c:
            count += 1
        else:
            replace_chars()
            last_char = c
            count = 1

    replace_chars()
    del chars[i:]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
