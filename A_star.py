import heapq
import osmnx as ox


class Astar:
    @staticmethod
    def heuristic(node, goal, graph):

        x1 = graph.nodes[node]["x"]
        y1 = graph.nodes[node]["y"]

        x2 = graph.nodes[goal]["x"]
        y2 = graph.nodes[goal]["y"]

        return ox.distance.great_circle(
            y1,
            x1,
            y2,
            x2
        )

    @staticmethod
    def Ashortest_path(graph, start, end) -> list:
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

        # Store which specific edge was used to reach each node
        previous_edge = {}

        # Set the initial values for every node
        # All nodes initially have an unknown/infinite cost
        # No previous node has been assigned yet
        for node in graph.nodes:
            g_score[node] = float('inf')
            f_score[node] = float('inf')
            previous[node] = None

        # The cost of reaching the starting node from itself is 0
        g_score[start] = 0

        # Calculate the initial f_score for the starting node
        f_score[start] = Astar.heuristic(start, end, graph)

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
            for neighbor in graph.successors(current_node):

                # Skip neighbors that have already been explored
                if neighbor in closed_list:
                    continue

                # Get all edges connecting the current node to the neighbor
                edge_data = graph.get_edge_data(
                    current_node,
                    neighbor
                )

                # Find the shortest edge between the current node and neighbor
                weight = float('inf')
                best_edge = None

                for key in edge_data:
                    if "length" in edge_data[key]:
                        edge_length = edge_data[key]["length"]

                        if edge_length < weight:
                            weight = edge_length
                            best_edge = key

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

                    # Store the specific edge that was used
                    previous_edge[neighbor] = best_edge

                    # Calculate the estimated total cost:
                    # f_score = cost so far + estimated cost to the goal
                    f_score[neighbor] = (
                           new_g
                           + Astar.heuristic(neighbor, end, graph)
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
        edges = []

        node = end

        while node is not None:
            path.append(node)

            if previous[node] is not None:
                edges.append(previous_edge[node])

            node = previous[node]

        # The path was built from end to start, so reverse it
        # to obtain the path from start to end
        path.reverse()

        # The edges were also built backwards, so reverse them
        # to obtain the edges from start to end
        edges.reverse()
                 
        return path, edges