import streamlit as st
from datetime import datetime
from pymongo.mongo_client import MongoClient

def create_connection():
    # Create Mongo DB connection
    uri = st.secrets['mongomongo']  
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    return client

def load_data_into_collection(client, db_name: str, collection_name: str, data: dict):
    # Make sure client takes db name, then the DB takes the collection name for the inser_one method!
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(data)
    
def provide_feedback_function():
    # Set up feedback box
    feedback = st.text_input(label="Please write your suggestion here:", value="", max_chars=500, key="feedback_input")
    
    # Ensure the button is always displayed
    submit_button_pressed = st.button("Submit Your Suggestion Here")  

    # Checks if the button was pressed
    if submit_button_pressed:  
        # Now checks if feedback is not empty
        if feedback:  
            try:
                current_time_date = datetime.now()

                data = {
                    "feedback": feedback,
                    "time_stamp": current_time_date
                }

                # MongoDB operations
                client = create_connection()
                load_data_into_collection(client, st.secrets["db_mongo"], st.secrets["mongo_collect2"], data)
                st.success("**Success! Thanks for sharing your thoughts!**")
            except Exception:
                st.error("**An error occurred. Please try again later.**")
        else:
            # This message will only be shown if the button was pressed but no feedback was entered
            st.error("**Please enter some feedback before submitting!**")

def homepage_function():
    st.markdown("""
    # Welcome to *Rate My Digs* :house_with_garden:

    ###### *Simplifying the search for quality HMOs in Leeds.*

    *Rate My Digs* is a simple platform aimed at improving the rental experience of people living in Leeds, particularly for those in Houses in Multiple Occupation (HMOs).

    ### Features at a Glance:
    - **HMO Density:** A map that visualises the concentration of HMOs across Leeds.
    - **HMO Deep Dive:** Gain insights into properties with reviews and ratings, enabling informed decisions.
    - **Feedback Form:** Share your experiences and contribute to improving private renting accross Leeds.
    """)
    st.markdown("""
    ### Why Use Rate My Digs?
    - Make smarter rental choices with property insights.
    - Raise your voice for higher living standards and accountability.
    """)
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
    
    st.markdown("##### *Please use the navigation bar to the left and select a page.*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="navigation-box">
            <h3>HMO Density</h3>
            <p>A map showing the density of HMOs across Leeds.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="navigation-box">
            <h3>HMO Deep Dive</h3>
            <p>What are people saying about HMOs across Leeds?</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="navigation-box">
            <h3>Feedback Form</h3>
            <p>Share your thoughts and submit your HMO feedback here!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    # Container for feedback section
    with st.container():
        st.markdown("""
                    ##### This is currently a prototype and runs on a free community server. We're keen to hear your thoughts and suggestions on how to enhance *Rate My Digs*.
                    """)
        provide_feedback_function() 

    st.write("")
    
    col4, col5 = st.columns(2)
    with col4:
        container = st.container(border=True)
        container.caption("""
        **This Streamlit App Contains the Following Data:**\n
        **(i)** Housing in Multiple Occupation (HMO) Licence Register", (c) Leeds City Council, 2024: 
        [Data Mill North](https://datamillnorth.org/dataset/2o13g/houses-in-multiple-occupation-licence-register/).\n
        This information is licensed under the terms of the Open Government Licence.
        
        **(ii)** Postcode Coordinates Data: [Postcode.io]("https://postcodes.io").\n
        This information is available under the MIT licence.
        """)
