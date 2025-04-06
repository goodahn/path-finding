from common import (
    Node,
    Edge,
    Graph,
    Tree,
)
from typing import (
    Tuple,
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


def make_output_information_for_single_source(
    graph: Graph, source_node: Node
) -> OutputInformation:
    output_info = OutputInformation(graph, source_node)

    for node in graph.nodes.values():
        for edge in graph.get_adjacent_edges(node.id):
            new_distance = (
                output_info.get_distance(edge.start_node.id) + edge.get_weight()
            )
            if new_distance >= output_info.get_distance(edge.end_node.id):
                continue

            output_info.set_distance(edge.end_node.id, new_distance)
            output_info.update_parent_of_node(
                node_id=edge.end_node.id, parent_id=edge.start_node.id
            )

    return output_info


def make_output_information_for_all_pair(
    graph: Graph,
) -> Dict[int, OutputInformation]:
    output_info_dict: Dict[int, OutputInformation] = {}
    for node in graph.nodes.values():
        output_info = OutputInformation(graph, node)

        for adjacent_edge in graph.get_adjacent_edges(node.id):
            other_node = adjacent_edge.get_other_node(node.id)
            output_info.set_distance(other_node.id, adjacent_edge.get_weight())
            output_info.update_parent_of_node(node_id=other_node.id, parent_id=node.id)

        output_info_dict[node.id] = output_info

    for pivot_node in graph.nodes.values():
        output_info_for_pivot_node = output_info_dict[pivot_node.id]
        for start_node in graph.nodes.values():
            output_info_for_start_node = output_info_dict[start_node.id]
            for end_node in graph.nodes.values():
                new_distance = output_info_for_start_node.get_distance(
                    pivot_node.id
                ) + output_info_for_pivot_node.get_distance(end_node.id)
                current_distance = output_info_for_start_node.get_distance(end_node.id)
                if new_distance >= current_distance:
                    continue

                output_info_for_start_node.set_distance(end_node.id, new_distance)
                output_info_for_start_node.update_parent_of_node(
                    node_id=end_node.id, parent_id=pivot_node.id
                )

    return output_info_dict
