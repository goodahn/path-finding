import pprint
from common import (
    Node,
    Edge,
    Graph,
    Tree,
)
from single_agent.output_information import make_output_information_for_single_source

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
    output_info = make_output_information_for_single_source(graph, nodes[0])
    pprint.pprint(output_info.shortest_distance_dict)

    queue = [output_info.shortest_tree_dict[nodes[0].id]]
    while len(queue) > 0:
        node = queue.pop(0)
        msg = ""
        if node.parent is not None:
            msg += f"{node.parent.value.id}"
        else:
            msg += "root"
        msg += f" -> {node.value.id}"
        print(msg)
        for child in node.children:
            queue.append(child)
