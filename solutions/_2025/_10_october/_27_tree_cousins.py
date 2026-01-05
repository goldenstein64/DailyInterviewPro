r"""
Given a binary tree and a given node value, return all of the node's cousins.
Two nodes are considered cousins if they are on the same level of the tree with
different parents. You can assume that all nodes will have their own unique
value.

Example:

>>> list_cousins(
...     BinaryTree.from_tuples((((4,), 2, (6,)), 1, (3, (5,)))),
...     5,
... )
[4, 6]
"""

from ds.binary_tree import BinaryTree


def nodes_at_level[T](tree: BinaryTree[T], level: int) -> list[BinaryTree[T]]:
    current_level: list[BinaryTree[T]] = [tree]
    new_level: list[BinaryTree[T]] = []
    for _ in range(level):
        new_level.clear()
        if not current_level:
            return []

        for node in current_level:
            if left := node.left:
                new_level.append(left)

            if right := node.right:
                new_level.append(right)

        current_level, new_level = new_level, current_level

    return current_level


def list_cousins[T](tree: BinaryTree[T], val: T) -> list[T]:
    # we need to find the `val` node first
    val_node: BinaryTree[T] | None = next(
        (n for n in tree.preorder() if n.val == val), None
    )
    if not val_node:
        return []

    node: BinaryTree[T] | None = val_node.parent
    if not node:
        return []

    val_level: int = 1
    result: list[BinaryTree[T]] = []
    while node and (parent := node.parent):
        other: BinaryTree[T] | None = (
            parent.right if parent.left == node else parent.left
        )

        if other:
            result.extend(nodes_at_level(other, val_level))

        val_level += 1
        node = parent

    return [node.val for node in result]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
