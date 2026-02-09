"""
Given a linked list, remove all duplicate values from the linked list.

Example:

>>> arg = LinkedList.from_values([1, 2, 3, 3, 4])
>>> actual = remove_duplicates(arg)
>>> list(actual.values())
[1, 2, 4]

>>> list(arg.values())
[1, 2, 3, 3, 4]
>>> remove_duplicates_in_place(arg)
>>> list(arg.values())
[1, 2, 4]
"""

from ds.linked_list import LinkedList
from collections import Counter
from itertools import pairwise


def remove_duplicates[T](node: LinkedList[T] | None) -> LinkedList[T] | None:
    if not node:  # nothing to remove
        return None

    counts: Counter[T] = Counter(node.values())
    return LinkedList.from_values(v for v in node.values() if counts[v] == 1)


def remove_duplicates_in_place[T](node: LinkedList[T] | None) -> None:
    if not node:  # nothing to remove
        return

    counts: Counter[T] = Counter(node.values())
    pairs: list[tuple[LinkedList[T], LinkedList[T]]] = list(pairwise(node))
    pairs.reverse()
    for a, b in pairs:
        if counts[b.val] > 1:
            a.next = b.next


if __name__ == "__main__":
    import doctest

    doctest.testmod()
