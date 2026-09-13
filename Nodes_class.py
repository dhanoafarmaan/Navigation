import random
import math

class Nodes:
    @staticmethod
    def dijkstra_nodes(num_nodes: int) -> dict:

        graph = {}

        for i in range(num_nodes):
            node = f"A{i}"
            graph[node] = {}

            if i + 1 < num_nodes:
                graph[node][f"A{i+1}"] = random.randint(1, 20)
            if i + 2 < num_nodes:
                graph[node][f"A{i+2}"] = random.randint(1, 20)
            if i + 3 < num_nodes:
                graph[node][f"A{i+3}"] = random.randint(1, 20)
        return graph

    @staticmethod
    def astar_nodes(num_nodes: int, connections: int) -> dict:
        # Give every node a position
        positions = {
            f"A{i}": (
                random.uniform(0, 100),
                random.uniform(0, 100)
            )
            for i in range(num_nodes)
        }

        graph = {node: {} for node in positions}

        # First, connect every node to the next node
        # This guarantees that the graph is connected
        for i in range(num_nodes - 1):
            node = f"A{i}"
            neighbor = f"A{i+1}"

            x1, y1 = positions[node]
            x2, y2 = positions[neighbor]

            distance = math.hypot(x2 - x1, y2 - y1)

            graph[node][neighbor] = distance
            graph[neighbor][node] = distance

        # Connect each node to its nearest nodes
        for node, (x1, y1) in positions.items():
            distances = []

            for other, (x2, y2) in positions.items():
                if node != other:
                    distance = math.hypot(x2 - x1, y2 - y1)
                    distances.append((distance, other))

            distances.sort()

            for distance, neighbor in distances[:connections]:
                graph[node][neighbor] = distance

                # Add the reverse edge
                graph[neighbor][node] = distance

        return graph, positions