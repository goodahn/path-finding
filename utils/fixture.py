from common import (
    Node,
    Edge,
    Graph,
)


def make_grid(width: int, height: int, unit: float) -> Graph:
    nodes = []
    for row_idx in range(height):
        for col_idx in range(width):
            nodes.append(Node(id=col_idx + row_idx * width))

    edges = []
    edge_id = 0
    for row_idx in range(height):
        for col_idx in range(width):
            node_id = col_idx + row_idx * width

            connected_node_ids = []
            if col_idx != 0:
                connected_node_ids.append(node_id - 1)
            if col_idx != width - 1:
                connected_node_ids.append(node_id + 1)
            if row_idx != 0:
                connected_node_ids.append(node_id - width)
            if row_idx != height - 1:
                connected_node_ids.append(node_id + width)

            for other_node_id in connected_node_ids:
                edges.append(
                    Edge(
                        id=edge_id,
                        start_node=nodes[node_id],
                        end_node=nodes[other_node_id],
                        weight=unit,
                    )
                )
                edge_id += 1
    graph = Graph(nodes=nodes, edges=edges)
    return graph
