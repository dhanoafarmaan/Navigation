import folium

def show_route(graph, path, edges):

    start_lat = graph.nodes[path[0]]["y"]
    start_lon = graph.nodes[path[0]]["x"]

    end_lat = graph.nodes[path[-1]]["y"]
    end_lon = graph.nodes[path[-1]]["x"]

    map = folium.Map(
    location=[start_lat, start_lon],
    zoom_start=14
    )

    folium.TileLayer(
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attr='© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    name="OpenStreetMap",
    overlay=False,
    control=True
    ).add_to(map)

    map.get_root().html.add_child(
    folium.Element("""
        <style>
            .leaflet-bottom.leaflet-right {
                right: auto;
                left: 0;
            }

            .leaflet-control-attribution {
                font-size: 9px;
            }
        </style>
    """)
    )

    route_coordinates = []

    for i in range(len(edges)):

        current_node = path[i]
        next_node = path[i + 1]
        edge_key = edges[i]

        edge_data = graph.get_edge_data(
            current_node,
            next_node,
            edge_key
        )

        if "geometry" in edge_data:

            geometry = edge_data["geometry"]

            for point in geometry.coords:

                lon, lat = point

                route_coordinates.append(
                    [lat, lon]
                )

        else:

            lat1 = graph.nodes[current_node]["y"]
            lon1 = graph.nodes[current_node]["x"]

            lat2 = graph.nodes[next_node]["y"]
            lon2 = graph.nodes[next_node]["x"]

            route_coordinates.append(
                [lat1, lon1]
            )

            route_coordinates.append(
                [lat2, lon2]
            )

    folium.PolyLine(
        route_coordinates,
        weight=5,
        opacity=0.8
    ).add_to(map)

    map.fit_bounds(route_coordinates)

    folium.Marker(
        [start_lat, start_lon],
        tooltip="Start"
    ).add_to(map)

    folium.Marker(
        [end_lat, end_lon],
        tooltip="Destination"
    ).add_to(map)

    filename = "data/route.html"

    map.save(filename)

    return map