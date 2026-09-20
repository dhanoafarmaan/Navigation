import streamlit as st

from streamlit_folium import st_folium
from Graph import load_graph
from Navigation import find_route
from Navigation import get_road_names
from Map import show_route
from Geocoder import geocode_address


st.title("Navigation")


location = st.text_input(
    "Location",
    "Waterloo, Ontario, Canada"
)

start_address = st.text_input(
    "Starting location"
)

end_address = st.text_input(
    "Destination"
)

@st.cache_resource
def get_graph(location):

    return load_graph(location)

if st.button("Find Route"):

    graph = get_graph(location)

    start = geocode_address(
        start_address,
        location
    )

    end = geocode_address(
        end_address,
        location
    )

    path, edges = find_route(
        graph,
        start,
        end
    )

    road_names = get_road_names(
        graph,
        path,
        edges
    )

    st.session_state["route_map"] = show_route(
        graph,
        path,
        edges
    )

    st.session_state["road_names"] = road_names

    st.session_state["path"] = path

if "route_map" in st.session_state:

    st_folium(
        st.session_state["route_map"],
        width=1000,
        height=600
    )

    st.write(
        "Roads:",
        st.session_state["road_names"]
    )

    st.write(
        "Path:",
        st.session_state["path"]
    )