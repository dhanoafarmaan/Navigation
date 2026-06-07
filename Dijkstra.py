import Nodes as N

def shortest_path(start: str, end: str) -> list:
    """
    Takes inputs start and end which are nodes,
    and determines the shortest path between them
    using the Dijkstra Algorithm
    """

    distances = {node: float('inf') for node in N.graph}
    distances[start] = 0
            
shortest_path('A','E')