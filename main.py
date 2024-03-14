# Import required libaries and modules
import streamlit as st
from streamlit_folium import folium_static
from functions.fetch_data import connect_to_motherduck, fetch_data, fetch_data2, fetch_data3
from functions.leeds_hex import hex_mapper
from functions.geo_joiner import df_to_geodf, spatial_join_hex_with_data
from functions.hex_map import display_hex_map
from functions.select_address_map import select_address_map
from functions.mongodb_dump_ratings import user_input_and_data_upload

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
def return_df3():
    db = st.secrets['db_name']
    con = connect_to_motherduck(db)
    df = fetch_data2(con)
    return df

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
    st.markdown("# Welcome to Rate My Digs (Leeds)")
    
    with st.container():
        st.info("""
        **This Streamlit App Contains the following data:**\n
        "Housing in Multiple Occupation (HMO) Licence Register", (c) Leeds City Council, 2024, 
        [Data Mill North](https://datamillnorth.org/dataset/2o13g/houses-in-multiple-occupation-licence-register/).\n 
        This information is licensed under the terms of the Open Government Licence.
        """)
    
    st.markdown("## The aim is simple:")
    st.markdown("##### **1. Where are HMOs located in Leeds?**")
    st.markdown("##### **2. Are students happy with their HMO living conditions?**")
    
    # Adjust CSS for filled-in boxes with a distinct background color
    st.markdown("""
    <style>
    .navigation-box {
        background-color: #1f77b4; /* Change to a filled background color */
        color: #ffffff; /* Ensure text color contrasts well with the background */
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .navigation-box h3, .navigation-box p {
        margin: 0; /* Remove default margins for a cleaner look */
        color: #ffffff; /* Text color for visibility */
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("## Navigation:")
    st.markdown("##### Please use the bar to the left.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="navigation-box">
            <h3>HMO Density Map (Leeds)</h3>
            <p>View the density of HMOs across Leeds.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="navigation-box">
            <h3>HMO Ratings Map (Leeds)</h3>
            <p>View the best and worst ranked HMOs across Leeds.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="navigation-box">
            <h3>Rate My Digs (Leeds)</h3>
            <p>Submit your HMO feedback here!</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    st.set_page_config(layout="wide")
    
    st.sidebar.header("**Navigation Bar**")
    page = st.sidebar.radio("**Please Select a Page**", 
                            ["**Home Page**",
                            "**HMO Density Map (Leeds)**", 
                            "**HMO Ratings Map (Leeds)**", 
                            "**Rate My Digs (Leeds)**"])

    if page == "**Home Page**":
        homepage_text()
    elif page == "**HMO Density Map (Leeds)**":
        st.markdown("## Mapping the Density of HMOs Accross Leeds")
        
        # Create the hex counts
        hex_map_gdf = return_hex_counts()  
    
        # Calculate the total number of addresses
        total_addresses = hex_map_gdf['TotalUniqueAddresses'].sum()
        st.markdown(f"##### **Total addresses plotted**: {total_addresses}")
    
        # Generate the map using the display_hex_map function
        folium_map = return_hex_map(hex_map_gdf)
    
        # Display the map in the Streamlit app
        st.write("**Hover your mouse over the hex grids to see the total number of HMOs in each one**")
        folium_static(folium_map, width=1420, height=750)
    elif page == "**HMO Ratings Map (Leeds)**":
        # Use return_df2 to get the geodataframe
        address_map_gdf = return_df2()
        
        # Generate and display the map for Rate My Digs
        folium_map2 = return_address_map(address_map_gdf)
        st.write('###### **Click an icon for more popup information**')
        # Display the map in the Streamlit app
        folium_static(folium_map2, width=1420, height=750)
    elif page == "**Rate My Digs (Leeds)**":
        # Display the image in the first column
        st.image('pictures/Rate_My_Digs.png', width=250)
        address_data = return_df3()
        user_input_and_data_upload(address_data)
        

if __name__ == "__main__":
    main()