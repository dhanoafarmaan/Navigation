import math
import heapq
from Nodes_class import Nodes

class Astar:
    @staticmethod
    def heuristic(node, goal, positions):
        x1, y1 = positions[node]
        x2, y2 = positions[goal]

        return math.hypot(x2 - x1, y2 - y1)

    @staticmethod
    def Ashortest_path(graph: dict, positions: dict, start: str, end: str) -> list:
        """
        Shortest path algorithm using A* algorithm.

        g_score = cost of traveling from start to current_node,
        heuristic = estimated cost of travelling from current node to end,
        f_score = g + heuristic,
        The node with the lowest f_score is selected to be explored next.
        """
        # Check that the starting and ending nodes exist in the graph
        if start not in graph:
            raise ValueError(f"Starting node {start} is not in the graph.")
        
        if end not in graph:
            raise ValueError(f"Ending node {end} is not in the graph.")

        # Initialize open and closed lists
        # open_list contains nodes that still need to be explored 
        # closed_list contains nodes that have already been fully explored
        open_list = []
        closed_list = []

        # Initialize dictionaries to store the cost of reaching each node,
        # the estimated total cost, and the previous node in the shortest path
        g_score = {}
        f_score = {}
        previous = {}

        # Set the initial values for every node
        # All nodes initially have an unknown/infinite cost
        # No previous node has been assigned yet
        for node in graph:
            g_score[node] = float('inf')
            f_score[node] = float('inf')
            previous[node] = None

        # The cost of reaching the starting node from itself is 0
        g_score[start] = 0

        # Calculate the initial f_score for the starting node
        f_score[start] = Astar.heuristic(start, end, positions)

        # Add the starting node to the open list
        # The heap keeps the node with the lowest f_score at the top
        heapq.heappush(open_list, (f_score[start], start))

        # Continue exploring nodes while there are still nodes in the open list
        while open_list:
            # Remove the node with the lowest f_score from the heap
            current_f, current_node = heapq.heappop(open_list)

            # If the goal has been reached, the shortest path can be reconstructed
            if current_node == end:
                break

            # Skip the node if it has already been explored
            if current_node in closed_list:
                continue

            # Mark the current node as explored
            closed_list.append(current_node)

            # Check every neighboring node connected to the current node
            for neighbor, weight in graph[current_node].items():

                # Skip neighbors that have already been explored
                if neighbor in closed_list:
                    continue

                # Calculate the cost of reaching the neighbor through the current node
                new_g = g_score[current_node] + weight

                # If this route to the neighbor is shorter than the
                # shortest route found so far, update its information
                if new_g < g_score[neighbor]:

                    # Store the new shortest known cost to the neighbor
                    g_score[neighbor] = new_g

                    # Store the current node as the previous node
                    # so the final path can be reconstructed
                    previous[neighbor] = current_node

                    # Calculate the estimated total cost:
                    # f_score = cost so far + estimated cost to the goal
                    f_score[neighbor] = (
                           new_g
                           + Astar.heuristic(neighbor, end, positions)
                    )

                    # Add the neighbor to the open list so it can be explored
                    # The heap will prioritize the node with the lowest f_score
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        # If the end node still has an infinite g_score,
        # then no route from start to end was found
        if g_score[end] == float('inf'):
            print(f"No route found to", end)
            return []

        # Reconstruct the shortest path by working backwards
        # from the end node using the previous dictionary
        path = []
        node = end

        while node is not None:
            path.append(node)
            node = previous[node]

        # The path was built from end to start, so reverse it
        # to obtain the path from start to end
        path.reverse()
                 
        return path

graph, positions = Nodes.astar_nodes(num_nodes=100, connections=3)

path = Astar.Ashortest_path(
    graph=graph,
    positions=positions,
    start="A1",
    end="A36"
)

print(path)