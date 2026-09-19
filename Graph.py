import os
import osmnx as ox
from shapely.geometry import Point, LineString


def load_graph(location):

    filename = location.replace(",", "").replace(" ", "_") + ".graphml"

    if os.path.exists(filename):

        print("Loading saved graph...")

        graph = ox.load_graphml(filename)

    else:

        print("Downloading graph...")

        graph = ox.graph_from_place(
            location,
            network_type="drive"
        )

        ox.save_graphml(
            graph,
            filename
        )

        print("Graph saved.")

    return graph


def get_nearest_nodes(graph, start, end):

    start_lat, start_lon = start
    end_lat, end_lon = end

    start_edge = ox.distance.nearest_edges(
        graph,
        X=start_lon,
        Y=start_lat
    )

    end_edge = ox.distance.nearest_edges(
        graph,
        X=end_lon,
        Y=end_lat
    )

    start_node = add_address_node(
        graph,
        start_edge,
        start_lon,
        start_lat,
        "START"
    )

    end_node = add_address_node(
        graph,
        end_edge,
        end_lon,
        end_lat,
        "END"
    )

    return start_node, end_node


def add_address_node(graph, edge, lon, lat, name):

    u, v, key = edge

    edge_data = graph.get_edge_data(
        u,
        v,
        key
    )

    if "geometry" in edge_data:

        geometry = edge_data["geometry"]

    else:

        geometry = LineString([
            (graph.nodes[u]["x"], graph.nodes[u]["y"]),
            (graph.nodes[v]["x"], graph.nodes[v]["y"])
        ])

    address_point = Point(lon, lat)

    # Find the closest point on the road
    closest_point = geometry.interpolate(
        geometry.project(address_point)
    )

    closest_lon = closest_point.x
    closest_lat = closest_point.y

    # Create the temporary node
    node_id = name

    graph.add_node(
        node_id,
        x=closest_lon,
        y=closest_lat
    )

    # Find the position of the closest point along the road
    position = geometry.project(closest_point)
    fraction = position / geometry.length

    # Original road length is already in metres
    road_length = edge_data["length"]

    first_length = road_length * fraction
    second_length = road_length * (1 - fraction)

    # Copy edge information
    first_edge_data = edge_data.copy()
    second_edge_data = edge_data.copy()

    first_edge_data["length"] = first_length
    second_edge_data["length"] = second_length

    # Remove the original edge
    graph.remove_edge(
        u,
        v,
        key
    )

    # u → address
    graph.add_edge(
        u,
        node_id,
        **first_edge_data
    )

    # address → v
    graph.add_edge(
        node_id,
        v,
        **second_edge_data
    )

    return node_id