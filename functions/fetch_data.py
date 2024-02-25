import streamlit as st
import duckdb

def connect_to_motherduck(database):
    """
    Create database connection object
    """
    
    token = st.secrets['mother_token']
    if token is None:
        raise ValueError("MotherDuck token not found in environment variables")

    connection_string = f'md:{database}?motherduck_token={token}'
    con = duckdb.connect(connection_string)
    return con


def fetch_data(con):
    """
    Fetch df containing counts of addresses grouped by postcode and the corresponding coordinates
    """
    
    query = """
    SELECT COUNT(DISTINCT Address) AS UniqueAddressCount, 
    Postcode, 
    Coordinates
    FROM leeds_hmo_15022024 
    GROUP BY Postcode, Coordinates
    """
    result = con.execute(query)
    df = result.fetchdf()
    return df

def fetch_data2(con):
    """
    Fetch df containing all information on addresses
    """
    
    query = """
    SELECT DISTINCT Address, 
    "Street name", 
    "Maximum Permitted Number of Tenants",
    "Licence Holder",
    Coordinates
    from leeds_hmo_15022024
    """
    result = con.execute(query)
    df = result.fetchdf()
    return df
