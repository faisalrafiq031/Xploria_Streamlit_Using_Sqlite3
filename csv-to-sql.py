import sqlite3
import pandas as pd

# Path to your local CSV file
csv_path = r"D:\Data Engineer Internship CodeGurus\SQL - DATA ENGINEERING\Streamlit-sqlite3\Top_100_2.csv"

# Load CSV into pandas DataFrame
df = pd.read_csv(csv_path)

# Connect to your SQLite database
db_path = r"D:\Data Engineer Internship CodeGurus\SQL - DATA ENGINEERING\Streamlit-sqlite3\data.db"
conn = sqlite3.connect(db_path)

# Store the data into a new table called `xploria_data` (replace if exists)
df.to_sql("Top_100_AI", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("CSV data loaded successfully into 'Top_100_AI' table.")
