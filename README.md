# GraphPathPy: Shortest Path Algorithms in Python

This project offers a Python-based library for various graph shortest path algorithms. It includes implementations of A*, Dijkstra, Bellman-Ford, Floyd-Warshall, and Space-Time A*. A key feature is the exploration of algorithm performance in scenarios with dynamic edge weight updates.

## Implemented Algorithms and Capabilities

This library provides implementations of several classic shortest path algorithms:

*   **A\* Search**: Finds the shortest path using a heuristic to guide the search.
*   **Bellman-Ford Algorithm**: Computes shortest paths from a single source vertex to all other vertices in a weighted digraph. Handles negative edge weights.
*   **Dijkstra's Algorithm**: Computes shortest paths from a single source vertex to all other vertices in a weighted graph with non-negative edge weights.
*   **Floyd-Warshall Algorithm**: Computes all-pairs shortest paths.
*   **Space-Time A\* Search**: An adaptation of A\* for problems involving a time dimension (details in `single_agent/space_time_a_star.py`).

In addition to these, the project includes specialized functions for **Dynamic Shortest Path Updates**:

*   Located in `single_agent/dynamic_problem.py`, these functions efficiently update shortest path information (previously computed, e.g., by Floyd-Warshall) when edge weights in the graph are increased or decreased. This is particularly useful for scenarios where graph costs change over time.

## Core Data Structures

- **`Graph`**: Represents the graph using an adjacency list approach. Manages nodes and edges.
- **`Node`**: Represents a vertex in the graph. Stores its ID and lists of inbound and outbound edges.
- **`Edge`**: Represents a directed edge in the graph. Connects a start node to an end node and has an associated weight.
- **`Tree`**: (from `common/tree.py`) A tree data structure where each tree node wraps a `Node` object. This is likely used to represent shortest path trees or other hierarchical structures derived from graph processing.

## Usage and Examples

For more detailed examples, please see the scripts in the `example/` directory.

### Basic Usage

Here's a simple example of how to use the library to find the shortest path between two nodes using Dijkstra's algorithm:

```python
from common import Graph, Node, Edge
from single_agent import dijkstra

# 1. Create nodes
node0 = Node(id=0)
node1 = Node(id=1)
node2 = Node(id=2)

# 2. Create edges
edge01 = Edge(id=0, start_node=node0, end_node=node1, weight=1.0)
edge12 = Edge(id=1, start_node=node1, end_node=node2, weight=2.0)
edge02 = Edge(id=2, start_node=node0, end_node=node2, weight=5.0)

# 3. Create graph
graph = Graph(nodes=[node0, node1, node2], edges=[edge01, edge12, edge02])

# 4. Find shortest path using Dijkstra
source_node_id = 0
goal_node_id = 2
distance, path = dijkstra.find_shortest_path(graph, source_node_id, goal_node_id)

if distance != float('inf'):
    print(f"Shortest distance from node {source_node_id} to node {goal_node_id} is: {distance}")
    print(f"Path: {path}")
else:
    print(f"No path found from node {source_node_id} to node {goal_node_id}")
```

### Dynamic Edge Weight Updates

The `example/bypass_agents_by_updating_edge_weight.py` script showcases how to use the dynamic update capabilities. It first computes all-pairs shortest paths using the Floyd-Warshall algorithm on a grid graph. Subsequently, it iteratively modifies the weights of randomly selected edges. The core logic for recalculating shortest paths efficiently after these changes—handling both edge weight increases and decreases—is provided by functions within `single_agent/dynamic_problem.py`. The example measures the performance of these update operations, demonstrating the library's utility in scenarios where graph costs are not static.

## Installation

This project is written in Python 3. It does not require any special installation steps or external libraries beyond what is typically available in a standard Python environment. Clone the repository to your local machine:
```bash
git clone <repository_url> # Replace <repository_url> with the actual URL
cd <repository_directory_name>
```

## Running Tests

The project includes a suite of tests located in the `tests/` directory. These tests are built using Python's standard `unittest` module. To run the tests, navigate to the root directory of the project and execute the following command:
```bash
python -m unittest discover tests
```

## Contributing
Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please feel free to:
- Open an issue in the project's issue tracker.
- Fork the repository, make your changes, and submit a pull request.

When contributing code, please ensure your changes are well-tested and adhere to the existing coding style where possible.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
