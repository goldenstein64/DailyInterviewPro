"""
Given a string `s` and a character `c`, find the distance for all characters in
the string to the character `c` in the string `s`. You can assume that the
character c will appear at least once in the string.

Examples:

>>> distance_from_char("helloworld", "l")
[2, 1, 0, 0, 1, 2, 2, 1, 0, 1]
"""

# This has been done before (!), and so recently that I don't want to implement
# it again.
from solutions._2026._03_march._02_str_distance_from_char import distance_from_char

distance_from_char = distance_from_char

if __name__ == "__main__":
    import doctest

    doctest.testmod()
