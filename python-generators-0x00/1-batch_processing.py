#!/usr/bin/env python3
"""
Batch processing of user data from a database using generators.

Uses `cursor.fetchmany` and Python generators to process large datasets 
without loading the entire result set into memory.
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# --- Configuration (Centralized Constants) ---

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

# --- Generator Function ---
def stream_users_in_batches(batch_size: int):
    """
    Connects to the database and yields rows in manageable batches using fetchmany.
    This function acts as a resource-efficient data producer (Generator).
    
    Args:
        batch_size: The number of records to fetch in each database call.

    Yields:
        A list of dictionaries, where each dictionary is one user record batch.
    """
    try:
        # Use context manager for automatic connection closing
        with mysql.connector.connect(**DB_CONFIG) as connection:
            if not connection.is_connected():
                raise ConnectionError(f"Failed to connect to database at {DB_CONFIG['host']}")

            # Use dictionary=True for cleaner access (row['column_name'])
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM user_data;")

                # Continues until the cursor has yielded all rows
                while True:
                    batch_of_rows = cursor.fetchmany(size=batch_size)
                    if not batch_of_rows:
                        break # End of result set
                    yield batch_of_rows
                        
    except Error as e:
        print(f"Database Error: Could not stream data. Details: {e}")
    except ConnectionError as e:
        print(f"Connection Error: {e}")


# --- Processing Function ---
def batch_processing(batch_size):
    """
    Consumes batches from the generator(stream_users_in_batches) and processes them.
    Filters users over the age of 25 in a memory-efficient manner.
    
    Args:
        batch_size: The desired size of each batch.
    """
    
    # Iterates over the batches yielded by the generator
    for batch in stream_users_in_batches(batch_size):
        
        # Filtering is done using a list comprehension - which keeps the code concise and Pythonic.
        filtered_users = [
            user for user in batch 
            if user.get('age', 0) > 25
        ]

        # Print filtered users
        if filtered_users:
            print(f"Users found over age 25:")
            for user in filtered_users:
                print(user)
        else:
            print(f"No users found over age 25 in this batch.")
