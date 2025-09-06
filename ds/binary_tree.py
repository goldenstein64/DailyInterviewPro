from __future__ import annotations

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
    val: T
    left: BinaryTree[T] | None = None
    right: BinaryTree[T] | None = None

    def preorder(self) -> Generator[T]:
        yield self.val

        if self.left:
            yield from self.left.preorder()

        if self.right:
            yield from self.right.preorder()

    def inorder(self) -> Generator[T]:
        if self.left:
            yield from self.left.inorder()

        yield self.val

        if self.right:
            yield from self.right.inorder()

    def postorder(self) -> Generator[T]:
        if self.left:
            yield from self.left.postorder()

        if self.right:
            yield from self.right.postorder()

        yield self.val

    def preorder_iter(self) -> Generator[T]:
        stack: list[BinaryTree[T]] = []
        current: BinaryTree[T] | None = self

        while stack or current:
            while current:
                yield current.val
                if current.right:
                    stack.append(current.right)
                current = current.left

            if stack:
                current = stack.pop()

    def inorder_iter(self) -> Generator[T]:
        stack: list[BinaryTree[T]] = []
        current: BinaryTree[T] | None = self

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            yield current.val

            current = current.right

    def postorder_iter(self) -> Generator[T]:
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
                    yield last.val
                    last_visited = stack.pop()

    @staticmethod
    def from_tuples[U](tuples: TupleBinaryTree[U]) -> BinaryTree[U]:
        match tuples:
            case (val,):
                return BinaryTree(val, None, None)
            case (left, right):
                if type(left) == tuple:
                    return BinaryTree(
                        cast(U, right),
                        BinaryTree.from_tuples(cast(TupleBinaryTree[U], left)),
                        None,
                    )
                else:
                    return BinaryTree(
                        cast(U, left),
                        None,
                        BinaryTree.from_tuples(cast(TupleBinaryTree[U], right)),
                    )
            case (tuple(left), val, tuple(right)):
                return BinaryTree(
                    val, BinaryTree.from_tuples(left), BinaryTree.from_tuples(right)
                )

    def as_tuples(self) -> TupleBinaryTree[T]:
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
