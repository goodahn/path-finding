import random
from unittest import TestCase
from typing import Dict

from single_agent.output_information import (
    OutputInformation,
    make_output_information_for_all_pair,
)
from single_agent.dynamic_problem import (
    decrease_edge_weight,
)
from utils.fixture import make_grid


class TestDecreaseEdgeWeight(TestCase):
    def test_with_grid(self):
        width, height = random.randint(3, 10), random.randint(3, 10)
        graph = make_grid(width, height)
        output_info_dict = make_output_information_for_all_pair(graph)
        
        for test_edge_id in random.sample(list(range(1, width*height)), 5):
            test_edge = graph.get_edge(test_edge_id)
            decrease_edge_weight(graph, output_info_dict, test_edge_id, test_edge.weight - 1)
        expected_output_info_dict = make_output_information_for_all_pair(graph)

        self._compare_output_info(expected=expected_output_info_dict, actual=output_info_dict)

    def _compare_output_info(self, expected: Dict[int, OutputInformation], actual: Dict[int, OutputInformation]):
        for node_id in expected.keys():
            expected_output_info = expected[node_id]
            actual_output_info = actual[node_id]

            self.assertDictEqual(
                expected_output_info.shortest_distance_dict,
                actual_output_info.shortest_distance_dict,
            )

