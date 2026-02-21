"""
Given a list of numbers, find if there exists a pythagorean triplet in that
list. A pythagorean triplet is 3 variables a, b, c where `a**2 + b**2 = c**2`.

Example:

>>> # 5**2 + 12**2 = 13**2
>>> find_pythagorean_triplets([3, 5, 12, 5, 13])
True

>>> find_pythagorean_triplets([3, 12, 5, 13])
True
"""

# This has been done before!
from solutions._2025._07_july._20_list_pythagorean_triplets import (
    find_pythagorean_triplets as find_pythagorean_triplets_old,
)


if __name__ == "__main__":
    import doctest

    find_pythagorean_triplets = find_pythagorean_triplets_old
    doctest.testmod()
