import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from functions.geo_joiner import df_to_geodf, spatial_join_hex_with_data

"""
Does df_to_geodf correctly change the coordinates to Point geometries and assign the correct crs? 
"""

def test_df_to_geodf():
    df = pd.DataFrame({
    'Coordinates': [
        '40.7128, -74.0060',  # New York
        '34.0522, -118.2437', # Los Angeles
        '41.8781, -87.6298',  # Chicago
        '29.7604, -95.3698',  # Houston
        '33.4484, -112.0740', # Phoenix
        '39.9526, -75.1652',  # Philadelphia
        '29.4241, -98.4936'   # San Antonio
    ]
})
    
    geo_df = df_to_geodf(df)
    
    assert 'Coordinates' in df.columns, "A Coordinate columns is present in the df"
    assert 'Latitude' in geo_df.columns and 'Longitude' in geo_df.columns, "Latitude and Longitude columns should be present"
    assert isinstance(geo_df, gpd.GeoDataFrame), "Output should be a GeoDataFrame"
    assert geo_df.crs.to_string() == 'EPSG:4326', "CRS should be WGS 84 (EPSG:4326)"
    assert all(isinstance(geom, Point) for geom in geo_df.geometry), "All geometries should be Points"
    
def create_mock_hex_gdf():
    hexes = [
        Polygon([(-1, 1), (-1, 2), (0, 3), (1, 2), (1, 1), (0, 0)]),
        Polygon([(1, 1), (1, 2), (2, 3), (3, 2), (3, 1), (2, 0)]),
    ]
    hex_gdf = gpd.GeoDataFrame(geometry=hexes, crs="EPSG:4326")
    return hex_gdf

def create_mock_data_gdf():
    data_points = [
        {'geometry': Point(0.5, 1.5), 'UniqueAddressCount': 5},
        {'geometry': Point(2.5, 1.5), 'UniqueAddressCount': 3},
    ]
    data_gdf = gpd.GeoDataFrame(data_points, crs="EPSG:4326")
    return data_gdf

"""
The final gdf should have a total unique address count to use for the map later on.
Does the spatial join work and the index join at the end?
"""
def test_spatial_join_hex_with_data():
    hex_gdf = create_mock_hex_gdf()
    data_gdf = create_mock_data_gdf()

    result_gdf = spatial_join_hex_with_data(hex_gdf, data_gdf)
    
    assert len(result_gdf) == len(hex_gdf), "Result should have the same number of rows as the hex_gdf"
    assert result_gdf['TotalUniqueAddresses'].sum() == 8, "Total unique addresses should sum up correctly"
    assert 'TotalUniqueAddresses' in result_gdf.columns, "Result should have a 'TotalUniqueAddresses' column"


if __name__ == "__main__":
    pytest.main()
