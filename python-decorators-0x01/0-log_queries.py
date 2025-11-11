import sqlite3
import functools
from datetime import datetime


# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{now} [LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No SQL query found.")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def create_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# === Create table with email field ===
create_users(query="""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    email TEXT
);
""")

# === Insert users with email addresses ===
create_users(query="INSERT INTO users (name, age, email) VALUES ('SOLOMON', 31, 'solomon@example.com');")
create_users(query="INSERT INTO users (name, age, email) VALUES ('ALEX', 28, 'alex@example.com');")
create_users(query="INSERT INTO users (name, age, email) VALUES ('MARIA', 25, 'maria@example.com');")
create_users(query="INSERT INTO users (name, age, email) VALUES ('JOHN', 35, 'john@example.com');")

# === Fetch and display all users ===
users = fetch_all_users(query="SELECT * FROM users;")
print("\nAll Users:")
for user in users:
    print(user)
