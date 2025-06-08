import psycopg
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=5432
    )

def fetch_customer_data(customer_id):
    with get_connection() as conn:
        query = "SELECT * FROM customer_purchases WHERE customer_id = %s"
        df = pd.read_sql_query(query, conn, params=(customer_id,))
    return df



