"""
A k-ary tree is a tree with k-children, and a tree is symmetrical if the data of the left side of the tree is the same as the right side of the tree.

Example:

>>> tree = KTree(
...     val=4,
...     children=[
...         KTree(
...             val=3,
...             children=[KTree(9), KTree(4), KTree(1)],
...         ),
...         KTree(
...             val=3,
...             children=[KTree(1), KTree(4), KTree(9)],
...         ),
...     ],
... )
>>> is_symmetric(tree)
True
"""

from __future__ import annotations

import unittest
from dataclasses import dataclass, field


@dataclass
class KTree:
    val: int
    children: list[KTree] = field(default_factory=lambda: [])


def inverted(tree: KTree) -> KTree:
    return KTree(
        val=tree.val,
        children=list_inverted(tree.children),
    )


def list_inverted(trees: list[KTree]) -> list[KTree]:
    return list(map(inverted, reversed(trees)))


def is_symmetric(root: KTree) -> bool:
    """
    determine whether a K-ary tree is symmetric. This uses a simple algorithm
    that inverts one side of the tree and compares it to the other.

    This has O(n) time complexity and O(n) space.
    """
    n: int = len(root.children)
    if not root.children:
        return True
    elif n == 1:
        return is_symmetric(root.children[0])
    elif n % 2 == 0:  # even number children
        left_side: list[KTree] = root.children[: n // 2]
        right_side: list[KTree] = root.children[n // 2 :]
        return list_inverted(left_side) == right_side
    else:  # odd number of children
        left_side: list[KTree] = root.children[: n // 2]
        center: KTree = root.children[n // 2]
        right_side: list[KTree] = root.children[n // 2 + 1 :]
        return list_inverted(left_side) == right_side and is_symmetric(center)


class Tests(unittest.TestCase):
    cases: list[tuple[KTree, bool]] = [
        (KTree(1), True),
        (KTree(2, [KTree(1)]), True),
        (KTree(2, [KTree(1), KTree(1)]), True),
        (KTree(2, [KTree(1), KTree(2)]), False),
        (KTree(2, [KTree(1), KTree(1), KTree(1)]), True),
        (KTree(2, [KTree(1), KTree(3), KTree(1)]), True),
        (KTree(2, [KTree(1), KTree(2), KTree(3)]), False),
    ]

    def test_cases(self):
        for root, expected in self.cases:
            with self.subTest(root=root, expected=expected):
                self.assertEqual(expected, is_symmetric(root))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
