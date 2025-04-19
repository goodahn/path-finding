import random
from unittest import TestCase
from typing import Dict

from single_agent.output_information import OutputInformation
from single_agent import (
    bellman_ford,
    floyd_warshall,
)
from utils.fixture import make_grid


class TestDecreaseEdgeWeight(TestCase):
    def test_with_grid(self):
        width, height = random.randint(3, 10), random.randint(3, 10)
        graph = make_grid(width, height, 10)
        output_info_dict_by_bellman_ford = bellman_ford.make_output_information_for_all_source(graph)
        output_info_dict_by_floyd_warshall = floyd_warshall.make_output_information(graph)
        
        self._compare_output_info(expected=output_info_dict_by_bellman_ford, actual=output_info_dict_by_floyd_warshall)

    def _compare_output_info(self, expected: Dict[int, OutputInformation], actual: Dict[int, OutputInformation]):
        for node_id in expected.keys():
            expected_output_info = expected[node_id]
            actual_output_info = actual[node_id]

            self.assertDictEqual(
                expected_output_info.shortest_distance_dict,
                actual_output_info.shortest_distance_dict,
            )

