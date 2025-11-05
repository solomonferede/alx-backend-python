#!/usr/bin/env python3
"""
Computes the average age of users from a MySQL database using a generator
to stream data efficiently without loading the entire dataset into memory.
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# --- Load Environment Variables ---
load_dotenv()

# --- Database Configuration ---
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_DATABASE', 'ALX_prodev'),
}


# --- Generator Function: Stream User Ages ---
def stream_user_ages():
    """
    Lazily fetches user ages from the database.
    Yields one user age at a time.
    """
    connection = None
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Query only the 'age' column
        cursor.execute("SELECT age FROM user_data;")

        # Fetch rows one by one using an iterator
        for (age,) in cursor:
            if age is not None:   # Skip NULL ages if any
                yield age

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# --- Function to Calculate Average Age ---
def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute the average age efficiently.
    """
    total_age = 0
    count = 0

    # Loop 1: Consume the generator lazily (one age at a time)
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Compute the average safely
    if count == 0:
        print("No users found in the database.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")


# --- Main Entry Point ---
if __name__ == "__main__":
    calculate_average_age()
