"""
Given a number of integers, concatenate them so it would create the largest
number.

Example:

>>> largest_num([17, 7, 2, 45, 72])
77245217

>>> largest_num([123, 4, 5, 6, 78, 9])
978654123

>>> largest_num([83, 830])
83830
"""


def largest_num(nums: list[int]) -> int:
    strings = list(map(str, nums))
    max_len = max(map(len, strings))
    strings.sort(reverse=True, key=lambda s: s + s[-1] * (max_len - len(s)))
    return int("".join(strings))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
