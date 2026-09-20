import osmnx as ox

def geocode_address(address, location):

    query = f"{address}, {location}"

    try:

        point = ox.geocode(query)

    except Exception as e:

        raise ValueError(
            f"Could not find location: {address}"
        ) from e

    return point