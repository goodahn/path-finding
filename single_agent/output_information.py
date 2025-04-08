from common import (
    Node,
    Graph,
    Tree,
)
from typing import (
    Dict,
)


class OutputInformation:
    shortest_distance_dict: Dict[int, float]
    shortest_tree_dict: Dict[int, Tree]

    def __init__(self, graph: Graph, source_node: Node):
        self.shortest_distance_dict: Dict[int, float] = {}
        self.shortest_tree_dict: Dict[int, Tree] = {}

        for node in graph.nodes.values():
            self.shortest_distance_dict[node.id] = float("inf")
            self.shortest_tree_dict[node.id] = Tree(node)

        self.shortest_distance_dict[source_node.id] = 0

    def get_distance(self, node_id: int) -> float:
        return self.shortest_distance_dict[node_id]

    def set_distance(self, node_id: int, distance: float):
        self.shortest_distance_dict[node_id] = distance

    def update_parent_of_node(self, *, node_id: int, parent_id: int):
        parent_tree = self.shortest_tree_dict[parent_id]
        child_tree = self.shortest_tree_dict[node_id]
        child_tree.set_parent(parent_tree)




