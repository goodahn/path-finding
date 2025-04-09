from unittest import TestCase

from single_agent.dijkstra import find_shortest_path
from utils.fixture import make_grid


class TestAstar(TestCase):
    def test_with_grid(self):
        width, height = 3, 3
        graph = make_grid(width, height, 1)
        
        for source_node_id in range(width*height):
            x_source_node, y_source_node = source_node_id % width, source_node_id // width
            for goal_node_id in range(width*height):
                x_goal_node, y_goal_node = goal_node_id % width, goal_node_id // width

                print(source_node_id, goal_node_id)
                (shortest_distance, _) = find_shortest_path(graph, source_node_id, goal_node_id)
                self.assertEqual(shortest_distance, abs(x_source_node - x_goal_node) + abs(y_source_node - y_goal_node))