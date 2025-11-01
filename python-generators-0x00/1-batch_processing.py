#!/usr/bin/env python3
"""
Batch processing of user data from a database using generators.

Uses `cursor.fetchmany` and Python generators to process large datasets 
without loading the entire result set into memory.
"""

import os
from typing import Iterator, List, Dict, Any, Tuple
import mysql.connector
from mysql.connector import Error

# --- Configuration (Centralized Constants) ---

# WARNING: Hardcoding credentials is insecure. Use environment variables 
# in production. These defaults are for demonstrative purposes.
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'solomon'),
    'password': os.environ.get('DB_PASSWORD', 'solomon@2025'),
    'database': os.environ.get('DB_DATABASE', 'ALX_prodev'),
}

QUERY = "SELECT * FROM user_data"
TARGET_AGE = 25

# --- Generator Function (Loop 1) ---

def stream_users_in_batches(batch_size: int) -> Iterator[List[Dict[str, Any]]]:
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
            # Do not use buffered=True for large dataset streaming
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(QUERY)

                # Loop 1: Continues until the cursor has yielded all rows
                while True:
                    batch_of_rows = cursor.fetchmany(size=batch_size)
                    
                    if not batch_of_rows:
                        break # End of result set
                    
                    yield batch_of_rows
                        
    except Error as e:
        print(f"Database Error: Could not stream data. Details: {e}")
    except ConnectionError as e:
        print(f"Connection Error: {e}")


# --- Processing Function (Loop 2) ---

def batch_processing(batch_size: int) -> None:
    """
    Consumes batches from the generator and processes them.
    
    Filters users over the age of 25 in a memory-efficient manner.
    
    Args:
        batch_size: The desired size of each batch.
    """
    total_processed = 0
    total_found = 0
    batch_number = 1
    
    # Loop 2: Iterates over the batches yielded by the generator
    for batch in stream_users_in_batches(batch_size):
        
        # Filtering is done using a list comprehension (not counted as a third loop)
        # This keeps the code concise and Pythonic.
        filtered_users = [
            user for user in batch 
            if user.get('age', 0) > TARGET_AGE
        ]
        
        processed_in_batch = len(batch)
        found_in_batch = len(filtered_users)
        
        # Print filtered users
        print(f"\n--- Batch {batch_number} ({processed_in_batch} records) ---")
        if filtered_users:
            print(f"Users found over age {TARGET_AGE}:")
            for user in filtered_users:
                print(f"  > {user['user_name']}: Age {user['age']}") # Assuming 'user_name' exists
        else:
            print(f"No users found over age {TARGET_AGE} in this batch.")

        # Update and print summary
        total_processed += processed_in_batch
        total_found += found_in_batch
        
        print(f"Batch Summary: Processed {processed_in_batch}, Found {found_in_batch}.")
        print("---------------------------------------")
        
        batch_number += 1
        
    # --- Final Report ---
    print("\n" + "=" * 50)
    print("PROCESSING COMPLETE")
    print(f"TOTAL RECORDS PROCESSED: {total_processed}")
    print(f"TOTAL USERS OVER AGE {TARGET_AGE}: {total_found}")
    print("=" * 50)


if __name__ == "__main__":
    # Example usage: process the data in batches of 2000
    batch_processing(batch_size=2000)
