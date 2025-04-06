import sys
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

from .fixture import make_grid


if __name__ == "__main__":
    width, height = int(sys.argv[1]), int(sys.argv[2])
    start_time = time.time()
    graph = make_grid(width, height)
    end_time = time.time()
    print(
        f"execution time of constructing {width}x{height} grid: {end_time - start_time} s"
    )
    start_time = time.time()
    output_info_dict = make_output_information_for_all_pair(graph)
    end_time = time.time()
    print(f"execution time of floyd warshall: {end_time - start_time} s")

    start_time = time.time()
    decrease_edge_weight(graph, output_info_dict, 5, 9)
    end_time = time.time()
    print(
        f"execution time of dynamic algorithm in decrease of edge weight: {end_time - start_time} s"
    )
