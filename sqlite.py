import sqlite3
from datetime import datetime

# Establish a connection to the SQLite database with thread check disabled
try:
    conn = sqlite3.connect("chat_logs.db", check_same_thread=False)
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Database connection failed: {e}")
    raise

# Create the table if it doesnt already exist
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
except sqlite3.Error as e:
    print(f"Failed to create table: {e}")
    raise

def insertChat(chat_id: str, role: str, content: str):
    """
    Inserts a single chat message into the chat_logs table.

    Args:
        chat_id (str): Unique identifier for the chat session.
        role (str): The role of the sender (e.g., 'user' or 'assistant').
        content (str): The message content.
    """
    try:
        cursor.execute(
            "INSERT INTO chat_logs (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Failed to insert chat message: {e}")

def getChatMessages(chat_id: str):
    """
    Retrieves all messages for a given chat session, ordered by timestamp.

    Args:
        chat_id (str): Unique identifier for the chat session.

    Returns:
        List[dict]: A list of dictionaries with 'role' and 'content' keys.
    """
    try:
        cursor.execute(
            "SELECT role, content FROM chat_logs WHERE chat_id = ? ORDER BY timestamp",
            (chat_id,)
        )
        rows = cursor.fetchall()
        return [{'role': role, 'content': content} for role, content in rows]
    except sqlite3.Error as e:
        print(f"Failed to fetch chat messages: {e}")
        return []

def listChats():
    """
    Lists all distinct chat sessions with their creation timestamp.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing (chat_id, created_at).
    """
    try:
        cursor.execute('''
            SELECT DISTINCT chat_id, MIN(timestamp) as created_at 
            FROM chat_logs 
            GROUP BY chat_id 
            ORDER BY created_at DESC
        ''')
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Failed to list chat sessions: {e}")
        return []
