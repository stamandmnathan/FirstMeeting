import sqlite3
import hashlib


DB_PATH = "users.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        conn.commit()
    _seed_default_user()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _seed_default_user():
    """Insert a default user if the table is empty."""
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                ("admin", _hash_password("admin123")),
            )
            conn.commit()


def validate_user(username: str, password: str) -> bool:
    password_hash = _hash_password(password)
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        ).fetchone()
    return row is not None
