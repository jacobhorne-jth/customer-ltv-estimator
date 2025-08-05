from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load trained models
churn_model = joblib.load("models/churn_model.pkl")
ltv_model = joblib.load("models/ltv_model.pkl")

# Define expected input schema for both models
class CustomerFeatures(BaseModel):
    num_orders: int
    total_spent: float
    avg_order_value: float
    tenure_days: int
    recency_days: int
    avg_days_between_orders: float
    days_since_last_purchase: float


@app.post("/predict/")
def predict(customer: CustomerFeatures):
    input_df = pd.DataFrame([customer.dict()])

    churn_features = input_df[[
        'num_orders',
        'total_spent',
        'avg_order_value',
        'tenure_days',
        'recency_days',
        'avg_days_between_orders',
        'days_since_last_purchase'
    ]]

    ltv_features = input_df[[
        'num_orders',
        'avg_order_value',
        'tenure_days',
        'recency_days',
        'avg_days_between_orders'  # <- This one is required
    ]]

    churn_pred = churn_model.predict(churn_features)[0]
    ltv_pred = max(0.0, ltv_model.predict(ltv_features)[0])

    return {
        "churn_prediction": int(churn_pred),
        "predicted_ltv": round(float(ltv_pred), 2)
    }
