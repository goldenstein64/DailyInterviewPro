r"""
Given a binary tree, remove the nodes in which there is only 1 child, so that
the binary tree is a full binary tree.

So leaf nodes with no children should be kept, and nodes with 2 children should
be kept as well.

Example:

>>> #     1
>>> #    / \
>>> #   2   3
>>> #  /   / \
>>> # 0   9   4
>>> tree = BinaryTree.from_tuples((((0,), 2), 1, ((9,), 3, (4,))))

>>> #     1
>>> #    / \
>>> #   0   3
>>> #      / \
>>> #     9   4
>>> make_full(tree).as_tuples()
((0,), 1, ((9,), 3, (4,)))
"""

from ds.binary_tree import BinaryTree


def make_full[T](node: BinaryTree[T]) -> BinaryTree[T]:
    match (node.left, node.right):
        case (BinaryTree() as left, BinaryTree() as right):
            node.left = make_full(left)
            node.right = make_full(right)
            return node
        case (BinaryTree() as child, None) | (None, BinaryTree() as child):
            return make_full(child)
        case (None, None):
            return node


if __name__ == "__main__":
    import doctest

    doctest.testmod()
