import Nodes as N
import heapq

def shortest_path(start: str, end: str) -> list:
    """
    Takes inputs start and end which are nodes,
    and determines the shortest path between them
    using the Dijkstra Algorithm
    """
    distances = {} # Saved the shortest known distance from the start node
    previous = {} # To save the relative path from nodes to the previous shortest node
    heap = [] # To organize nodes from lowest weight to highest
    
    for node in N.graph: # Set all nodes to infinity in distances and set all nodes to None for previous
        distances[node] = float('inf') 
        previous[node] = None

    distances[start] = 0 # Starting node = 0
    heapq.heappush(heap, (0, start)) # Add starting node to heap list

    while heap: # Iterate through heap
        current_dist, current_node = heapq.heappop(heap) # Obtain the Weight and name of the current Node being observed

        if current_node == end: # If current Node is the End node then end the loop and create path
            break

        if current_dist > distances[current_node]: # If the weight of the current node is > overall weight move on to next node in heap
            continue

        for neighbor in N.graph[current_node]: # Iterate through the current node in graph to look at its neighbors
            weight = N.graph[current_node][neighbor]
            new_dist = distances[current_node] + weight # Calculated sum of the overeall weight and the weight to the neighbor

            if new_dist < distances[neighbor]: 
                distances[neighbor] = new_dist # If the new weight is less than shortest known distance from the start node, update node
                previous[neighbor] = current_node # Save the shortest relative path to neighbor as being the current node
                heapq.heappush(heap, (new_dist, neighbor)) # push updated distances into a priority queue; heap ensures the smallest-distance node is popped first

    # rebuild path
    path = [] # List for shortest path
    node = end # Make sure node = ending node

    if distances[end] == float('inf'): # If the shortest known distance from the start node is infinity then there is no path to end node
        print("No route found to end")
        return []

    while node is not None: # while loop to iterate through previous
        path.append(node) # add previous nodes in route to list(path)
        node = previous[node] # cycle through the route in previous

    path.reverse() # Flip list to get list from start to end
    return path

print(shortest_path('C', 'E'))