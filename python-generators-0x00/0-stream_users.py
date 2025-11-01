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
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

# Database configuration using environment variables
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_DATABASE", "ALX_prodev")
}

def stream_users():
    """Generator that streams rows from the user_data table one by one."""
    connection = None
    cursor = None

    try:
        # Connect to the database
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if not connection.is_connected():
                raise ConnectionError(f"Failed to connect to database at {DB_CONFIG['host']}")
        
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data;")

                # Single loop: yield each row
                while True:
                    row = cursor.fetchone()
                    if row is None:
                        break  # No more rows
                    yield row

    except Error as e:
        print("Error while streaming users:", e)
