import time
import pprint

from common import (
    Node,
    Edge,
    Graph,
    Tree,
)
from single_agent.output_information import (
    make_output_information_for_all_pair,
)
from single_agent.dynamic_problem import (
    decrease_edge_weight,
)


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
    start_time = time.time()
    output_info_dict = make_output_information_for_all_pair(graph)
    end_time = time.time()
    for node_id in sorted(output_info_dict.keys()):
        output_info = output_info_dict[node_id]
        pprint.pprint(output_info.shortest_distance_dict)
    print(f"execution time of floyd warshall: {end_time - start_time} s")

    for source_node in graph.nodes.values():
        queue = [output_info_dict[source_node.id].shortest_tree_dict[source_node.id]]
        while len(queue) > 0:
            tree = queue.pop(0)
            msg = ""
            if tree.parent is not None:
                msg += f"{tree.parent.value.id}"
            else:
                msg += "root"
            msg += f" -> {tree.value.id}"
            print(msg)
            for child in tree.children:
                queue.append(child)
        print("=========================")

    start_time = time.time()
    decrease_edge_weight(graph, output_info_dict, 5, 9)
    end_time = time.time()
    print("decrease edge weight", end_time - start_time)
    for source_node in graph.nodes.values():
        queue = [output_info_dict[source_node.id].shortest_tree_dict[source_node.id]]
        while len(queue) > 0:
            tree = queue.pop(0)
            msg = ""
            if tree.parent is not None:
                msg += f"{tree.parent.value.id} -> "
            else:
                msg += "root = "
            msg += f"{tree.value.id}"
            print(msg)
            for child in tree.children:
                queue.append(child)
        print("=========================")
