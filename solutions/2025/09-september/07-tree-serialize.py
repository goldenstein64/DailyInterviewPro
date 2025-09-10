"""
You are given the root of a binary tree. You need to implement 2 functions:

1. serialize(root) which serializes the tree into a string representation
2. deserialize(s) which deserializes the string back to the original tree that
   it represents

Example:

>>> tuples = (((2,), 3, (5,)), 1, (4, (7,)))
>>> tree = BinaryTree.from_tuples(tuples)
>>> serialized = serialize_rec(tree)
>>> serialized
'1 3 2 # # 5 # # 4 # 7 # #'
>>> deserialize_rec(serialized) == tree
True
"""

from ds.binary_tree import BinaryTree, TupleBinaryTree
from collections.abc import Generator, Iterator, Callable
from itertools import islice, product
import unittest


def serialize_part(root: BinaryTree[int] | None) -> Generator[str]:
    if root is None:
        yield "#"
    else:
        yield str(root.val)
        yield from serialize_part(root.left)
        yield from serialize_part(root.right)


def serialize_rec(root: BinaryTree[int] | None) -> str:
    return " ".join(serialize_part(root))


def serialize_iter(root: BinaryTree[int] | None) -> str:
    if root is None:
        return "#"

    path: list[BinaryTree[int] | None] = [root]
    buffer: list[str] = []

    while path:
        current = path.pop()
        if current is None:
            buffer.append("#")
            continue

        buffer.append(str(current.val))
        path.append(current.right)
        path.append(current.left)

    return " ".join(buffer)


def deserialize_part(tokens: Iterator[str]) -> BinaryTree[int] | None:
    val = next(tokens)
    if val == "#":
        return None

    root = BinaryTree(int(val))
    root.left = deserialize_part(tokens)
    root.right = deserialize_part(tokens)
    return root


def deserialize_rec(data: str) -> BinaryTree[int] | None:
    return deserialize_part(iter(data.split()))


def deserialize_iter(data: str) -> BinaryTree[int] | None:
    str_vals: list[str] = data.split(" ")
    if str_vals[0] == "#":
        return None

    root: BinaryTree[int] = BinaryTree(int(str_vals[0]))
    path: list[tuple[BinaryTree[int], bool]] = [(root, True)]

    for str_val in islice(str_vals, 1, len(str_vals)):
        current, write_left = path[-1]
        if str_val == "#":
            if write_left:
                path[-1] = (current, False)
            else:
                path.pop()
        else:
            val: int = int(str_val)
            if write_left:
                left: BinaryTree[int] = BinaryTree(val)
                current.left = left
                path[-1] = (current, False)
                path.append((left, True))
            else:
                right: BinaryTree[int] = BinaryTree(val)
                current.right = right
                path[-1] = (right, True)

    return root


class Tests(unittest.TestCase):
    serializers: list[Callable[[BinaryTree[int] | None], str]] = [
        serialize_iter,
        serialize_rec,
    ]

    deserializers: list[Callable[[str], BinaryTree[int] | None]] = [
        deserialize_iter,
        deserialize_rec,
    ]

    cases: list[tuple[TupleBinaryTree[int] | None, str]] = [
        (None, "#"),
        ((1,), "1 # #"),
        ((1, (2,)), "1 # 2 # #"),
        (((1,), 2), "2 1 # # #"),
        (((1,), 2, (3,)), "2 1 # # 3 # #"),
        ((((1,), 2, (3,)), 4, ((5,), 6, (7,))), "4 2 1 # # 3 # # 6 5 # # 7 # #"),
        ((((2,), 3, (5,)), 1, (4, (7,))), "1 3 2 # # 5 # # 4 # 7 # #"),
    ]

    def test_cases(self):
        for serialize, deserialize, (tuples, data) in product(
            self.serializers, self.deserializers, self.cases
        ):
            ser = serialize.__name__
            with self.subTest(serialize=ser, root=tuples, data=data):
                root: BinaryTree[int] | None = None
                if tuples is not None:
                    root = BinaryTree.from_tuples(tuples)
                serialized = serialize(root)
                self.assertEqual(data, serialized)

            deser = deserialize.__name__
            with self.subTest(deserialize=deser, root=tuples, data=data):
                deserialized = deserialize(data)
                self.assertEqual(tuples, deserialized and deserialized.as_tuples())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
