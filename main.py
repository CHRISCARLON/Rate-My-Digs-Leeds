import streamlit as st
import folium
import streamlit_folium 
import matplotlib.pyplot as plt
import pandas as pd
from fetch_data import connect_to_motherduck, fetch_data
from leeds_hex import get_hexagons_within_boundary, hexagons_to_geodataframe, define_city


def hex_mapper():
    # Generate hexagons within the boundary
    city = define_city("Leeds")
    hexagons = get_hexagons_within_boundary(city, resolution=7)
    hex_gdf = hexagons_to_geodataframe(hexagons)

    # Plot
    fig, ax = plt.subplots()
    hex_gdf.boundary.plot(ax=ax, color='blue', alpha=1)
    plt.title('Leeds, UK with Hexagonal Grid')
    plt.show()
    
def main_page():
    st.write("hello")
    con = connect_to_motherduck("leeds_hmo")
    df = fetch_data(con)
    st.write(df)


if __name__=="__main__":
    main_page()