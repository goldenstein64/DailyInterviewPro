"""
Given a binary tree, perform an in-order traversal both recursively and
iteratively.

Example:

>>> tree = BinaryTree.from_tuples((((2,), 6, (3,)), 12, ((7,), 4, (8,))))

>>> list(inorder_recursive(tree))
[2, 6, 3, 12, 7, 4, 8]

>>> list(inorder_iterative(tree))
[2, 6, 3, 12, 7, 4, 8]
"""

from collections.abc import Generator
from ds.binary_tree import BinaryTree


def inorder_recursive[T](tree: BinaryTree[T]) -> Generator[T]:
    # alternatively,
    # yield from tree.inorder_values_rec()

    if left := tree.left:
        yield from inorder_recursive(left)

    yield tree.val

    if right := tree.right:
        yield from inorder_recursive(right)


def inorder_iterative[T](tree: BinaryTree[T]) -> Generator[T]:
    # alternatively,
    # yield from tree.inorder_values()

    stack: list[BinaryTree[T]] = []
    current: BinaryTree[T] = tree

    while left := current.left:
        stack.append(current)
        current = left

    while current:
        yield current.val
        if right := current.right:
            current = right

            while left := current.left:
                stack.append(current)
                current = left
        elif stack:
            current = stack.pop()
        else:
            break


if __name__ == "__main__":
    import doctest

    doctest.testmod()
