import osmnx as ox


def show_route(graph, path):

    fig, ax = ox.plot_graph_route(
        graph,
        path,
        route_color="red",
        route_linewidth=3,
        node_size=0,
        bgcolor="white",
    )
    
    return fig, ax