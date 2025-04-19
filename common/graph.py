from dataclasses import dataclass, field
from typing import List, Dict, Set


@dataclass
class Node:
    id: int
    is_visited: bool = False

    inbound_edges: List["Edge"] = field(default_factory=list)
    outbound_edges: List["Edge"] = field(default_factory=list)

    def add_inbound_edge(self, edge: "Edge"):
        self.inbound_edges.append(edge)

    def add_outbound_edge(self, edge: "Edge"):
        self.outbound_edges.append(edge)

    def get_inbound_edges(self) -> List["Edge"]:
        return self.inbound_edges
    
    def get_outbound_edges(self) -> List["Edge"]:
        return self.outbound_edges


@dataclass
class Edge:
    id: int
    start_node: Node
    end_node: Node
    weight: float

    def __init__(self, id:int, start_node:Node, end_node:Node, weight:float):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.weight = weight

        self.start_node.add_outbound_edge(self)
        self.end_node.add_inbound_edge(self)

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

    def __init__(
        self,
        *,
        nodes: List[Node],
        edges: List[Edge] = None,
    ):
        self.nodes = {node.id: node for node in nodes}
        self.edges = {edge.id: edge for edge in edges}

    def get_node(self, node_id: int) -> Node:
        return self.nodes[node_id]

    def get_edge(self, edge_id: int) -> Edge:
        return self.edges[edge_id]

    def set_node_visited(self, node_id: int):
        self.nodes[node_id].is_visited = True

    def get_connected_nodes(self, node_id: int) -> List[Node]:
        adjacent_edges = self.adjacent_edges.get(node_id, [])
        return [edge.get_other_node(node_id) for edge in adjacent_edges]

    def get_outbound_edges(self, node_id: int) -> List[Edge]:
        return self.get_node(node_id).get_outbound_edges()
    
    def get_inbound_edges(self, node_id: int) -> List[Edge]:
        return self.get_node(node_id).get_inbound_edges()

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
