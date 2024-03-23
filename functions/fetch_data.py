import streamlit as st
import duckdb
from loguru import logger


def connect_to_motherduck(database):
    """
    Create database connection object
    """
    
    token = st.secrets['mother_token']
    if token is None:
        raise ValueError("MotherDuck token not found in environment variables")

    connection_string = f'md:{database}?motherduck_token={token}'
    try:
        con = duckdb.connect(connection_string)
    except Exception as e:
        logger.warning(f"An error occured {e}")
    return con


def fetch_data(con):
    """
    Fetch df containing counts of addresses grouped by postcode and the corresponding coordinates
    """
    schema = st.secrets["mother_schema"]
    table_name = st.secrets["table_name"]
    
    query = f"""
    SELECT COUNT(DISTINCT Address) AS UniqueAddressCount, 
    postcode, 
    coordinates
    FROM {schema}.{table_name}
    GROUP BY postcode, coordinates
    """
    result = con.execute(query)
    df = result.fetchdf()
    return df


def fetch_data2(con):
    """
    Fetch df containing information on addresses
    """
    schema = st.secrets["mother_schema"]
    table_name = st.secrets["table_name"]
    
    query = f"""
    SELECT DISTINCT address,
    coordinates,
    max_tenants
    FROM {schema}.{table_name}
    """
    result = con.execute(query)
    df = result.fetchdf()
    return df


def fetch_data3(con):
    """
    Fetch df containing information on addresses
    """
    schema = st.secrets["mother_schema"]
    table_name = st.secrets["table_name"]
    
    query = f"""
    SELECT DISTINCT address,
    hmo_id
    FROM {schema}.{table_name}
    """
    result = con.execute(query)
    df = result.fetchdf()
    return df
