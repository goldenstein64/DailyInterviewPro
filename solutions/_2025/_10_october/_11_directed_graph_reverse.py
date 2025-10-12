"""
Given a directed graph, reverse the directed graph so all directed edges are
reversed.

Example:

>>> c = GraphNode("c")
>>> b = GraphNode("b", [c])
>>> a = GraphNode("a", [b, c])
>>> graph = {
...     a.val: a,
...     b.val: b,
...     c.val: c,
... }
>>> { k: [n.val for n in v.adjacent] for k, v in reverse_graph(graph).items() }
{'a': [], 'b': ['a'], 'c': ['a', 'b']}
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GraphNode[T]:
    val: T
    adjacent: list[GraphNode[T]] = field(default_factory=lambda: [])


def reverse_graph[T](graph: dict[T, GraphNode[T]]) -> dict[T, GraphNode[T]]:
    """
    Reverse a directed graph.

    This uses O(V + E) time and O(V + E) space, where V is vertex count and E is
    edge count.
    """
    result: dict[T, GraphNode[T]] = {
        k: GraphNode(node.val, []) for k, node in graph.items()
    }

    for k, node in graph.items():
        result_node: GraphNode[T] = result[k]
        for adj in node.adjacent:
            result[adj.val].adjacent.append(result_node)

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
