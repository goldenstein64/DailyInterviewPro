from __future__ import annotations

from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from typing import cast

type TupleBinaryTree[T] = (
    tuple[T]
    | tuple[TupleBinaryTree[T], T]
    | tuple[T, TupleBinaryTree[T]]
    | tuple[TupleBinaryTree[T], T, TupleBinaryTree[T]]
)


@dataclass
class BinaryTree[T]:
    """a container for a binary tree"""

    val: T
    left: BinaryTree[T] | None = None
    right: BinaryTree[T] | None = None
    parent: BinaryTree[T] | None = None

    @staticmethod
    def from_tuples[U](
        tuples: TupleBinaryTree[U], parent: BinaryTree[U] | None = None
    ) -> BinaryTree[U]:
        """
        Produce a tree from a tuple tree. This can be used to produce trees from
        a short-form representation.

        Examples:

        >>> BinaryTree.from_tuples((3,))
        BinaryTree(val=3, left=None, right=None)
        >>> BinaryTree.from_tuples(((1,), 2, (3,)))
        BinaryTree(val=2, left=BinaryTree(val=1, left=None, right=None), right=BinaryTree(val=3, left=None, right=None))
        """
        match tuples:
            case (val,):
                return BinaryTree(val, parent=parent)
            case (left, right):
                if type(left) == tuple:
                    tree = BinaryTree(cast(U, right), parent=parent)
                    tree.left = BinaryTree.from_tuples(
                        cast(TupleBinaryTree[U], left), parent=tree
                    )
                    return tree
                else:
                    tree = BinaryTree(cast(U, left), parent=parent)
                    tree.right = BinaryTree.from_tuples(
                        cast(TupleBinaryTree[U], right), parent=tree
                    )
                    return tree
            case (tuple(left), val, tuple(right)):
                tree = BinaryTree(val, parent=parent)
                tree.left = BinaryTree.from_tuples(left, parent=tree)
                tree.right = BinaryTree.from_tuples(right, parent=tree)
                return tree

    def as_tuples(self) -> TupleBinaryTree[T]:
        """
        Produce a tuple tree from this tree. This can be used to produce a
        short-form representation of a tree.

        Examples:

        >>> BinaryTree(val=3).as_tuples()
        (3,)
        >>> BinaryTree(left=BinaryTree(1), val=2).as_tuples()
        ((1,), 2)
        >>> BinaryTree(val=1, right=BinaryTree(2)).as_tuples()
        (1, (2,))
        >>> BinaryTree(left=BinaryTree(1), val=2, right=BinaryTree(3)).as_tuples()
        ((1,), 2, (3,))
        """
        match self:
            case BinaryTree(val, None, None):
                return (val,)
            case BinaryTree(val, BinaryTree() as left, None):
                return (left.as_tuples(), val)
            case BinaryTree(val, None, BinaryTree() as right):
                return (val, right.as_tuples())
            case BinaryTree(val, BinaryTree() as left, BinaryTree() as right):
                return (left.as_tuples(), val, right.as_tuples())
            case _:
                raise ValueError("unknown Node structure")

    def preorder_values_rec(self) -> Generator[T]:
        return (node.val for node in self.preorder_rec())

    def preorder_rec(self) -> Generator[BinaryTree[T]]:
        """Perform a recursive preorder traversal of this tree."""
        yield self

        if self.left:
            yield from self.left.preorder_rec()

        if self.right:
            yield from self.right.preorder_rec()

    def inorder_values_rec(self) -> Generator[T]:
        return (node.val for node in self.inorder_rec())

    def inorder_rec(self) -> Generator[BinaryTree[T]]:
        """Perform a recursive inorder traversal of this tree."""
        if self.left:
            yield from self.left.inorder_rec()

        yield self

        if self.right:
            yield from self.right.inorder_rec()

    def postorder_values_rec(self) -> Generator[T]:
        return (node.val for node in self.postorder_rec())

    def postorder_rec(self) -> Generator[BinaryTree[T]]:
        """Perform a recursive postorder traversal of this tree."""
        if self.left:
            yield from self.left.postorder_rec()

        if self.right:
            yield from self.right.postorder_rec()

        yield self

    def preorder_values(self) -> Generator[T]:
        return (node.val for node in self.preorder())

    def preorder(self) -> Generator[BinaryTree[T]]:
        """Perform an iterative preorder traversal of this tree."""
        stack: list[BinaryTree[T]] = []
        current: BinaryTree[T] | None = self

        while stack or current:
            while current:
                yield current
                if current.right:
                    stack.append(current.right)
                current = current.left

            if stack:
                current = stack.pop()

    def inorder_values(self) -> Generator[T]:
        return (node.val for node in self.inorder())

    def inorder(self) -> Generator[BinaryTree[T]]:
        """Perform an iterative inorder traversal of this tree."""
        stack: list[BinaryTree[T]] = []
        current: BinaryTree[T] | None = self

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            yield current

            current = current.right

    def postorder_values(self) -> Generator[T]:
        return (node.val for node in self.postorder())

    def postorder(self) -> Generator[BinaryTree[T]]:
        """Perform an iterative postorder traversal of this tree."""
        stack: list[BinaryTree[T]] = []
        current: BinaryTree[T] | None = self
        last_visited: BinaryTree[T] | None = None

        while stack or current:
            if current:
                stack.append(current)
                current = current.left
            else:
                last = stack[-1]
                if last.right and last_visited != last.right:
                    current = last.right
                else:
                    yield last
                    last_visited = stack.pop()

    def depth_walk(self) -> Generator[BinaryTree[T]]:
        nodes: list[BinaryTree[T]] = [self]
        while nodes:
            node = nodes.pop()
            yield node

            if left := node.left:
                nodes.append(left)

            if right := node.right:
                nodes.append(right)

    def breadth_walk(self) -> Generator[BinaryTree[T]]:
        nodes: deque[BinaryTree[T]] = deque()
        nodes.append(self)
        while nodes:
            node = nodes.popleft()
            yield node

            if left := node.left:
                nodes.append(left)

            if right := node.right:
                nodes.append(right)

    def ancestors(self) -> Generator[BinaryTree[T]]:
        ancestor: BinaryTree[T] | None = self
        while ancestor:
            yield ancestor
            ancestor = ancestor.parent

    def path(self, path: str) -> BinaryTree[T]:
        node: BinaryTree[T] = self
        for c in path:
            match c:
                case "L":
                    node = cast(BinaryTree[T], node.left)
                case "R":
                    node = cast(BinaryTree[T], node.right)
                case _:
                    raise ValueError(f"'{c}' is not 'L' or 'R'")

        return node


if __name__ == "__main__":
    import doctest

    doctest.testmod()
