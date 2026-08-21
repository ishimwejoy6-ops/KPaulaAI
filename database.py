import sqlite3

DATABASE = "kpaula.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO messages (role, content)
        VALUES (?, ?)
        """,
        (role, content)
    )

    conn.commit()
    conn.close()


def get_messages():
    conn = get_connection()

    cursor = conn.execute("""
        SELECT role, content
        FROM messages
        ORDER BY id ASC
    """)

    messages = cursor.fetchall()

    conn.close()

    return messages


def clear_messages():
    conn = get_connection()

    conn.execute("DELETE FROM messages")

    conn.commit()
    conn.close()
