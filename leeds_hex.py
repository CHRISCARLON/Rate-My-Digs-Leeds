import osmnx as ox
import matplotlib.pyplot as plt
from h3 import h3
import geopandas as gpd
import shapely.geometry


def get_hexagons_within_boundary(geometry, resolution=8):
    """
    Returns a list of hexagon IDs within the given geometry.
    """

    # Get hexagons within the bounding box of the geometry
    bounding_box = geometry.bounds
    south, west, north, east = bounding_box
    hexagons = h3.polyfill_polygon([(west, south), (west, north), (east, north), (east, south)], resolution)

    # Filter hexagons that are completely within the geometry
    hexagons_within_boundary = [h for h in hexagons if shapely.geometry.Polygon(h3.h3_to_geo_boundary(h, True)).intersects(geometry)]

    return hexagons_within_boundary


def hexagons_to_geodataframe(hexagons):
    """
    Convert a list of hexagon IDs to a GeoDataFrame.
    """
    polygons = []
    for hex_id in hexagons:
        polygons.append(shapely.geometry.Polygon(h3.h3_to_geo_boundary(hex_id, True)))
    return gpd.GeoDataFrame(geometry=polygons)


def define_city(city_name: str):
    # Ensure the city_name is combined with ", UK" to specify the country
    query = f"{city_name}, UK"
    
    # Use OSMnx to get the boundary of the specified place
    city = ox.geocode_to_gdf(query)
    
    # Extract the geometry of the first (and likely only) row
    geometry = city.iloc[0].geometry

    # Returning the geometry for further use
    return geometry


if __name__=="__main__":
    # Generate hexagons within the boundary
    city = define_city("Leeds")
    hexagons = get_hexagons_within_boundary(city, resolution=7)
    hex_gdf = hexagons_to_geodataframe(hexagons)

    # Plot
    fig, ax = plt.subplots()
    hex_gdf.boundary.plot(ax=ax, color='blue', alpha=1)
    plt.title('Leeds, UK with Hexagonal Grid')
    plt.show()
