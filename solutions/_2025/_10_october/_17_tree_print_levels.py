r"""
You are given a tree, and your job is to print it level-by-level **with
linebreaks**.

I'm implementing this example a little differently, by creating an iterator
that does essentially the same thing. You can print each level line-by-line using
`str.join`.

Example:

>>> tree = BinaryTree.from_tuples(
...     ((('d',), 'b', ('e',)), 'a', (('f',), 'c', ('g',)))
... )
>>> [[n.val for n in level] for level in split_by_levels(tree)]
[['a'], ['b', 'c'], ['d', 'e', 'f', 'g']]
>>> print(
...     "\n".join(
...         "".join(n.val for n in level) for level in split_by_levels(tree)
...     )
... )
a
bc
defg
"""

from ds.binary_tree import BinaryTree
from collections.abc import Generator


def split_by_levels[T](root: BinaryTree[T]) -> Generator[list[BinaryTree[T]]]:
    # perform a breadth walk through the tree, by level
    current_list: list[BinaryTree[T]] = [root]
    while current_list:
        yield current_list
        new_list: list[BinaryTree[T]] = []
        for node in current_list:
            if left := node.left:
                new_list.append(left)

            if right := node.right:
                new_list.append(right)

        current_list = new_list


if __name__ == "__main__":
    import doctest

    doctest.testmod()
