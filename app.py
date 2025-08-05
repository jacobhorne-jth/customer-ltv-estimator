# app.py

import streamlit as st
import requests

st.set_page_config(page_title="Customer LTV & Churn Estimator", layout="centered")

st.title("🧮 Customer LTV & Churn Estimator")

st.markdown("Enter customer features to predict Lifetime Value and Churn risk.")

# Input fields
num_orders = st.number_input("Number of Orders", min_value=0)
total_spent = st.number_input("Total Spent ($)", min_value=0.0)
avg_order_value = st.number_input("Average Order Value ($)", min_value=0.0)
tenure_days = st.number_input("Tenure (days since first purchase)", min_value=0)
recency_days = st.number_input("Recency (days since most recent purchase)", min_value=0)
avg_days_between_orders = st.number_input("Average Days Between Orders", min_value=0.0)
days_since_last_purchase = st.number_input("Days Since Last Purchase", min_value=0.0)

# Send request
if st.button("Predict"):
    input_data = {
        "num_orders": num_orders,
        "total_spent": total_spent,
        "avg_order_value": avg_order_value,
        "tenure_days": tenure_days,
        "recency_days": recency_days,
        "avg_days_between_orders": avg_days_between_orders,
        "days_since_last_purchase": days_since_last_purchase
    }

    try:
        response = requests.post("https://customer-ltv-estimator-api.onrender.com/predict/", json=input_data)
        result = response.json()

        churn = result["churn_prediction"]
        ltv = result["predicted_ltv"]

        st.success(f"Predicted LTV: ${ltv:,.2f}")
        st.success("Churn Risk: High" if churn else "Churn Risk: Low")
    except Exception as e:
        st.error(f"Error: {e}")
