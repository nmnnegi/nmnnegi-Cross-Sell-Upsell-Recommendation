import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_engine():
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")

    connection_string = (
        f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    )
    engine = create_engine(connection_string)
    return engine

engine = get_engine()


def fetch_customer_data(customer_id):
    query = "SELECT * FROM customer_purchases WHERE customer_id = %s"
    df = pd.read_sql_query(query, engine, params=(customer_id,))
    return df

# Example usage:



