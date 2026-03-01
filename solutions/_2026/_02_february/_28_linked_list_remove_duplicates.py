"""
Given a linked list, remove all duplicate values from the linked list.

Example:

>>> ls = LinkedList.from_values([1, 2, 3, 3, 4])
>>> actual = remove_duplicates(ls)
>>> actual and list(actual.values())
[1, 2, 4]
"""

from collections import Counter
from ds.linked_list import LinkedList

# This has been done before!
from solutions._2026._02_february._08_linked_list_remove_duplicates import (
    remove_duplicates as remove_duplicates_old,  # pyright: ignore[reportUnusedImport]
)


def remove_duplicates[T](ls: LinkedList[T]) -> LinkedList[T] | None:
    """
    Return a new linked list with all values appear more than once removed.

    This uses O(n) time and O(n) space.
    """
    counter = Counter(ls.values())
    return LinkedList.from_values(v for v in ls.values() if counter[v] <= 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
