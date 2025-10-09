r"""
You are given the root of a binary tree. Find the level for the binary tree with
the minimum sum, and return that value.

Example:

    10
   /  \
  2    8
 / \    \
4   1    2
>>> root = BinaryTree.from_tuples((((4,), 2, (1,)), 10, (8, (2,))))
>>> minimum_level_sum(root)
7
"""

from ds.binary_tree import BinaryTree
from collections import deque
from collections.abc import Generator


def depth_walk[T](root: BinaryTree[T]) -> Generator[BinaryTree[T]]:
    nodes: list[BinaryTree[T]] = [root]
    while nodes:
        node: BinaryTree[T] = nodes.pop()
        yield node

        if left := node.left:
            nodes.append(left)

        if right := node.right:
            nodes.append(right)


def depth_walk_with_level[T](
    root: BinaryTree[T],
) -> Generator[tuple[int, BinaryTree[T]]]:
    nodes: list[tuple[int, BinaryTree[T]]] = [(0, root)]
    while nodes:
        level, node = nodes.pop()
        yield level, node

        if left := node.left:
            nodes.append((level + 1, left))

        if right := node.right:
            nodes.append((level + 1, right))


def minimum_level_sum(root: BinaryTree[float]) -> float:
    """
    Calculate all sums by level and return the smallest one. This uses a simple
    depth-first walk to iterate through every node in the tree and add it to one
    of a list of sums grouped by level. The minimum of that list of sums is
    taken at the end.

    This uses O(n) time and O(h) space complexity, where
    n = node count and h = height.
    """
    sums_by_level: list[float] = []

    # walk through the entire tree compute sums by level
    for level, node in depth_walk_with_level(root):
        n: int = len(sums_by_level)
        assert level <= n
        if level < n:
            sums_by_level[level] += node.val
        else:
            sums_by_level.append(node.val)

    return min(sums_by_level)


def breadth_walk_by_level_once[T](
    nodes: deque[BinaryTree[T]],
) -> Generator[BinaryTree[T]]:
    for _ in range(len(nodes)):
        node = nodes.popleft()
        yield node

        if left := node.left:
            nodes.append(left)

        if right := node.right:
            nodes.append(right)


def breadth_walk_by_level[T](
    root: BinaryTree[T],
) -> Generator[Generator[BinaryTree[T]]]:
    nodes: deque[BinaryTree[T]] = deque()
    nodes.append(root)
    while nodes:
        yield breadth_walk_by_level_once(nodes)


def minimum_level_sum_rolling_min(root: BinaryTree[float]) -> float:
    """
    Calculate all sums by level and return the smallest one. This uses a series
    of generators to separate the iteration behavior from the function's intent.

    This uses O(n) time and about O(n) space. The worst-case space
    complexity of O(n) occurs when processing a balanced tree, whereas the best
    case would be O(1) with a skewed tree.
    """
    return min(sum(node.val for node in nodes) for nodes in breadth_walk_by_level(root))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
