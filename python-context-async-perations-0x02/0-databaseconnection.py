#!/usr/bin/env python3
"""
A custom context manager for handling database connections automatically.
"""

import sqlite3


class DatabaseConnection:
    """Context manager to handle opening and closing database connections."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open the database connection and return the connection object."""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection automatically."""
        if self.conn:
            self.conn.close()
        # Return False to propagate exceptions (if any)
        return False


if __name__ == "__main__":
    # Example usage of the context manager
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
