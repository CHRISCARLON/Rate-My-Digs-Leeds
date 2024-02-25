# Import required libaries and modules
import streamlit as st
from streamlit_folium import folium_static
from functions.fetch_data import connect_to_motherduck, fetch_data, fetch_data2
from functions.leeds_hex import hex_mapper
from functions.geo_joiner import df_to_geodf, spatial_join_hex_with_data
from functions.hex_map import display_hex_map
from functions.select_address_map import select_address_map

# Use the streamlit cache to prevent reloading 
@st.cache_data(show_spinner=True)
def return_hex():
    hex = hex_mapper()
    return hex

@st.cache_data(show_spinner=True)
def return_df():
    db = st.secrets['db_name']
    con = connect_to_motherduck(db)
    df = fetch_data(con)
    df2 = df_to_geodf(df)
    return df2

@st.cache_data(show_spinner=True)
def return_df2():
    db = st.secrets['db_name']
    con = connect_to_motherduck(db)
    df = fetch_data2(con)
    df2 = df_to_geodf(df)
    return df2

@st.cache_data(show_spinner=True)    
def return_hex_counts():
    hex_object = return_hex()
    df_object = return_df()
    joined_gdf = spatial_join_hex_with_data(hex_object, df_object)
    return joined_gdf

def return_hex_map(gdf):
    map = display_hex_map(gdf)
    return map

def return_address_map(gdf):
    map = select_address_map(gdf)
    return map

def homepage_text():
    st.markdown("## TBC")

def main():
    st.set_page_config(layout="wide")
    
    st.sidebar.header("**Navigation Bar**")
    page = st.sidebar.radio("**Please Select a Page**", 
                            ["**Home Page**",
                            "**HMO Density Map (Leeds)**", 
                            "**HMO Address Map (Leeds)**", 
                            "**Rate My Digs**"])

    if page == "**Home Page**":
        homepage_text()
    elif page == "**HMO Density Map (Leeds)**":
        st.markdown("## Mapping the Density of HMOs accross Leeds")
        
        # Create the hex counts
        hex_map_gdf = return_hex_counts()  
    
        # Calculate the total number of addresses
        total_addresses = hex_map_gdf['TotalUniqueAddresses'].sum()
        st.write(f"**Total addresses plotted**: {total_addresses}")
    
        # Generate the map using the display_hex_map function
        folium_map = return_hex_map(hex_map_gdf)
    
        # Display the map in the Streamlit app
        st.write("**Hover your mouse over the hex grids to see the total number of HMOs in each one**")
        folium_static(folium_map, width=1420, height=750)
    elif page == "**HMO Address Map (Leeds)**":
        # Use return_df2 to get the geodataframe
        address_map_gdf = return_df2()
        
        # Generate and display the map for Rate My Digs
        folium_map2 = return_address_map(address_map_gdf)
        st.write('###### **Click an icon for more popup information**')
        # Display the map in the Streamlit app
        folium_static(folium_map2, width=1420, height=750)
    elif page == "**Rate My Digs**":
        st.markdown("## TBC")


if __name__ == "__main__":
    main()