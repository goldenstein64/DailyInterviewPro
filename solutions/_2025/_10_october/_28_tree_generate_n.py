"""
Given a number n, generate all binary search trees that can be constructed with
nodes 1 to n.

Example:

>>> [tree.as_tuples() for tree in generate_bst(3)]
[(1, (2, (3,))), (1, ((2,), 3)), ((1,), 2, (3,)), ((1, (2,)), 3), (((1,), 2), 3)]
"""

from ds.binary_tree import BinaryTree
from itertools import product


def generate_bst(count: int, offset: int = 1) -> list[BinaryTree[int]]:
    if count <= 0:
        return []
    elif count == 1:
        return [BinaryTree(offset)]

    result: list[BinaryTree[int]] = []
    for i in range(count):
        left_subtrees = generate_bst(i, offset) or [None]
        right_subtrees = generate_bst(count - i - 1, i + offset + 1) or [None]

        for left, right in product(left_subtrees, right_subtrees):
            result.append(BinaryTree(i + offset, left, right))

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
