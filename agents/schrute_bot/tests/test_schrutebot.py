import sqlite3
import pytest

DB_FILE = "schrutebot.db"

def get_dwight_quotes_count():
    """Fetch the count of quotes in the dwight_quotes table."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dwight_quotes")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def test_dwight_quotes_not_empty():
    """Test that the dwight_quotes table is not empty."""
    count = get_dwight_quotes_count()
    assert count > 0, "❌ Test failed: No Dwight quotes found in the database. Run setup.py to populate quotes."
