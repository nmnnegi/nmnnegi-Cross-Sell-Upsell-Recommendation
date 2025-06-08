import psycopg
import pandas as pd

def get_connection():
    return psycopg.connect(
        dbname="zeeproc",
        user="zeeproc_user",
        password="MyzPOzDAEOa67RZ3QmXjDL7IyoDKIcaC",
        host="dpg-d12od0c9c44c738hj96g-a.singapore-postgres.render.com",
        port=5432
    )

def fetch_customer_data(customer_id):
    with get_connection() as conn:
        # psycopg3 uses "conn.execute" with context manager
        query = "SELECT * FROM customer_purchases WHERE customer_id = %s"
        df = pd.read_sql_query(query, conn, params=(customer_id,))
    return df


