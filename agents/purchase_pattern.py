from db_utils import fetch_customer_data
import pandas as pd

def analyze_purchase_patterns(df, customer_id):
    cust_df = df[df["customer_id"] == customer_id]
    industry = cust_df.iloc[0]["industry"]
    
    product_counts = cust_df["product"].value_counts().to_dict()
    peer_df = df[df["industry"] == industry]
    peer_products = peer_df["product"].value_counts().to_dict()
    
    missing_products = [p for p in peer_products if p not in product_counts]
    
    return {
        "frequent": list(product_counts.keys()),
        "missing": missing_products
    }
