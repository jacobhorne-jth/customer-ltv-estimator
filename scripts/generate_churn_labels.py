import sqlite3

def generate_churn_labels(db_path='data/online_retail.db'):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Drop the churn table if it exists
    cursor.execute("DROP TABLE IF EXISTS churn_labels;")

    # Create churn_labels table
    cursor.execute("""
        CREATE TABLE churn_labels AS
        WITH last_orders AS (
            SELECT CustomerID, MAX(InvoiceDate) AS last_purchase
            FROM transactions
            GROUP BY CustomerID
        ),
        dataset_max_date AS (
            SELECT MAX(InvoiceDate) AS max_date FROM transactions
        )
        SELECT 
            l.CustomerID,
            julianday(m.max_date) - julianday(l.last_purchase) AS days_since_last_purchase,
            CASE 
                WHEN julianday(m.max_date) - julianday(l.last_purchase) > 180 THEN 1
                ELSE 0
            END AS churned
        FROM last_orders l
        CROSS JOIN dataset_max_date m;
    """)

    connection.commit()
    connection.close()
    print("Churn_labels table created!")

if __name__ == '__main__':
    generate_churn_labels()
