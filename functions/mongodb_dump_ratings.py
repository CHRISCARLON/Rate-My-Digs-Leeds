from pymongo.mongo_client import MongoClient
import streamlit as st


def create_connection():
    uri = st.secrets['mongomongo']  
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    return client

def load_data_into_collection(client, db_name: str, collection_name: str, data: dict):
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_one(data)

def user_input_and_data_upload(df):
    # Select an address
    st.markdown('## Rate My Digs Feedback Form')
    st.markdown('#### **Please select your address and provide your feedback below!**')
    selected_address = st.selectbox('Select an Address', options=df['address'].unique())

    if selected_address:
        # User inputs for happiness and rent
        happiness_level = st.number_input("On a scale of 1-10, how happy are you with your accommodation?", min_value=1, max_value=10, value=5, step=1)
        rent_amount = st.number_input("How much rent do you pay per month in £s?", min_value=0.0, format="%.2f")

        # Button to submit data
        if st.button("Submit Feedback"):
            data = {
                "address": selected_address,
                "happiness_level": happiness_level,
                "rent_amount": rent_amount
            }

            # MongoDB operations
            client = create_connection()
            load_data_into_collection(client, st.secrets["db_mongo"], st.secrets["mongo_collect"], data)
            st.success("Success! Thank you for your feedback!")
