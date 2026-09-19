import osmnx as ox


def geocode_address(address, location):

    query = f"{address}, {location}"

    results = ox.geocode_to_gdf(
        query,
        which_result=None
    )

    if results.empty:
        raise ValueError(
            f"Could not find location: {address}"
        )

    search_words = set(address.lower().split())

    best_result = None
    best_score = -1

    for i in range(len(results)):

        result = results.iloc[i]

        name = str(
            result.get("name", "")
        ).lower()

        display_name = str(
            result.get("display_name", "")
        ).lower()

        score = 0

        # Compare the user's words with the actual name
        for word in search_words:

            if word in name:
                score += 3

            elif word in display_name:
                score += 1

        if score > best_score:

            best_score = score
            best_result = result

    point = best_result.geometry.centroid

    return point.y, point.x