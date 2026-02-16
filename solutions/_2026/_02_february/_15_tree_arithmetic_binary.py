"""
You are given a binary tree representation of an arithmetic expression. In this
tree, each leaf is an integer value, and a non-leaf node is one of the four
operations: '+', '-', '*', or '/'.

Write a function that takes this tree and evaluates the expression.

Example:

>>> tree = from_tuples((((3,), '+', (2,)), '*', ((4,), '+', (5,))))

>>> evaluate(tree)
45
"""

from __future__ import annotations

from typing import Literal
from dataclasses import dataclass

type Operation = Literal["+", "-", "*", "/"]
type ArithmeticTree = OperationNode | float
type ArithmeticTuple = (
    tuple[float] | tuple[ArithmeticTuple, Operation, ArithmeticTuple]
)


@dataclass
class OperationNode:
    op: Operation
    left: ArithmeticTree
    right: ArithmeticTree


def from_tuples(tup: ArithmeticTuple) -> ArithmeticTree:
    match tup:
        case (float(val) | int(val),):
            return val
        case (tuple(left), str(op), tuple(right)):
            return OperationNode(op, from_tuples(left), from_tuples(right))


def evaluate(tree: ArithmeticTree) -> float:
    match tree:
        case float(val) | int(val):
            return val
        case OperationNode(op, left, right):
            match op:
                case "+":
                    return evaluate(left) + evaluate(right)
                case "-":
                    return evaluate(left) - evaluate(right)
                case "*":
                    return evaluate(left) * evaluate(right)
                case "/":
                    return evaluate(left) / evaluate(right)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
