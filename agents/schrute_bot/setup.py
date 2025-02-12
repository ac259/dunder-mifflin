import sqlite3
from datasets import load_dataset

DB_FILE = "schrutebot.db"

def create_tables():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dwight_quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT UNIQUE
        )
    ''')
    
    conn.commit()
    conn.close()

def fetch_and_store_dwight_quotes():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    dataset = load_dataset("jxm/the_office_lines")
    dwight_lines = [row["line"] for row in dataset["train"] if row["speaker"] == "Dwight Schrute"]
    
    for quote in dwight_lines:
        try:
            cursor.execute("INSERT INTO dwight_quotes (quote) VALUES (?)", (quote,))
        except sqlite3.IntegrityError:
            continue  # Ignore duplicate entries

    conn.commit()
    conn.close()
    print("✅ Dwight Schrute quotes successfully stored!")

if __name__ == "__main__":
    create_tables()
    fetch_and_store_dwight_quotes()
