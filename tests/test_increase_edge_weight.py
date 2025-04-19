import random
from unittest import TestCase
from typing import Dict

from single_agent.output_information import OutputInformation
from single_agent import floyd_warshall
from single_agent.dynamic_problem import (
    increase_edge_weight,
)
from utils.fixture import make_grid


class TestIncreaseEdgeWeight(TestCase):
    def test_with_grid(self):
        # width, height = random.randint(3, 10), random.randint(3, 10)
        width, height = 3, 3
        graph = make_grid(width, height, 1)
        output_info_dict = floyd_warshall.make_output_information(graph)
        
        changed_edge_ids = []
        #for test_edge_id in random.sample(list(range(1, width*height)), 5):
        for test_edge_id in [4, 2, 6, 1, 8]:
            test_edge = graph.get_edge(test_edge_id)
            changed_edge_ids.append(f"{test_edge.start_node.id}, {test_edge.end_node.id} - {test_edge_id}")
            increase_edge_weight(graph, output_info_dict, test_edge_id, 10)
        expected_output_info_dict = floyd_warshall.make_output_information(graph)

        self._compare_output_info(expected=expected_output_info_dict, actual=output_info_dict, changed_edge_ids=changed_edge_ids)

    def _compare_output_info(self, expected: Dict[int, OutputInformation], actual: Dict[int, OutputInformation], **kwargs):
        for node_id in expected.keys():
            expected_output_info = expected[node_id]
            actual_output_info = actual[node_id]

            self.assertDictEqual(
                expected_output_info.shortest_distance_dict,
                actual_output_info.shortest_distance_dict,
                msg=f"source node is {node_id} and changed edge ids are {kwargs['changed_edge_ids']}\n"
            )

