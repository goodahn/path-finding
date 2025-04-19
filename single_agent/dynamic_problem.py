from typing import Dict, Any
import heapq
from dataclasses import dataclass, field

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


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


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

    queue = [
        PrioritizedItem(
            priority=output_info.get_distance(end_node.id),
            item=end_node,
        ),
    ]
    queue_dict = {end_node.id: queue[0]}
    while len(queue) > 0:
        current_item = heapq.heappop(queue)
        current_node = current_item.item
        del queue_dict[current_node.id]

        for edge in graph.get_outbound_edges(current_node.id):
            current_distance = output_info.get_distance(edge.end_node.id)
            new_distance = output_info.get_distance(current_node.id) + edge.weight
            if new_distance >= current_distance:
                continue

            output_info.set_distance(edge.end_node.id, new_distance)
            output_info.update_parent_of_node(
                node_id=edge.end_node.id, parent_id=current_node.id
            )

            if edge.end_node.id not in queue_dict:
                item = PrioritizedItem(
                    priority=output_info.get_distance(edge.end_node.id),
                    item=edge.end_node,
                )
                heapq.heappush(queue, item)
                queue_dict[edge.end_node.id] = item
            else:
                queue_dict[edge.end_node.id].item.priority = output_info.get_distance(
                    edge.end_node.id
                )

WHITE = 0
PINK = 1
RED = 2

def increase_edge_weight(
    graph: Graph,
    output_info_dict: Dict[int, OutputInformation],
    edge_id: int,
    amount: int,
):
    edge = graph.get_edge(edge_id=edge_id)
    if amount <= 0:
        raise Exception("amount cannot be zero or negative value")

    edge.set_weight(edge.weight + amount)

    for source_node in graph.nodes.values():
        increase_edge_weight_for_single_source(
            graph,
            output_info_dict[source_node.id],
            edge,
        )

def increase_edge_weight_for_single_source(
    graph: Graph,
    output_info: OutputInformation,
    edge: Edge,
):
    # Step 1
    shortest_tree_dict = output_info.shortest_tree_dict
    start_node = edge.start_node
    end_node = edge.end_node
    
    if start_node.id not in shortest_tree_dict or end_node.id not in [t.value.id for t in shortest_tree_dict[start_node.id].get_children()]:
        return

    color_dict = {}
    m = [
        PrioritizedItem(
            priority=output_info.get_distance(end_node.id),
            item=end_node,
        ),
    ]

    # Step 2
    count = 0
    trace = []
    while len(m) > 0:
        count +=1
        if count > 20:
            break
        current_item = heapq.heappop(m)
        source_node = current_item.item
        trace.append([source_node.id, []])
        is_non_red_neighbor = False
        for adjacent_edge in graph.get_inbound_edges(source_node.id):
            sink_node = adjacent_edge.get_other_node(source_node.id)
            if color_dict.get(sink_node.id, -1) == RED:
                continue
            if output_info.get_distance(sink_node.id) + adjacent_edge.get_weight() == output_info.get_distance(source_node.id):
                color_dict[source_node.id] = PINK
                output_info.update_parent_of_node(node_id=source_node.id, parent_id=sink_node.id)
                is_non_red_neighbor = True
        
        if not is_non_red_neighbor:
            color_dict[source_node.id] = RED
            for child in output_info.get_children(source_node.id):
                trace[-1][1].append(child.value.id)
                item = PrioritizedItem(
                    priority=output_info.get_distance(child.value.id),
                    item=child.value,
                )
                heapq.heappush(m, item)

    # Step 3.a
    q = []
    q_dict = {}
    for node_id, color in color_dict.items():
        if color != RED:
            continue
        source_node = graph.get_node(node_id)

        output_info.set_distance(node_id=source_node.id, distance=float("inf"))
        output_info.remove_parent_of_node(node_id=source_node.id)

        best_distance = float("inf")
        for adjacent_edge in graph.get_inbound_edges(source_node.id):
            sink_node = adjacent_edge.get_other_node(source_node.id)
            if sink_node.id in color_dict and color_dict[sink_node.id] == RED:
                continue
            new_distance = output_info.get_distance(sink_node.id) + adjacent_edge.get_weight()
            if new_distance < best_distance:
                best_distance = new_distance
                output_info.set_distance(source_node.id, best_distance)
                output_info.update_parent_of_node(node_id=source_node.id, parent_id=sink_node.id)

        item = PrioritizedItem(
            priority=output_info.get_distance(source_node.id),
            item=graph.get_node(source_node.id),
        )
        heapq.heappush(q, item)
        q_dict[source_node.id] = item

    # Step 3.b
    while len(q) > 0:
        current_item = heapq.heappop(q)
        source_node = current_item.item
        del q_dict[source_node.id]

        for adjacent_edge in graph.get_outbound_edges(source_node.id):
            sink_node = adjacent_edge.get_other_node(source_node.id)
            if sink_node.id not in color_dict or color_dict[sink_node.id] != RED:
                continue
            new_distance = output_info.get_distance(source_node.id) + adjacent_edge.get_weight()
            if new_distance >= output_info.get_distance(sink_node.id):
                continue
            output_info.set_distance(sink_node.id, new_distance)
            output_info.update_parent_of_node(node_id=sink_node.id, parent_id=source_node.id)
            if sink_node.id in q_dict:
                q_dict[sink_node.id].priority = new_distance
                heapq.heapify(q)
            else:
                item = PrioritizedItem(
                    priority=output_info.get_distance(sink_node.id),
                    item=graph.get_node(sink_node.id),
                )
                heapq.heappush(q, item)
                q_dict[source_node.id] = item


