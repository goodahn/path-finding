from typing import (
    Tuple,
    List,
    Callable,
)
import heapq
import math
from dataclasses import dataclass

from common import (
    Node,
    Edge,
    Graph,
)

@dataclass
class PathNode:
    start: Node
    end: Node

    timestamp: int
    started_at: int

    def __init__(self, *, start: Node, end: Node, timestamp: int=-1, started_at: int=-1):
        self.start = start
        self.end = end
        self.timestamp = timestamp
        self.started_at = started_at

    def get_move_info(self) -> Tuple[int, int]:
        return (self.start.id, self.end.id)

@dataclass
class ExpandNode:
    parent: "ExpandNode|None"
    value: Node
    goal: Node
    g_val: float
    h_func: Callable

    @property
    def id(self) -> int:
        return self.value.id

    @property
    def f_val(self) -> float:
        return self.g_val + self.h_func(self)

    def __lt__(self, other):
        return self.f_val < other.f_val


def find_shortest_path(
    graph: Graph,
    source_node_id: int,
    goal_node_id: int,
    h_func: Callable,
) -> Tuple[float, List[PathNode]]:
    source_node = graph.get_node(source_node_id)
    goal_node = graph.get_node(goal_node_id)

    def new_expand_node(parent:ExpandNode|None, value:Node, goal:Node, g_val:float) -> ExpandNode:
        return ExpandNode(parent, value, goal, g_val, h_func)

    open = [new_expand_node(None, source_node, goal_node, 0)]
    closed = {}
    while len(open) > 0:
        node = heapq.heappop(open)
        if node.id == goal_node_id:
            return (node.g_val, make_space_time_path(graph, node))

        closed[node.id] = node
        for edge in graph.get_outbound_edges(node.id):
            weight = edge.get_weight()
            other_node = edge.get_other_node(node.id)
            new_g_val = node.g_val + weight
            if other_node.id not in closed or new_g_val < closed[other_node.id].g_val:
                heapq.heappush(open, new_expand_node(node, other_node, goal_node, new_g_val))

    return (float("inf"), [])


def make_space_time_path(graph: Graph, node: ExpandNode) -> List[PathNode]:
    path = []

    while node.parent != None:
        start  = node.parent.value
        end = node.value
        node = node.parent

        edge = graph.get_edge_by_node_id_pair(start.id, end.id)
        if edge is None:
            path.append(PathNode(start=start, end=end, started_at=len(path), timestamp=len(path)))
            continue

        for i in range(math.ceil(edge.get_weight())):
            path.append(PathNode(start=start, end=end, started_at=len(path), timestamp=len(path)))
    path.append(PathNode(start=graph.get_node(node.id), end=graph.get_node(node.id), started_at=len(path), timestamp=len(path)))
    path.reverse()
    prev_path_node = None
    started_at = 0
    for i in range(len(path)):
        path_node = path[i]
        if prev_path_node is not None and \
            prev_path_node.get_move_info() != path_node.get_move_info():
            started_at = i - 1

        path_node.started_at = started_at
        path_node.timestamp = len(path) - path_node.timestamp - 1
        prev_path_node = path_node
    return path

if __name__ == "__main__":
    nodes = []
    for i in range(6):
        nodes.append(Node(id=i + 1))

    edges = []
    edges.append(Edge(1, start_node=nodes[0], end_node=nodes[1], weight=3))
    edges.append(Edge(2, start_node=nodes[0], end_node=nodes[2], weight=1))
    edges.append(Edge(3, start_node=nodes[1], end_node=nodes[3], weight=1))
    edges.append(Edge(4, start_node=nodes[1], end_node=nodes[4], weight=1))
    edges.append(Edge(5, start_node=nodes[1], end_node=nodes[5], weight=10))
    edges.append(Edge(6, start_node=nodes[2], end_node=nodes[3], weight=1))
    edges.append(Edge(7, start_node=nodes[4], end_node=nodes[5], weight=1))

    graph = Graph(nodes=nodes, edges=edges)
    (_, space_time_path) = find_shortest_path(graph, nodes[0].id, nodes[-1].id, lambda x: 0)
    for path_node in space_time_path:
        edge = graph.get_edge_by_node_id_pair(path_node.start.id, path_node.end.id)
        weight = edge.get_weight() if edge is not None else 0
        print("current_time:", path_node.timestamp, "start:", path_node.start.id, "end:", path_node.end.id, "weight:", weight,"started_at:", path_node.started_at)