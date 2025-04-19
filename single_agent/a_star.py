from typing import (
    Tuple,
    List,
    Callable,
)
import heapq
from dataclasses import dataclass

from common import (
    Node,
    Graph,
    Tree,
)


@dataclass
class ExpandNode:
    parent: "ExpandNode"
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
) -> Tuple[float, Tree]:
    source_node = graph.get_node(source_node_id)
    goal_node = graph.get_node(goal_node_id)

    def new_expand_node(parent:ExpandNode|None, value:Node, goal:Node, g_val:float) -> ExpandNode:
        return ExpandNode(parent, value, goal, g_val, h_func)

    open = [new_expand_node(None, source_node, goal_node, 0)]
    closed = {}
    while len(open) > 0:
        node = heapq.heappop(open)
        if node.id == goal_node_id:
            return (node.g_val, traceback(node))

        closed[node.id] = node
        for edge in graph.get_outbound_edges(node.id):
            weight = edge.get_weight()
            other_node = edge.get_other_node(node.id)
            new_g_val = node.g_val + weight
            if other_node.id not in closed or new_g_val < closed[other_node.id].g_val:
                heapq.heappush(open, new_expand_node(node, other_node, goal_node, new_g_val))

    return (float("inf"), [])

def traceback(node: ExpandNode) -> List[ExpandNode]:
    path = [node.id]
    while node.parent != None:
        path.append(node.parent.id)
        node = node.parent
    path.reverse()
    return path
