# scripts/load_churn_data.py

import pandas as pd
import sqlite3

def load_churn_data(db_path='../data/online_retail.db'):
    connection = sqlite3.connect(db_path)
    
    # Join customer features with churn labels
    query = """
    SELECT cf.*, cl.churned
    FROM customer_features cf
    JOIN churn_labels cl
    ON cf.CustomerID = cl.CustomerID
    """
    
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df
    