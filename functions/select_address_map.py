import folium
import streamlit as st

def select_address_map(df):
    st.markdown('## Address Mapping')
    # Separate multiselect for addresses
    selected_addresses = st.multiselect('**Search an Address**', options=df['address'].unique())

    # Add 'coords' column to the original DataFrame first
    df['coords'] = df['geometry'].apply(lambda geom: (geom.y, geom.x) if not geom.is_empty else None)

    # Filter the DataFrame based on selected addresses or licence holders
    mask = df['address'].isin(selected_addresses)
    filtered_df = df.loc[mask]

    # Display DataFrame
    st.write("")
    st.write("**Table Information**")
    st.dataframe(filtered_df[['address', 'Street Name', 'Maximum Permittted Number of Tenants']], use_container_width=True, hide_index=True)
    
    # Set coordinates for Leeds, UK
    leeds_centre = (53.800755, -1.549077)
    
    # Create a Folium map centered on Leeds with custom attribution
    custom_attribution = 'Map data &copy; OpenStreetMap contributors | Housing in Multiple Occupation (HMO) licence register, (c) Leeds City Council, 2024, <a href="https://datamillnorth.org/dataset/2o13g/houses-in-multiple-occupation-licence-register/" target="_blank">Data Source: Data Mill North</a>. This information is licensed under the terms of the Open Government Licence.'
    m = folium.Map(location=leeds_centre, zoom_start=12, 
                            attr=custom_attribution)

    # Grouped df ready to plot
    grouped = filtered_df.groupby('coords')

    for coords, group in grouped:
        # Extract latitude and longitude from coords
        latitude, longitude = coords

        # Aggregate information for tooltip
        tooltip_text = '<br>'.join([f"<div style='font-family: monospace; font-size: 12px;'> Address: {row['address']}.</div>" for _, row in group.iterrows()])
        
        # Create a popup with aggregated information
        popup = folium.Popup(tooltip_text, max_width=700)
    
        # Create a marker for the grouped addresses with the popup
        folium.Marker([latitude, longitude], popup=popup, icon=folium.Icon(icon='home', prefix='fa', color='purple')).add_to(m)

    return m
