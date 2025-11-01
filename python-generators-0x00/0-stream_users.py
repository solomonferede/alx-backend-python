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

# 0-stream_users.py

import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that streams rows from the user_data table one by one."""
    connection = None
    cursor = None

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='solomon',            # update if needed
            password='solomon@2025',   # update with your password
            database='ALX_prodev'
        )

        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT * FROM user_data;")

        # Single loop: yield each row
        for row in cursor:
            yield row

    except Error as e:
        print("Error while streaming users:", e)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
