from db_utils import fetch_customer_data

def get_customer_profile(customer_id):
    df = fetch_customer_data(customer_id)
    if df.empty:
        return None
    row = df.iloc[0]
    return {
        "customer_id": customer_id,
        "name": row["customer_name"],
        "industry": row["industry"],
        "location": row["location"],
        "annual_revenue": int(row["annual_revenue"]),
        "employee_count": int(row["number_of_employees"]),
        "priority": row["customer_priority"],
        "current_products": list(df["current_products"].dropna().unique()),
        "product_usage": int(df["product_usage"].max())
    }
