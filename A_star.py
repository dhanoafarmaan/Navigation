import math
import Nodes as N

class Astar:
    def heuristic(self, node, goal, positions):
        x1, y1 = positions[node]
        x2, y2 = positions[goal]

        return math.hypot(x2 - x1, y2 - y1)

    def Ashortest_path(self, graph: dict, start: str, end: str) -> list:
        if start not in graph:
                raise ValueError(f"Starting node {start} is not in the graph.")
        
        if end not in graph:
                raise ValueError(f"Ending node {end} is not in the graph.")
        
        F = G + Astar.heuristic(current_node, end, N.Nodes().astar_nodes[1])
        return


node_generator = N.Nodes()

graph = node_generator.astar_nodes(num_nodes=100, connections=3)[0]

path = Astar.Ashortest_path(
    graph=graph,
    start="A1",
    end="A99"
)

print(path)