# customer-ltv-estimator
A machine learning web app that predicts both **Customer Churn** and **Customer Lifetime Value (LTV)** using customer transaction behavior data.

**Live Demo: https://customer-ltv-estimator-demo.onrender.com**

_Note on Loading Time_
```text
Because the backend API is hosted on a free Render service, it automatically goes to sleep after periods of
inactivity. If you visit the app after it has been idle, the first request can take up to 30 seconds to
respond while the server wakes up. Subsequent requests will be much faster.
```

- Frontend: https://customer-ltv-estimator-demo.onrender.com
- Backend API: https://customer-ltv-estimator-api.onrender.com/predict

---

**Features**
- Dual ML model architecture:
  - `RandomForestRegressor` for LTV prediction
  - `RandomForestClassifier` for churn prediction
- Real-time predictions based on 7 input features:
  - Number of orders
  - Total spent
  - Average order value
  - Tenure
  - Recency
  - Days since last purchase
  - Average days between orders
- FastAPI backend with `/predict` endpoint
- Streamlit UI for clean, accessible input + output
- SQLite-based data pipeline with raw transactions and churn labels
- Deployed entirely on free-tier Render services

---

**Dataset**

The project is based on the [UCI Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail), containing ~500,000 historical transactions from a UK-based e-commerce retailer.

Churn labels were engineered using SQL based on inactivity:
```sql
CASE WHEN days_since_last_purchase > 180 THEN 1 ELSE 0 END AS churned
```
---

**Project Structure**
```text
├── app.py                      # Streamlit frontend
├── scripts/
│   ├── churn_ltv_api.py        # FastAPI backend
│   ├── train_churn_model.py    # Churn model training
│   ├── train_ltv_model.py      # LTV model training
│   ├── load_data.py            # Data loading utility
│   ├── generate_churn_labels.py# SQL churn labeling
│   └── generate_churn_features.py
├── models/
│   ├── churn_model.pkl         # Saved churn classifier
│   └── ltv_model.pkl           # Saved LTV regressor
├── data/                       # SQLite database and source data (excluded from GitHub)
├── notebooks/                  # EDA and exploration notebooks
├── requirements.txt
├── render.yaml                 # Infrastructure definition for Render deployment
└── README.md
```

---

**How to Run Locally**

1. Clone the repository

```text
git clone https://github.com/jacobhorne-jth@gmail.com/customer-ltv-estimator.git
cd customer-ltv-estimator
```
2. Create a virtual environment and activate it:
```text
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
3. Install dependencies:
```text
pip install -r requirements.txt
```
4. Train the models (optional if not using pre-trained .pkl files):
```text
python scripts/train_churn_model.py
python scripts/train_ltv_model.py
```
5. Run the API server
```text
uvicorn scripts.churn_ltv_api:app --reload
```
6. Open the Streamlit frontend in another terminal:
```text
streamlit run app.py
```

---

**Deployment**
- Backend: Render (FastAPI server)
- Frontend: Render (Streamlit app)
- Defined in render.yaml for 1-click deploy

**Example Prediction**

Input:
```text
{
  "num_orders": 15,
  "total_spent": 1125.50,
  "avg_order_value": 75.03,
  "tenure_days": 270,
  "recency_days": 30,
  "avg_days_between_orders": 18.0,
  "days_since_last_purchase": 30
}
```
Output:
```text
{
  "churn_prediction": 0,
  "predicted_ltv": 1056.38
}
```


**License**

This project is licensed under the MIT License.

**Acknowledgments**
- UCI Online Retail Dataset
- scikit-learn, FastAPI, Streamlit, Render for making full-stack ML deployment accessible
