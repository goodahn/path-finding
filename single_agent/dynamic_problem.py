from typing import Dict
import heapq

from common import (
    Graph,
    Edge,
)
from single_agent.output_information import (
    OutputInformation,
)


def decrease_edge_weight(
    graph: Graph,
    output_info_dict: Dict[int, OutputInformation],
    edge_id: int,
    amount: int,
):
    edge = graph.get_edge(edge_id=edge_id)
    if amount >= edge.weight:
        raise Exception("edge.weight cannot be zero or negative value")

    edge.set_weight(edge.weight - amount)

    for source_node in graph.nodes.values():
        decrease_edge_weight_for_single_source(
            graph,
            output_info_dict[source_node.id],
            edge,
        )


def decrease_edge_weight_for_single_source(
    graph: Graph,
    output_info: OutputInformation,
    edge: Edge,
):
    start_node = edge.start_node
    end_node = edge.end_node

    current_distance = output_info.get_distance(end_node.id)
    new_distance = output_info.get_distance(start_node.id) + edge.weight
    if new_distance >= current_distance:
        return

    output_info.set_distance(end_node.id, new_distance)
    output_info.update_parent_of_node(node_id=end_node.id, parent_id=start_node.id)

    queue = [[output_info.get_distance(end_node.id), end_node]]
    queue_dict = {end_node.id: queue[0]}
    while len(queue) > 0:
        [d, node] = heapq.heappop(queue)
        del queue_dict[node.id]
        for edge in graph.get_adjacent_edges(node.id):
            current_distance = output_info.get_distance(edge.end_node.id)
            new_distance = output_info.get_distance(node.id) + edge.weight
            if new_distance >= current_distance:
                continue

            output_info.set_distance(edge.end_node.id, new_distance)
            output_info.update_parent_of_node(edge.end_node.id, node.id)

            if edge.end_node.id not in queue_dict:
                c = [output_info.get_distance(edge.end_node.id), edge.end_node.id]
                heapq.heappush(c)
                queue_dict[edge.end_node.id] = c
            else:
                queue_dict[edge.end_node.id][0] = output_info.get_distance(
                    edge.end_node.id
                )
