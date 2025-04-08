from typing import (
    Dict,
)

from common import (
    Graph,
)
from single_agent.output_information import (
    OutputInformation,
)

def make_output_information(
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
