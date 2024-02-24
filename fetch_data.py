from streamlit import secrets
import duckdb

def connect_to_motherduck(database):
    """_summary_
    Args:
        database (_type_): _description_
    Raises:
        ValueError: _description_
    Returns:
        _type_: _description_
    """
    token = secrets['mother_token']
    if token is None:
        raise ValueError("MotherDuck token not found in environment variables")

    connection_string = f'md:{database}?motherduck_token={token}'
    con = duckdb.connect(connection_string)
    print("Connection Made Baby!")
    return con


def fetch_data(con):
        query = """
        SELECT COUNT(Address), Postcode
        FROM leeds_hmo_15022024 
        GROUP BY Postcode
        """
        result = con.execute(query)
        return result.fetchdf()
    
