r"""
You are given the preorder and inorder traversals of a binary tree in the form
of arrays. Write a function that reconstructs the tree represented by these
traversals.

Example:

>>> reconstruct(['a'], ['a']).as_tuples()
('a',)

>>> reconstruct(['a', 'b', 'c'], ['b', 'a', 'c']).as_tuples()
(('b',), 'a', ('c',))

>>> reconstruct(
...     preorder=['a', 'b', 'd', 'e', 'c', 'f', 'g'],
...     inorder=['d', 'b', 'e', 'a', 'f', 'c', 'g'],
... ).as_tuples()
((('d',), 'b', ('e',)), 'a', (('f',), 'c', ('g',)))
"""

from __future__ import annotations

import unittest
from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from itertools import count, product
from random import randint
from typing import Literal, overload

type TupleNode = (
    tuple[str]
    | tuple[TupleNode, str]
    | tuple[str, TupleNode]
    | tuple[TupleNode, str, TupleNode]
)


@dataclass
class Node:
    val: str
    left: Node | None = None
    right: Node | None = None

    def preorder(self) -> Generator[str]:
        yield self.val

        if self.left:
            yield from self.left.preorder()

        if self.right:
            yield from self.right.preorder()

    def inorder(self) -> Generator[str]:
        if self.left:
            yield from self.left.inorder()

        yield self.val

        if self.right:
            yield from self.right.inorder()

    def postorder(self) -> Generator[str]:
        if self.left:
            yield from self.left.postorder()

        if self.right:
            yield from self.right.postorder()

        yield self.val

    def preorder_iter(self) -> Generator[str]:
        stack: list[Node] = []
        current: Node | None = self

        while stack or current:
            while current:
                yield current.val
                if current.right:
                    stack.append(current.right)
                current = current.left

            if stack:
                current = stack.pop()

    def inorder_iter(self) -> Generator[str]:
        stack: list[Node] = []
        current: Node | None = self

        while stack or current:
            while current:
                stack.append(current)
                current = current.left

            current = stack.pop()
            yield current.val

            current = current.right

    def postorder_iter(self) -> Generator[str]:
        stack: list[Node] = []
        current: Node | None = self
        last_visited: Node | None = None

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
    def from_tuples(tuples: TupleNode) -> Node:
        match tuples:
            case (str(val),):
                return Node(val, None, None)
            case (tuple(left), str(val)):
                return Node(val, Node.from_tuples(left), None)
            case (str(val), tuple(right)):
                return Node(val, None, Node.from_tuples(right))
            case (tuple(left), str(val), tuple(right)):
                return Node(val, Node.from_tuples(left), Node.from_tuples(right))

    def as_tuples(self) -> TupleNode:
        match self:
            case Node(val, None, None):
                return (val,)
            case Node(val, Node() as left, None):
                return (left.as_tuples(), val)
            case Node(val, None, Node() as right):
                return (val, right.as_tuples())
            case Node(val, Node() as left, Node() as right):
                return (left.as_tuples(), val, right.as_tuples())
            case _:
                raise ValueError("unknown Node structure")


class ListView[T](Sequence[T]):
    def __init__(self, data: Sequence[T], view: Sequence[int] | None = None):
        self.data: Sequence[T] = data
        self.view: Sequence[int] = range(len(data)) if view is None else view

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> ListView[T]: ...
    def __getitem__(self, index: int | slice) -> T | ListView[T]:
        if type(index) == slice:
            return ListView(self.data, self.view[index])
        else:
            return self.data[self.view[index]]

    def __len__(self) -> int:
        return len(self.view)


def reconstruct_inner_lookup(
    preorder: Sequence[str],
    inorder: Sequence[str],
    lookup: dict[str, int],
    lookup_offset: int = 0,
) -> Node:
    val = preorder[0]
    inorder_root = lookup[val] - lookup_offset
    left: Node | None = None
    if inorder_root > 0:
        # there is a left child
        # len(inorder_left) == inorder_root
        inorder_left = inorder[:inorder_root]
        preorder_left = preorder[1 : inorder_root + 1]
        left = reconstruct_inner_lookup(
            preorder_left, inorder_left, lookup, lookup_offset
        )

    right: Node | None = None
    if inorder_root < len(inorder) - 1:
        # there is a right child
        # len(inorder_right) == len(inorder) - inorder_root
        inorder_right = inorder[inorder_root + 1 :]
        preorder_right = preorder[inorder_root + 1 :]
        right = reconstruct_inner_lookup(
            preorder_right, inorder_right, lookup, lookup_offset + inorder_root + 1
        )

    return Node(val, left, right)


def reconstruct_inner(preorder: Sequence[str], inorder: Sequence[str]) -> Node:
    val = preorder[0]
    inorder_root = inorder.index(val)
    left: Node | None = None
    if inorder_root > 0:
        # there is a left child
        # len(inorder_left) == inorder_root
        inorder_left = inorder[:inorder_root]
        preorder_left = preorder[1 : inorder_root + 1]
        left = reconstruct_inner(preorder_left, inorder_left)

    right: Node | None = None
    if inorder_root < len(inorder) - 1:
        # there is a right child
        # len(inorder_right) == len(inorder) - inorder_root
        inorder_right = inorder[inorder_root + 1 :]
        preorder_right = preorder[inorder_root + 1 :]
        right = reconstruct_inner(
            preorder_right,
            inorder_right,
        )

    return Node(val, left, right)


def reconstruct(preorder: Sequence[str], inorder: Sequence[str]) -> Node:
    """
    Create a tree from a list of preorder and inorder elements. This
    implementation is not well-optimized!

    I think this has O(n) time complexity and O(n) space.
    """
    # return reconstruct_inner_lookup(
    #     preorder, inorder, {v: i for i, v in enumerate(inorder)}
    # )
    return reconstruct_inner(preorder, inorder)


def reconstruct_view(preorder: Sequence[str], inorder: Sequence[str]) -> Node:
    """
    Create a tree from a list of preorder and inorder elements. This replaces
    both lists with a more performant view implementation that reduces the
    amount of copying done.

    This has O(n) time complexity (?) and O(log n) space (from the call stack).
    """
    return reconstruct(ListView(preorder), ListView(inorder))


class Fuzz:
    @staticmethod
    def find_rand_leaf(root: Node) -> tuple[Node, bool]:
        last_node: Node = root
        node: Node | None = root
        left: bool = False
        while node:
            last_node = node
            left = randint(1, 2) == 1
            if left:
                node = node.left
            else:
                node = node.right

        return last_node, left

    @staticmethod
    def gen_rand_node(size: int) -> Node:
        values = map(str, count(1))
        root: Node = Node(next(values))

        for _ in range(size - 1):
            leaf, add_left = Fuzz.find_rand_leaf(root)

            new_node: Node = Node(next(values))
            if add_left:
                leaf.left = new_node
            else:
                leaf.right = new_node

        return root

    @staticmethod
    def gen_rand_skewed_node(size: int) -> Node:
        values = map(str, count(1))
        root: Node = Node(next(values))

        node: Node = root
        for _ in range(size - 1):
            new_node: Node = Node(next(values))
            setattr(node, "left" if randint(1, 2) == 1 else "right", new_node)
            node = new_node

        return root

    @staticmethod
    def gen_skewed_node(size: int, left: bool = False) -> Node:
        values = map(str, count(1))
        root: Node = Node(next(values))

        attr: Literal["left", "right"] = "left" if left else "right"
        node: Node = root
        for _ in range(size - 1):
            new_node: Node = Node(next(values))
            setattr(node, attr, new_node)
            node = new_node

        return root


class Tests(unittest.TestCase):
    solutions: list[Callable[[list[str], list[str]], Node]] = [
        reconstruct,
        reconstruct_view,
    ]

    cases: list[tuple[list[str], list[str], TupleNode]] = [
        (["a"], ["a"], ("a",)),
        (["a", "b", "c"], ["b", "a", "c"], (("b",), "a", ("c",))),
        (
            ["a", "b", "d", "e", "c", "f", "g"],
            ["d", "b", "e", "a", "f", "c", "g"],
            ((("d",), "b", ("e",)), "a", (("f",), "c", ("g",))),
        ),
        (
            ["a", "b", "c", "d", "e"],
            ["e", "d", "c", "b", "a"],
            (((((("e",), "d"), "c"), "b"), "a")),
        ),
        (
            ["a", "b", "c", "d", "e"],
            ["a", "b", "c", "d", "e"],
            ("a", ("b", ("c", ("d", ("e",))))),
        ),
    ]

    def test_cases(self):
        for solution, (preorder, inorder, expected) in product(
            self.solutions, self.cases
        ):
            sol = solution.__name__
            with self.subTest(
                solution=sol, preorder=preorder, inorder=inorder, expected=expected
            ):
                self.assertEqual(
                    Node.from_tuples(expected), solution(preorder, inorder)
                )

    def test_fuzz(self):
        for _ in range(100):
            root: Node = Fuzz.gen_rand_node(size=randint(1, 100))

            preorder: list[str] = list(root.preorder())
            inorder: list[str] = list(root.inorder())
            expected: Node = root
            for solution in self.solutions:
                sol = solution.__name__
                with self.subTest(
                    solution=sol, preorder=preorder, inorder=inorder, expected=expected
                ):
                    self.assertEqual(expected, solution(preorder, inorder))

    def test_preorder(self):
        node = Fuzz.gen_rand_node(size=10_000)
        preorder1 = list(node.preorder())
        preorder2 = list(node.preorder_iter())
        self.assertEqual(preorder1, preorder2)

    def test_inorder(self):
        node = Fuzz.gen_rand_node(size=10_000)
        inorder1 = list(node.inorder())
        inorder2 = list(node.inorder_iter())
        self.assertEqual(inorder1, inorder2)

    def test_postorder(self):
        node = Fuzz.gen_rand_node(size=10_000)
        postorder1 = list(node.postorder())
        postorder2 = list(node.postorder_iter())
        self.assertEqual(postorder1, postorder2)


if __name__ == "__main__":
    # import doctest

    # doctest.testmod()
    # unittest.main()

    from timeit import timeit

    def time_reconstruct(gen: Callable[[int], Node], size: int, trials: int) -> None:
        print(f"time_reconstruct(gen={gen.__name__}, size={size}, trials={trials})")
        print("  creating node...", end="\r")
        node = gen(size)

        print("  creating traversals...", end="\r")
        preorder = list(node.preorder_iter())
        inorder = list(node.inorder_iter())

        print("  timing reconstruct_view...", end="\r")
        print(
            f"  reconstruct_view: {timeit(stmt=lambda: reconstruct_view(preorder, inorder), number=trials)}"
        )
        print("  timing reconstruct...", end="\r")
        print(
            f"  reconstruct: {timeit(stmt=lambda: reconstruct(preorder, inorder), number=trials)}"
        )

    time_reconstruct(gen=Fuzz.gen_rand_skewed_node, size=990, trials=100)
    time_reconstruct(gen=Fuzz.gen_rand_node, size=10, trials=100_000)
    time_reconstruct(gen=Fuzz.gen_rand_node, size=100, trials=10_000)
    time_reconstruct(gen=Fuzz.gen_rand_node, size=1_000, trials=1_000)
    time_reconstruct(gen=Fuzz.gen_rand_node, size=10_000, trials=100)
    time_reconstruct(gen=Fuzz.gen_rand_node, size=100_000, trials=10)
