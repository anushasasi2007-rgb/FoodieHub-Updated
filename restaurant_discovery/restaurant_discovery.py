import pandas as pd


def restaurant_discovery(restaurants, location, cuisine, price_range, min_rating):
    data = pd.DataFrame(restaurants)

    # Location filter
    if location != "All":
        data = data[data["location"] == location]

    # Cuisine filter
    if cuisine != "All":
        data = data[data["cuisine"] == cuisine]

    # Price filter
    if price_range != "All":
        data = data[data["price_range"] == price_range]

    # Rating filter
    data = data[data["rating"] >= min_rating]

    return data


def get_recommendations(restaurants, location, cuisine, price_range, min_rating):
    results = restaurant_discovery(
        restaurants,
        location,
        cuisine,
        price_range,
        min_rating
    )

    return results.sort_values(
        by="rating",
        ascending=False
    )