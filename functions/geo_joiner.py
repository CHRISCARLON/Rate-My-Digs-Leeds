import geopandas as gpd
from shapely.geometry import Point


def df_to_geodf(df):
    """
    Convert a DataFrame with coordinates to a GeoDataFrame.
    """
    # 'Coordinates' column format is '(lat, lon)', split and convert to numeric
    
    df[['Latitude', 'Longitude']] = df['coordinates'].str.strip('()').str.split(', ', expand=True).astype(float)
    
    # Create Point geometries
    df['geometry'] = [Point(xy) for xy in zip(df.Longitude, df.Latitude)]
    # Convert to GeoDataFrame
    geo_df = gpd.GeoDataFrame(df, geometry='geometry')
    # Set the CRS to WGS 84 to match hex_gdf
    geo_df.crs = "EPSG:4326"
    return geo_df


def spatial_join_hex_with_data(hex_gdf, data_gdf):
    """
    Perform a spatial join and aggregate unique address counts by hexagon.
    """
    # Ensure CRS match before spatial join
    if hex_gdf.crs != data_gdf.crs:
        data_gdf = data_gdf.to_crs(hex_gdf.crs)
    
    # Perform spatial join
    joined_gdf = gpd.sjoin(hex_gdf, data_gdf, how="inner", predicate="intersects")
    
    # After the join, 'index' of hex_gdf becomes the index of joined_gdf
    # Aggregate UniqueAddressCount by the hexagon index (which is the index of joined_gdf after the join)
    count_by_hex = joined_gdf.groupby(joined_gdf.index).agg(
        TotalUniqueAddresses=('UniqueAddressCount', 'sum')).reset_index()

    # Rename 'index' column to merge back correctly with hex_gdf
    count_by_hex.rename(columns={'index': 'hex_index'}, inplace=True)

    # Ensure hex_gdf has a column to join on, reset its index if necessary
    hex_gdf.reset_index(inplace=True)
    hex_gdf.rename(columns={'index': 'hex_index'}, inplace=True)
    
    # Join aggregated data back to hex_gdf to maintain all hexagons, including those without any addresses
    final_gdf = hex_gdf.merge(count_by_hex, how="left", on="hex_index")
    final_gdf['TotalUniqueAddresses'] = final_gdf['TotalUniqueAddresses'].fillna(0)
    
    # Optionally, set the final GeoDataFrame's index back if desired
    final_gdf.set_index('hex_index', inplace=True)
    return final_gdf