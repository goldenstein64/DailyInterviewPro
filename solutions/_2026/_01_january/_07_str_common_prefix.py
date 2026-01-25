"""
Given a list of strings, find the longest common prefix between all strings.

Examples:

>>> longest_common_prefix(['helloworld', 'hellokitty', 'hell'])
'hell'
>>> longest_common_prefix(['ab', 'ab', 'ac'])
'a'
>>> longest_common_prefix(['daily', 'interview', 'pro'])
''
"""

from itertools import takewhile


def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    elif len(strs) == 1:
        return strs[0]

    zipped: zip[tuple[str, ...]] = zip(*strs)
    prefix = takewhile(lambda cs: all(cs[0] == b for b in cs[1:]), zipped)
    return "".join(cs[0] for cs in prefix)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
