#!/usr/bin/env python3
"""
Simulates fetching paginated data from a database using a generator.
The generator only fetches the next page when explicitly requested (lazily).
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# --- Load Environment Variables ---
# This line looks for the .env file and loads its contents into os.environ
load_dotenv()
print(f"The .env file has been loaded from: {os.getenv('DB_HOST')}")
print(f"The DB user: {os.getenv('DB_USER')}")
print(f"The DB database: {os.getenv('DB_DATABASE')}")

# WARNING: Hardcoding credentials is insecure. Use environment variables 
# in production. These defaults are for demonstrative purposes.
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_DATABASE', 'ALX_prodev'),
}
QUERY = "SELECT * FROM user_data;"

# --- Helper Function ---

def paginate_users(page_size, offset):
    """
    Fetches a single page of user data from the database.
    Uses LIMIT and OFFSET for efficient database pagination.
    """
    connection = None
    try:
        # Establish connection using the configuration
        connection = mysql.connector.connect(**DB_CONFIG)
        if not connection.is_connected():
            print("ERROR: Failed to connect to database.")
            return []

        cursor = connection.cursor(dictionary=True)
        
        # SQL with pagination parameters
        sql = f"{QUERY} LIMIT {page_size} OFFSET {offset}"
        cursor.execute(sql)
        
        # Fetch all rows for the current page
        page_data = cursor.fetchall()
        
        cursor.close()
        return page_data

    except Error as e:
        print(f"Database Error during pagination at offset {offset}: {e}")
        return []
    finally:
        # Ensure the connection is closed
        if connection and connection.is_connected():
            connection.close()

# --- Generator Function (The core of lazy loading) ---

def lazy_paginate(page_size):
    """
    A generator that lazily yields pages of data on demand.
    Uses only one loop to continuously calculate the offset and fetch the next page.
    """
    offset = 0
    
    # Loop 1: The single mandated loop runs indefinitely until the database returns no data.
    while True:
        # Fetch the next page using the current offset
        page_data = paginate_users(page_size, offset)
        
        # If the returned list is empty, we have reached the end of the table
        if not page_data:
            break
            
        # Yield the full list (the page) back to the caller
        yield page_data
        
        # Increment the offset for the next iteration (the next page request)
        offset += page_size

