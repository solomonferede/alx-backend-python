import time
import sqlite3
import functools


# === Decorator: opens and closes the DB connection ===
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


# === Decorator: retries operation on transient failure ===
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempt += 1
                    if attempt > retries:
                        print(f"[ERROR] Operation failed after {retries} retries: {e}")
                        raise
                    print(f"[WARN] Transient error occurred: {e}. Retrying in {delay}s... (Attempt {attempt}/{retries})")
                    time.sleep(delay)
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=5, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * cFROM users")
    return cursor.fetchall()


# === Attempt to fetch users with automatic retry on failure ===
users = fetch_users_with_retry()
print(users)
