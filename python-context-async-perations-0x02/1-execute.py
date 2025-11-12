#!/usr/bin/env python3
"""
A reusable class-based context manager to handle both
database connection and query execution automatically.
"""

import sqlite3


class ExecuteQuery:
    """Context manager that executes a given SQL query with parameters."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Establish the connection, execute the query, and return the results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the cursor and connection automatically."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Return False to allow exceptions to propagate if any occur
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (30,)

    with ExecuteQuery("users.db", query, params) as results:
        print(results)
