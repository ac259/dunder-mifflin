import sqlite3
import pandas as pd

DB_FILE = "schrutebot.db"
PARQUET_FILE = "train-00000-of-00001-f3693a9d93680a13.parquet"
TABLE_NAME = "office_lines"

def create_database():
    """Creates a SQLite database and dynamically creates a table based on the Parquet file columns."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Load Parquet file into a DataFrame
    df = pd.read_parquet(PARQUET_FILE)

    # Dynamically create table schema based on Parquet columns
    columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {TABLE_NAME}  ({columns})')
    # Ensure the Dwight quotes table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dwight_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_text TEXT UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

def populate_office_lines():
    """Inserts the entire Parquet dataset into the office_lines table."""
    conn = sqlite3.connect(DB_FILE)
    
    # Load Parquet file
    df = pd.read_parquet(PARQUET_FILE)

    # Insert data into SQLite (replace existing duplicates)
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print(f"✅ Entire dataset stored in {TABLE_NAME}!")

def extract_dwight_quotes():
    """Extracts Dwight Schrute's quotes into the dwight_quotes table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Ensure the table exists before inserting
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dwight_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            line_text TEXT UNIQUE
        )
    ''')

    # Extract only Dwight's quotes from the office_lines table
    cursor.execute(f'''
        INSERT INTO dwight_quotes (line_text)
        SELECT line_text FROM office_lines WHERE speaker = 'Dwight'
        ON CONFLICT(line_text) DO NOTHING
    ''')

    conn.commit()
    conn.close()
    print("✅ Dwight Schrute quotes extracted successfully!")


if __name__ == "__main__":
    create_database()
    populate_office_lines()
    extract_dwight_quotes()
