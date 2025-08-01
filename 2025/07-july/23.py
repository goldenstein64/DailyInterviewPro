"""
Given an undirected graph, determine if a cycle exists in the graph.

Can you solve this in linear time, linear space?
"""

import unittest

type Graph = dict[str, Graph]


def _has_cycle_inner(
    parent: Graph, key: str, graph: Graph, visited: set[tuple[int, str, int]]
) -> bool:
    """
    checks whether a directed graph has a cycle. It's not an O(n) time or space
    algorithm since the same node can be visited multiple times under different
    keys or parents. The worst case can be O(inf) for something like
    `{ "a": shared, "b": shared, "c": shared, ... }`
    """
    # get the identity hash of this node along with its parent
    hashed = (id(parent), key, id(graph))
    if hashed in visited:
        return True

    visited.add(hashed)
    return any(_has_cycle_inner(graph, k, node, visited) for k, node in graph.items())


def has_cycle(graph: Graph) -> bool:
    visited: set[tuple[int, str, int]] = set()
    return any(_has_cycle_inner(graph, k, node, visited) for k, node in graph.items())


class Tests(unittest.TestCase):
    def test_empty(self):
        self.assertFalse(has_cycle({}))

    def test_one(self):
        self.assertFalse(has_cycle({"a": {}}))

    def test_tiny_cyclic(self):
        graph: Graph = {}
        graph["q"] = graph
        self.assertTrue(has_cycle(graph))

    def test_shared_acyclic(self):
        shared: Graph = {}
        graph: Graph = {"a": shared, "b": shared}
        self.assertFalse(has_cycle(graph))

    def test_disconnected_cyclic(self):
        graph: Graph = {"a": {"x": {}}, "b": {}}
        graph["b"]["self"] = graph["b"]
        self.assertTrue(has_cycle(graph))

    def test_acyclic(self):
        graph: Graph = {
            "a": {"a2": {}, "a3": {}},
            "b": {"b2": {}},
            "c": {},
        }
        self.assertFalse(has_cycle(graph))

    def test_cyclic(self):
        graph: Graph = {
            "a": {"a2": {}, "a3": {}},
            "b": {"b2": {}},
            "c": {},
        }
        graph["c"] = graph
        self.assertTrue(has_cycle(graph))


if __name__ == "__main__":
    unittest.main()
