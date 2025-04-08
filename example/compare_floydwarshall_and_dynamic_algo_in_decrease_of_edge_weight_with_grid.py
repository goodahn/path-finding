import sys
import time
import random


from single_agent import floyd_warshall
from single_agent.dynamic_problem import (
    decrease_edge_weight,
)

from utils.fixture import make_grid


if __name__ == "__main__":
    width, height = int(sys.argv[1]), int(sys.argv[2])
    start_time = time.time()
    graph = make_grid(width, height, 10)
    end_time = time.time()
    print(
        f"execution time of constructing {width}x{height} grid: {end_time - start_time} s"
    )
    start_time = time.time()
    output_info_dict = floyd_warshall.make_output_information(graph)
    end_time = time.time()
    print(f"execution time of floyd warshall: {end_time - start_time} s")

    start_time = time.time()
    for test_node_id in random.sample(list(range(width*height)), width*height//20*4):
        test_edges = graph.get_adjacent_edges(test_node_id)
        for test_edge in test_edges:
            decrease_edge_weight(graph, output_info_dict, test_edge.id, test_edge.weight - 1)
    end_time = time.time()
    print(
        f"execution time of dynamic algorithm in decrease of edge weight: {end_time - start_time} s"
    )
