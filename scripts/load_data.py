import pandas as pd
import sqlite3

def load_customer_features(db_path='data/online_retail.db'):
    connection = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM customer_features;", connection)
    connection.close()
    return df