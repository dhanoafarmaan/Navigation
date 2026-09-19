from Graph import get_nearest_nodes
from A_star import Astar


def find_route(graph, start, end):

    start_node, end_node = get_nearest_nodes(
        graph,
        start,
        end
    )

    path, edges = Astar.Ashortest_path(
        graph,
        start_node,
        end_node
    )

    return path, edges

def get_road_names(graph, path, edges):

    road_names = []

    for i in range(len(edges) - 1):

        current_node = path[i]
        next_node = path[i + 1]
        edge_key = edges[i]

        edge_data = graph.get_edge_data(
            current_node,
            next_node,
            edge_key
        )

        if "name" in edge_data:

            road_name = edge_data["name"]

            if not road_names or road_names[-1] != road_name:
                road_names.append(road_name)

    return road_names