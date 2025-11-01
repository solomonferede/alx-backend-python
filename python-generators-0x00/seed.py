#!/usr/bin/env python3
"""
Objective:
    Set up a MySQL database (ALX_prodev) and populate it with data from user_data.csv.

This script ensures the database and table exist and inserts data 
from a CSV file while preventing duplicate entries. It is designed to be 
imported and used as a module by another main file.
"""

import os
import csv
import uuid
from typing import Optional, Dict

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

# Database configuration using environment variables
# I use separate configs for server connection (no DB specified) and 
# application connection (DB specified) for clarity in the seeding process.
SERVER_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
}

DB_NAME = os.environ.get("DB_DATABASE", "ALX_prodev")

APP_CONFIG = {
    **SERVER_CONFIG, # Include host, user, and password
    "database": DB_NAME
}

# ----------------------------------------------------
# 1. Connect to MySQL server (WITHOUT specifying a database)
# ----------------------------------------------------
def connect_db():
    """
    Connects to the MySQL database server.

    Returns:
        A live connection object or None if connection fails.
    """
    try:
        # Establish connection. Note: The caller MUST close this connection.
        connection = mysql.connector.connect(**SERVER_CONFIG)
        if connection.is_connected():
            print("Connected to MySQL Server successfully.")
            return connection
    except Error as e:
        # This catches errors like bad credentials or server not running
        print(f"Error while connecting to MySQL Server: {e}")
        print("Please ensure your DB_HOST, DB_USER, and DB_PASSWORD are correct.")
    return None

# ----------------------------------------------------
# 2. Create database if not exists
# ----------------------------------------------------
def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
            print(f"Database '{DB_NAME}' verified/created successfully.")
    except Error as e:
        print(f"Failed to create database: {e}")

# ----------------------------------------------------
# 3. Connect to the ALX_prodev database
# ----------------------------------------------------
def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(**APP_CONFIG)
        if connection.is_connected():
            print(f"Connected to '{DB_NAME}' database.")
            return connection
    except Error as e:
        print(f"Error while connecting to {DB_NAME}: {e}")
    return None

# ----------------------------------------------------
# 4. Create user_data table
# ----------------------------------------------------
def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        # Use context manager for cursor
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_data (
                    user_id CHAR(36) PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    age DECIMAL NOT NULL,                  
                    INDEX(email)
                );
            """)
        print("Table 'user_data' verified/created successfully.")
    except Error as e:
        print(f"Failed to create table: {e}")

# ----------------------------------------------------
# 5. Insert data from CSV file
# ----------------------------------------------------
def insert_data(connection, data):
    """Reads from a CSV file and inserts data into the user_data table."""
    insert_sql = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s);
    """
    
    try:
        with connection.cursor() as cursor:
            with open(data, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                
                records_inserted = 0
                records_skipped = 0
                
                for row in reader:
                    if len(row) != 3:
                        print(f"Warning: Skipping invalid row (wrong column count): {row}")
                        records_skipped += 1
                        continue

                    name, email, age = row
                    
                    try:
                        # Attempt to insert new record
                        cursor.execute(insert_sql, (str(uuid.uuid4()), name, email, age))
                        records_inserted += 1
                    except mysql.connector.IntegrityError as e:
                        if e.errno == 1062: # MySQL error code for duplicate entry for key 'PRIMARY' or 'UNIQUE'
                            records_skipped += 1
                            pass # Silently skip duplicate entries
                        else:
                            raise e # Reraise other integrity errors
                    except ValueError:
                        print(f"Warning: Skipping row with invalid age: {row}")
                        records_skipped += 1
                        continue
                        
            connection.commit()
            print(f"Data insertion complete: {records_inserted} records inserted, {records_skipped} records skipped (duplicates/errors).")

    except FileNotFoundError:
        print(f"Error: CSV file '{data}' not found. Please ensure it is in the same directory.")
    except Error as e:
        print(f"Error during data insertion: {e}")
