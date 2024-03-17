import folium
from folium import GeoJson
import branca

def display_hex_map(gdf):
    """
    Display hex grids on a Folium map.
    Colour hexes based on the address count within each post code. 
    Hexes with no addresses are not plotted.
    The map is always centered on Leeds.
    """

    # Filter the GeoDataFrame to exclude hexagons with no addresses
    gdf_with_addresses = gdf[gdf['TotalUniqueAddresses'] > 0]

    # Set coordinates for Leeds, UK
    leeds_centre = (53.800755, -1.549077)
    
    # Create a Folium map centered on Leeds with custom attribution
    custom_attribution = 'Map data &copy; OpenStreetMap contributors | Housing in Multiple Occupation (HMO) licence register, (c) Leeds City Council, 2024, <a href="https://datamillnorth.org/dataset/2o13g/houses-in-multiple-occupation-licence-register/" target="_blank">Data Source: Data Mill North</a>. This information is licensed under the terms of the Open Government Licence.'
    m = folium.Map(location=leeds_centre, zoom_start=12, 
                            attr=custom_attribution)

    # Define a color scale for the hex grids with specified vmin, vmax, and tick_labels
    colors = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#084594"]
    colormap = branca.colormap.LinearColormap(colors, vmin=0, vmax=220)
    colormap.caption = 'Heatmap Bar: Total Unique Addresses in Each Hexagon'

    result = [i for i in range(0, 221, 20)]
    colormap.tick_labels = [str(label) for label in result]
    
    # Function to assign color to each hex based on address count
    def style_function(feature):
        address_count = feature['properties']['TotalUniqueAddresses']
        return {
            'fillColor': colormap(address_count),
            'color': 'black',
            'weight': 0.8,
            'fillOpacity': 0.7
        }

    # Add hexagons with addresses to the map with colors
    GeoJson(
        gdf_with_addresses,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=['TotalUniqueAddresses'], aliases=['Addresses:'], localize=True)
    ).add_to(m)

    # Add color scale to the map
    colormap.add_to(m)

    return m
