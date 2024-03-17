from pymongo.mongo_client import MongoClient
from datetime import datetime
import streamlit as st

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

def user_input_and_data_upload(df):
    st.markdown('# Feedback Form')
    st.markdown('### **To start the process, please select your address and then provide your feedback:**')
    
    # Address selection with placeholder
    selected_address = st.selectbox('Please select/type in your address - you can use your postcode to speed this up.', options=[""] + list(df['address'].unique()), index=0, format_func=lambda x: "Please select an option..." if x == "" else x)

    if selected_address:
        # Satisfaction level input
        satisfaction_level = st.number_input(label="On a scale of 1-10, how happy are you with your accommodation?", min_value=1, max_value=10, value=5, step=1)
        
        # Rent amount input
        rent_amount = st.number_input(label="How much is your monthly rent in £s? (e.g. 500.00)", min_value=0.0, value=0.0, format="%.2f")
        
        # Occupation selection with placeholder
        occupation = st.selectbox(label="Are you a Student, Professional, or Other?", options=[""] + ["Student", "Professional", "Other"], index=0, format_func=lambda x: "Please select an option..." if x == "" else x)
        
        # Dealing with landlord directly or via an estate agent with placeholder
        dealing_with_landlord = st.selectbox(label="Do you deal with the landlord directly or via an Estate Agent?", options=[""] + ["Landlord directly", "Via an Estate Agent"], index=0, format_func=lambda x: "Please select an option..." if x == "" else x)
        
        # Mould presence selection with placeholder
        mould_presence = st.selectbox(label="During the last 6 months, has there been any mould and/or damp in your HMO?", options=[""] + ["Yes", "No", "Don't Know"], index=0, format_func=lambda x: "Please select an option..." if x == "" else x)
        
        # Leaks presence selection with placeholder
        leaks_presence = st.selectbox(label="During the last 6 months, have there been any leaks in your HMO?", options=[""] + ["Yes", "No", "Don't Know"], index=0, format_func=lambda x: "Please select an option..." if x == "" else x)
        
        # Leaks presence selection with placeholder
        maintenance_repairs = st.selectbox(label="When a maintenance problem is reported, how long does it take to be resolved?", options=[""] + ["Hours", "Days", "Weeks", "Months", "Problems are not resolved"], index=0, format_func=lambda x: "Please select an option..." if x == "" else x)
        
        if st.button("Submit HMO Feedback"):
            if selected_address and occupation and satisfaction_level and rent_amount and mould_presence and dealing_with_landlord and leaks_presence and maintenance_repairs:
                try:
                    
                    current_time_date = datetime.now()
                    
                    data = {
                        "address": selected_address,
                        "satisfaction_level": satisfaction_level,
                        "dealing_with_landlord": dealing_with_landlord,
                        "rent_amount": rent_amount, 
                        "occupation": occupation,
                        "mould_prescence": mould_presence,
                        "leaks_presence": leaks_presence,
                        "maintenance_repairs": maintenance_repairs,
                        "time_stamp": current_time_date
                    }

                    # MongoDB operations
                    client = create_connection()
                    load_data_into_collection(client, st.secrets["db_mongo"], st.secrets["mongo_collect"], data)
                    st.success("**Success! Thank you for your feedback!**")
                except Exception:
                    st.error("**An error occurred. Please try again later.")
            else:
                st.error("**Problem! Please fill in all fields before submitting your feedback!**")
