from fastapi import FastAPI, HTTPException, Query
from graph_builder import run_pipeline
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Product Recommendation API",
    description="API for generating personalized product recommendations",
    version="1.0.0"
)

# Define response models
class RecommendationItem(BaseModel):
    product: str
    score: int
    rationale: str

class RecommendationResponse(BaseModel):
    customer_id: str
    report: str
    recommendations: list[RecommendationItem]
    success: bool

class ErrorResponse(BaseModel):
    error: str
    customer_id: str
    details: str

@app.get("/")
async def health_check():
    """Service health check endpoint"""
    return {
        "status": "running",
        "version": app.version,
        "endpoint": "/recommendation?customer_id=C001"
    }

@app.get("/recommendation", 
         response_model=RecommendationResponse,
         responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_recommendation(
    customer_id: str = Query(..., 
                           title="Customer ID", 
                           description="Customer identifier starting with 'C' followed by digits",
                           example="C003")
):
    """
    Generate cross-sell recommendations for a customer
    
    - **customer_id**: Unique customer identifier (e.g., C003)
    """
    logger.info(f"Processing recommendation request for customer: {customer_id}")
    
    try:
        # Validate customer ID format
        if not customer_id.startswith('C') or not customer_id[1:].isdigit():
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid customer ID format",
                    "customer_id": customer_id,
                    "details": "Must start with 'C' followed by digits (e.g., C003)"
                }
            )
            
        # Execute recommendation pipeline
        result = run_pipeline(customer_id)
        
        # Handle pipeline errors
        if not result.get("success", False):
            logger.error(f"Pipeline failed for customer {customer_id}: {result.get('report', '')}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Recommendation generation failed",
                    "customer_id": customer_id,
                    "details": result.get("report", "Unknown error in pipeline")
                }
            )
            
        # Format recommendations
        formatted_recs = [
            RecommendationItem(
                product=rec["product"],
                score=rec["score"],
                rationale=rec["rationale"]
            )
            for rec in result.get("recommendations", [])
        ]
        
        logger.info(f"Successfully generated recommendations for {customer_id}")
        
        return RecommendationResponse(
            customer_id=customer_id,
            report=result.get("report", ""),
            recommendations=formatted_recs,
            success=True
        )
        
    except HTTPException as he:
        # Re-raise our custom HTTP exceptions
        raise he
        
    except Exception as e:
        logger.exception(f"Unexpected error processing {customer_id}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "customer_id": customer_id,
                "details": str(e)
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

