import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score
import joblib

def load_churn_data(db_path='data/online_retail.db'):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM customer_churn_features;"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def train_and_save_model():
    df = load_churn_data()

    # Drop datetime fields — not suitable for training directly
    df = df.drop(columns=['first_purchase_date', 'last_purchase_date'], errors='ignore')

    # Split features and target
    X = df.drop(columns=['CustomerID', 'churned', 'first_purchase_date', 'last_purchase_date'], errors='ignore')
    y = df['churned']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }

    # Grid search with 5-fold cross-validation
    grid_search = GridSearchCV(
        RandomForestClassifier(random_state=42),
        param_grid,
        cv=5,
        scoring='accuracy',
        verbose=1,
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    # Evaluate
    y_pred = best_model.predict(X_test)
    print("Best Params:", grid_search.best_params_)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Save best model
    joblib.dump(best_model, 'models/churn_model.pkl')
    print("Model saved!")

if __name__ == '__main__':
    train_and_save_model()