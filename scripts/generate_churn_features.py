import sqlite3
import pandas as pd

def generate_churn_features(db_path='data/online_retail.db'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Read in customer features and churn labels
    features_df = pd.read_sql_query("SELECT * FROM customer_features;", conn)
    labels_df = pd.read_sql_query("SELECT * FROM churn_labels;", conn)

    # Merge them on CustomerID
    merged_df = pd.merge(features_df, labels_df, on="CustomerID", how="inner")

    # Save the result as a new table
    merged_df.to_sql("customer_churn_features", conn, if_exists="replace", index=False)

    conn.close()
    print("Created 'customer_churn_features' table")

if __name__ == '__main__':
    generate_churn_features()
