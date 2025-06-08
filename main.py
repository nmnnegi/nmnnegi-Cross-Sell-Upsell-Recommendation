from fastapi import FastAPI
from graph_builder import build_graph

app = FastAPI()

@app.get("/recommendation")
def get_recommendation(customer_id: str):
    return build_graph(customer_id)
