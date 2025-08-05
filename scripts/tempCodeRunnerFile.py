import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from load_data import load_customer_features

def train_and_evaluate():
    df = load_customer_features()

    # Features and target
    X = df.drop(columns=['CustomerID', 'total_spent', 'first_purchase_date', 'last_purchase_date'])
    y = df['total_spent']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²:   {r2:.2f}")

    # Save model
    joblib.dump(model, 'models/ltv_model.pkl')

if __name__ == '__main__':
    train_and_evaluate()
