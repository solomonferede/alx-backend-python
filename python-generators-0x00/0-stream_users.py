"""
Objective:
    Create a generator that streams rows from an SQL database one by one.

Instructions:
    In 0-stream_users.py write a function that uses a generator to fetch rows
    one by one from the user_data table. You must use the 'yield' Python generator.

Prototype:
    def stream_users()

    - Connect to the ALX_prodev MySQL database
    - Fetch rows one by one from user_data table
    - Use a generator with only one loop
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """Generator that streams rows from the user_data table one by one."""
    connection = None
    cursor = None

    try:
        # Connect to database
        connection = mysql.connector.connect(
            host='localhost',
            user='solomon',            # change if needed
            password='solomon@2025',  # replace with your password
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # Use fetchone() repeatedly instead of iterating the cursor
            row = cursor.fetchone()
            while row:
                yield row
                row = cursor.fetchone()

    except Error as e:
        print("Error while streaming users:", e)

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()