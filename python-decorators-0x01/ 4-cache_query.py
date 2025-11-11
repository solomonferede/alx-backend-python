import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# === DB connection decorator ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# === Decorator to cache query results based on SQL string ===
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        if query is None:
            raise ValueError("SQL query must be provided as 'query' argument")
        
        # Check if query is already cached
        if query in query_cache:
            print(f"[CACHE] Using cached result for query: {query}")
            return query_cache[query]
        
        # Execute the query and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        print(f"[CACHE] Caching result for query: {query}")
        return result
    return wrapper

# === Example function using both decorators ===
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# === First call: caches the result ===
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call result:", users)

# === Second call: uses cached result ===
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call result:", users_again)
