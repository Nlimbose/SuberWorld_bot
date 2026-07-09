import sqlite3

db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")

db.commit()


def add_user(user_id, username, first_name):
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES(?,?,?)",
        (user_id, username, first_name)
    )
    db.commit()


def get_users():
    cursor.execute("SELECT user_id FROM users")
    return cursor.fetchall()


def users_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]
