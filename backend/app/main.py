from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sys
import os

# Add root project path to Python Path so we can import analytics
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from analytics.scoring.churn_model import predict_with_explanation

app = FastAPI(
    title="Sthirta Churn Prediction API",
    description="API for predicting customer churn and generating SHAP explainability.",
    version="1.0.0"
)

class CustomerData(BaseModel):
    Tenure_Months: int = Field(..., ge=1, le=100)
    Monthly_Charges: float = Field(..., ge=0)
    Contract_Type: int = Field(..., description="0: Month-to-month, 1: One year, 2: Two year")
    Tech_Support: int = Field(..., description="0: No, 1: Yes")
    Internet_Service: int = Field(..., description="0: No, 1: DSL, 2: Fiber optic")

@app.get("/")
def read_root():
    return {"message": "Sthirta AI Churn Engine is running. Visit /docs for API documentation."}

@app.post("/predict")
def predict_churn(customer: CustomerData):
    """
    Predicts churn for a single customer and provides SHAP feature importance.
    """
    try:
        # Calculate derived feature if needed, or pass directly
        # Using Total_Charges roughly as Tenure * Monthly_Charges
        total_charges = customer.Tenure_Months * customer.Monthly_Charges
        
        customer_dict = {
            'Tenure_Months': customer.Tenure_Months,
            'Monthly_Charges': customer.Monthly_Charges,
            'Total_Charges': total_charges,
            'Contract_Type': customer.Contract_Type,
            'Tech_Support': customer.Tech_Support,
            'Internet_Service': customer.Internet_Service
        }
        
        result = predict_with_explanation(customer_dict)
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
