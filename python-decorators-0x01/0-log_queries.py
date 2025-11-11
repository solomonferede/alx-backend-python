import sqlite3
import functools
from datetime import datetime


#### decorator to log SQL queries
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

#### fetch users while logging the query
create_users(query="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER);")
create_users(query="INSERT INTO USERS (name, age) VALUES ('SOLOMON', '31');")
create_users(query="INSERT INTO USERS (name, age) VALUES ('ALEX', '28');")
create_users(query="INSERT INTO USERS (name, age) VALUES ('MARIA', '25');")
create_users(query="INSERT INTO USERS (name, age) VALUES ('JOHN', '35');")
users = fetch_all_users(query="SELECT * FROM users")
print(users)
