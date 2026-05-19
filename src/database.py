import sqlite3

DB_PATH = "journal.db"

def init_db():
    """Initializes the SQLite database and creates the profile table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Create a table to store profile facts as simple key-value pairs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            fact_key TEXT PRIMARY KEY,
            fact_value TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_fact(key: str, value: str):
    """Saves or updates a fact about the user in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_profile (fact_key, fact_value)
        VALUES (?, ?)
    ''', (key, value))
    conn.commit()
    conn.close()
    print(f"💾 [Database] Memorized: {key} -> {value}")

def get_all_facts() -> str:
    """Retrieves all stored facts as a single formatted string for the AI's context."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT fact_key, fact_value FROM user_profile')
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No facts remembered yet."
        
    facts = []
    for row in rows:
        facts.append(f"- {row[0]}: {row[1]}")
    return "\n".join(facts)