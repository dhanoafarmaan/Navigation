import osmnx as ox
from Graph import load_graph
from Navigation import find_route
from Navigation import get_road_names
from Map import show_route
from Geocoder import geocode_address


location = input("Enter location (City, Province, Country): ")
graph = load_graph(location)


start_address = input("Enter starting location: ")
end_address = input("Enter destination: ")

start = geocode_address(start_address, location)
end = geocode_address(end_address, location)

path, edges = find_route(
    graph,
    start,
    end
)

show_route(graph, path, edges)

road_names = get_road_names(
    graph,
    path,
    edges
)

print(path,'\n')
print(road_names)