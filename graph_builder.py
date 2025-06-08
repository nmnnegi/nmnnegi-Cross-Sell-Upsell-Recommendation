from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict
from agents.customer_context import get_customer_profile
from agents.purchase_pattern import analyze_purchase_patterns
from agents.product_affinity import suggest_related_products
from agents.opportunity_scoring import score_opportunities
from agents.report_generator import generate_report
from db_utils import fetch_customer_data

# Define state structure
class GraphState(TypedDict):
    customer_id: str
    profile: Dict[str, Any]
    df: Any  # Pandas DataFrame
    patterns: Dict[str, list]
    affinities: list
    scored: list
    report: str
    error: str

def customer_context_node(state: GraphState) -> GraphState:
    """Fetch customer profile"""
    try:
        customer_id = state["customer_id"]
        profile = get_customer_profile(customer_id)
        if not profile:
            return {"error": f"Customer {customer_id} not found"}
        return {"profile": profile}
    except Exception as e:
        return {"error": f"Profile error: {str(e)}"}

def pattern_analysis_node(state: GraphState) -> GraphState:
    """Analyze purchase patterns"""
    if "error" in state:
        return state
    
    try:
        customer_id = state["customer_id"]
        df = fetch_customer_data(customer_id)
        patterns = analyze_purchase_patterns(df, customer_id)
        return {"df": df, "patterns": patterns}
    except Exception as e:
        return {"error": f"Pattern analysis error: {str(e)}"}

def affinity_node(state: GraphState) -> GraphState:
    """Find product affinities"""
    if "error" in state:
        return state
    
    try:
        affinities = suggest_related_products(state["patterns"]["frequent"])
        return {"affinities": affinities}
    except Exception as e:
        return {"error": f"Affinity error: {str(e)}"}

def scoring_node(state: GraphState) -> GraphState:
    """Score opportunities"""
    if "error" in state:
        return state
    
    try:
        scored = score_opportunities(
            state["patterns"]["frequent"],
            state["patterns"]["missing"],
            state["affinities"]
        )
        return {"scored": scored}
    except Exception as e:
        return {"error": f"Scoring error: {str(e)}"}

def report_node(state: GraphState) -> GraphState:
    """Generate final report"""
    if "error" in state:
        # Handle error case
        return {"report": f"ERROR: {state['error']}"}
    
    try:
        report = generate_report(state["profile"], state["scored"])
        return {"report": report}
    except Exception as e:
        return {"report": f"Report generation error: {str(e)}"}

# Build the workflow graph
graph = StateGraph(GraphState)

# Add nodes to the graph
graph.add_node("get_profile", customer_context_node)
graph.add_node("analyze_patterns", pattern_analysis_node)
graph.add_node("find_affinities", affinity_node)
graph.add_node("score_opportunities", scoring_node)
graph.add_node("generate_report", report_node)

# Define workflow sequence
graph.set_entry_point("get_profile")
graph.add_edge("get_profile", "analyze_patterns")
graph.add_edge("analyze_patterns", "find_affinities")
graph.add_edge("find_affinities", "score_opportunities")
graph.add_edge("score_opportunities", "generate_report")
graph.add_edge("generate_report", END)  # End after report generation

# Compile the workflow
workflow = graph.compile()

def run_pipeline(customer_id: str):
    """Execute the workflow for a given customer"""
    result = workflow.invoke({"customer_id": customer_id})
    
    return {
        "customer_id": customer_id,
        "report": result.get("report", "No report generated"),
        "recommendations": result.get("scored", []),
        "error": result.get("error", "")
    }

# Example usage
if __name__ == "__main__":
    result = run_pipeline("C003")
    print(result["report"])