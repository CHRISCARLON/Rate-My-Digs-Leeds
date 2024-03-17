# Import required libaries and modules
import streamlit as st
from streamlit_folium import folium_static
from functions.fetch_data import connect_to_motherduck, fetch_data, fetch_data2, fetch_data3
from functions.leeds_hex import hex_mapper
from functions.geo_joiner import df_to_geodf, spatial_join_hex_with_data
from functions.hex_map import display_hex_map
from functions.select_address_map import select_address_map
from functions.mongodb_dump_ratings import user_input_and_data_upload
from functions.homepage import homepage_function

# Return Data Functions
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
    df = fetch_data3(con)
    return df

# Map Creation Functions
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

# Misc Calculation Functions 
def return_top_postcodes():
    top_10_postcodes = return_df()
    top_10_postcodes = top_10_postcodes.groupby('postcode')['UniqueAddressCount'] \
        .sum() \
        .reset_index() \
        .sort_values(by="UniqueAddressCount", ascending=False) \
        .head(10)  
    return top_10_postcodes

# Homepage Function
def homepage_text():
    homepage_function()

def main():
    st.set_page_config(layout="wide")
    
    st.sidebar.header("**Navigation Bar**")
    page = st.sidebar.radio("**Please Select a Page**", 
                            ["**Home Page**",
                            "**HMO Density**", 
                            "**HMO Deep Dive**", 
                            "**Feedback Form**"])

    if page == "**Home Page**":
        homepage_text()
    elif page == "**HMO Density**":
        st.markdown("# Concentration of HMOs Accross Leeds:")
        
        # Create the hex counts
        hex_map_gdf = return_hex_counts()  
        # Calculate the total number of addresses
        total_addresses = hex_map_gdf['TotalUniqueAddresses'].sum()
        st.markdown(f"#### **Total addresses plotted**: {total_addresses}")
        
        # Calculate the top 10 postcodes
        top_10_postcodes = return_top_postcodes() 
        st.markdown("#### **Top 10 Postcodes with the Most HMOs**:")
        st.dataframe(top_10_postcodes, hide_index=True)
    
        # Generate the map using the return_hex_map function
        folium_map = return_hex_map(hex_map_gdf)
        st.markdown("#### Density Map:")
        st.write("*Hover your mouse over the hex grids for more information:*")
        folium_static(folium_map, width=1420, height=750)
    elif page == "**HMO Deep Dive**":
        # Use return_df2 to get the geodataframe
        address_map_gdf = return_df2()
        
        # Generate and display the map for Rate My Digs
        folium_map2 = return_address_map(address_map_gdf)
        st.write('###### **Click an icon for more popup information:**')
        # Display the map in the Streamlit app
        folium_static(folium_map2, width=1420, height=750)
    elif page == "**Feedback Form**":
        address_data = return_df3()
        user_input_and_data_upload(address_data)
        
if __name__ == "__main__":
    main()