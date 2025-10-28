"""
Given a sorted list, create a height balanced binary search tree, meaning the
height differences of each node can only differ by at most 1.

Example:

>>> create_bst([1, 2, 3, 4, 5, 6, 7, 8]).as_tuples()
((((1,), 2), 3, (4,)), 5, ((6,), 7, (8,)))
"""

# I already solved this
from solutions._2025._08_august._11_binary_search_tree_create import create_bst  # type: ignore


if __name__ == "__main__":
    import doctest

    doctest.testmod()
