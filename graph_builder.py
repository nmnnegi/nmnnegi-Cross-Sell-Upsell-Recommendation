from agents.customer_context import get_customer_profile
from agents.purchase_pattern import analyze_purchase_patterns
from agents.product_affinity import suggest_related_products
from agents.opportunity_scoring import score_opportunities
from agents.report_generator import generate_report
from db_utils import fetch_customer_data

def build_graph(customer_id):
    profile = get_customer_profile(customer_id)
    if not profile:
        return {"error": "Customer not found"}

    df = fetch_customer_data(customer_id)
    patterns = analyze_purchase_patterns(df, customer_id)
    affinities = suggest_related_products(patterns['frequent'])
    scored = score_opportunities(patterns['frequent'], patterns['missing'], affinities)
    report = generate_report(profile, scored)

    return {
        "customer_id": customer_id,
        "report": report,
        "recommendations": scored
    }
