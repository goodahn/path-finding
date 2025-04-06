from dataclasses import dataclass
from typing import List, Dict, Set


@dataclass
class Node:
    id: int
    is_visited: bool = False


@dataclass
class Edge:
    id: int
    start_node: Node
    end_node: Node
    weight: float

    def get_weight(self) -> float:
        return self.weight

    def set_weight(self, weight: float):
        self.weight = weight

    def get_other_node(self, node_id: int) -> Node:
        if self.start_node.id == node_id:
            return self.end_node
        else:
            return self.start_node


class Graph:
    nodes: Dict[int, Node]
    edges: Dict[int, Edge]
    adjacent_edges: Dict[int, List[Edge]]

    def __init__(
        self,
        *,
        nodes: List[Node],
        edges: List[Edge] = None,
        adjacent_edges: Dict[int, List[Edge]] = None
    ):
        if edges == None and adjacent_edges == None:
            raise Exception("edges and adjacent_edges cannot be both None")

        self.nodes = {node.id: node for node in nodes}
        self.edges = {edge.id: edge for edge in edges}

        if adjacent_edges == None:
            adjacent_edges = self.__build_adjacent_edges_from_edges(self.edges)

        self.adjacent_edges = adjacent_edges

    def get_node(self, node_id: int) -> Node:
        return self.nodes[node_id]

    def get_edge(self, edge_id: int) -> Edge:
        return self.edges[edge_id]

    def set_node_visited(self, node_id: int):
        self.nodes[node_id].is_visited = True

    def get_connected_nodes(self, node_id: int) -> List[Node]:
        adjacent_edges = self.adjacent_edges.get(node_id, [])
        return [edge.get_other_node(node_id) for edge in adjacent_edges]

    def get_adjacent_edges(self, node_id: int) -> List[Edge]:
        return self.adjacent_edges.get(node_id, [])

    def update_local(
        self,
        shortest_distance_dict: Dict[int, Dict[int, float]],
        source_node_id: int,
        target_node_id: int,
    ):
        def backward(edge):
            return (
                shortest_distance_dict[source_node_id][edge.end_node.id] - edge.weight
            )

        self.adjacent_edges[target_node_id] = sorted(
            self.adjacent_edges[target_node_id],
            key=backward,
            reverse=True,
        )

    def __build_adjacent_edges_from_edges(
        self, edges: Dict[int, Edge]
    ) -> Dict[int, List[Edge]]:
        adjacent_edges: Dict[int, List[Edge]] = {}
        for edge_id in edges.keys():
            edge = edges[edge_id]
            node = edge.start_node
            try:
                adjacent_edges[node.id].append(edge)
            except:
                adjacent_edges[node.id] = [edge]
        return adjacent_edges
