from typing import Dict

from common import (
    Node,
    Graph,
)
from single_agent.output_information import (
    OutputInformation,
)

def make_output_information(
    graph: Graph, source_node: Node
) -> OutputInformation:
    output_info = OutputInformation(graph, source_node)

    for _ in range(len(graph.nodes) - 1):
        for edge in graph.edges.values():
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

def make_output_information_for_all_source(graph: Graph) -> Dict[int, OutputInformation]:
    output_info_dict: Dict[int, OutputInformation] = {}
    for node in graph.nodes.values():
        output_info_dict[node.id] = make_output_information(graph, node)
    return output_info_dict