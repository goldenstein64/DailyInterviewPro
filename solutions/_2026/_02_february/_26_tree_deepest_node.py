r"""
You are given the root of a binary tree. Return the deepest node (the furthest
node from the root).

Example:

>>> #     a
>>> #    / \
>>> #   b   c
>>> #  /
>>> # d
>>> root = BinaryTree.from_tuples(((("d",), "b"), "a", ("c",)))
>>> deepest_node(root)
('d', 3)

>>> deepest_node_iter(root)
('d', 3)
"""

from ds.binary_tree import BinaryTree


# This has been done before!
from solutions._2025._08_august._14_tree_deepest import (
    deepest_depth,  # pyright: ignore[reportUnusedImport]
)


def deepest_node[T](root: BinaryTree[T], depth: int = 1) -> tuple[T, int]:
    match (root.left, root.right):
        case (None, None):
            return (root.val, depth)
        case (child, None) | (None, child):
            return deepest_node(child, depth + 1)
        case (left, right):
            return max(
                deepest_node(left, depth + 1),
                deepest_node(right, depth + 1),
                key=lambda t: t[1],
            )


def deepest_node_iter[T](root: BinaryTree[T]) -> tuple[T, int]:
    result: tuple[BinaryTree[T], int] = (root, 1)
    stack: list[tuple[BinaryTree[T], int]] = [result]
    while stack:
        value = stack.pop()
        (node, depth) = value
        if depth > result[1]:
            result = value

        if left := node.left:
            stack.append((left, depth + 1))

        if right := node.right:
            stack.append((right, depth + 1))

    (node, depth) = result
    return (node.val, depth)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
