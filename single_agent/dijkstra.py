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

    @property
    def id(self) -> int:
        return self.value.id
    
    def __lt__(self, other):
        return self.g_val < other.g_val


def find_shortest_path(
    graph: Graph,
    source_node_id: int,
    goal_node_id: int,
) -> Tuple[float, Tree]:
    source_node = graph.get_node(source_node_id)
    goal_node = graph.get_node(goal_node_id)

    def new_expand_node(parent:ExpandNode|None, value:Node, goal:Node, g_val:float) -> ExpandNode:
        return ExpandNode(parent, value, goal, g_val)

    open = [new_expand_node(None, source_node, goal_node, 0)]
    closed = {}
    while len(open) > 0:
        node = heapq.heappop(open)
        if node.id == goal_node_id:
            return (node.g_val, traceback(node))

        closed[node.id] = node
        for edge in graph.get_adjacent_edges(node.id):
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

if __name__ == "__main__":
    from common import Edge
    nodes = []
    for i in range(6):
        nodes.append(Node(id=i))

    edges = []
    edges.append(Edge(0, start_node=nodes[0], end_node=nodes[1], weight=3))
    edges.append(Edge(1, start_node=nodes[0], end_node=nodes[2], weight=1))
    edges.append(Edge(2, start_node=nodes[1], end_node=nodes[3], weight=1))
    edges.append(Edge(3, start_node=nodes[1], end_node=nodes[4], weight=1))
    edges.append(Edge(4, start_node=nodes[1], end_node=nodes[5], weight=10))
    edges.append(Edge(5, start_node=nodes[2], end_node=nodes[3], weight=1))
    edges.append(Edge(6, start_node=nodes[4], end_node=nodes[5], weight=1))

    graph = Graph(nodes=nodes, edges=edges)
    print(find_shortest_path(graph, 0, 5))