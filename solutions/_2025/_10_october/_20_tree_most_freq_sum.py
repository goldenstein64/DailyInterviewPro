"""
Given a binary tree, find the most frequent subtree sum. If there is a tie
between the most frequent sum, you can return any one of them.

Example:

>>> tree = BinaryTree.from_tuples(((1,), 3, (-3,)))
>>> most_freq_subtree_sum(tree)
1

The above tree has 3 subtrees. The root node with 3, and the 2 leaf nodes, which
gives us a total of 3 subtree sums. The root node has a sum of 1 (3 + 1 + -3),
the left leaf node has a sum of 1, and the right leaf node has a sum of -3.
Therefore the most frequent subtree sum is 1.

>>> tree = BinaryTree.from_tuples(((2,), 4, (-4,)))
>>> most_freq_subtree_sum(tree)
2


"""

from ds.binary_tree import BinaryTree
from collections import Counter


def most_freq_subtree_sum_inner(root: BinaryTree[int]) -> tuple[int, Counter[int]]:
    match (root.left, root.right):
        case (None, None):
            return root.val, Counter({root.val: 1})
        case (child, None) | (None, child):
            child_sum, counter = most_freq_subtree_sum_inner(child)
            current_sum: int = root.val + child_sum
            counter[current_sum] += 1
            return current_sum, counter
        case (left, right):
            left_sum, left_counter = most_freq_subtree_sum_inner(left)
            right_sum, right_counter = most_freq_subtree_sum_inner(right)
            left_counter += right_counter
            current_sum: int = root.val + left_sum + right_sum
            left_counter[current_sum] += 1
            return current_sum, left_counter


def most_freq_subtree_sum(root: BinaryTree[int]) -> int:
    counter: Counter[int] = most_freq_subtree_sum_inner(root)[1]
    [(result_sum, _)] = counter.most_common(1)
    return result_sum


if __name__ == "__main__":
    import doctest

    doctest.testmod()
