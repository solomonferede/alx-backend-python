"""
Objective:
    Set up a MySQL database (ALX_prodev) and populate it with data from user_data.csv.

Instructions:
    Write a Python script named seed.py that:
        • Creates the database ALX_prodev (if it does not exist)
        • Creates the table user_data (if it does not exist)
        • Populates it with data from user_data.csv

Prototypes:
    def connect_db() :- connects to the MySQL database server
    def create_database(connection):- creates the database ALX_prodev if it does not exist
    def connect_to_prodev():- connects to the ALX_prodev database in MySQL
    def create_table(connection):- creates a table user_data if it does not exist
    def insert_data(connection, data):- inserts data in the database if it does not exist
"""

import mysql.connector
from mysql.connector import Error
import csv
import uuid


# -------------------------
# Connect to MySQL server
# -------------------------
def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='solomon',
            password='solomon@2025'
        )
        if connection.is_connected():
            print("Connected to MySQL Server")
            return connection
    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None


# -------------------------
# Create database if not exists
# -------------------------
def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database 'ALX_prodev' verified/created successfully")
    except Error as e:
        print("Failed to create database:", e)


# -------------------------
# Connect to ALX_prodev database
# -------------------------
def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='solomon',
            password='solomon@2025',
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print("Error while connecting to ALX_prodev:", e)
        return None


# -------------------------
# Create user_data table
# -------------------------
def create_table(connection):
    """Creates the user_data table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX(email)
            );
        """)
        print("Table 'user_data' verified/created successfully")
    except Error as e:
        print("Failed to create table:", e)


# -------------------------
# Insert data from CSV file
# -------------------------
def insert_data(connection, filename):
    """Reads from a CSV file and inserts data into the user_data table if not already present."""
    try:
        cursor = connection.cursor()

        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row

            for row in reader:
                if len(row) != 3:
                    print(f"Skipping invalid row: {row}")
                    continue

                name, email, age = row

                # Check for duplicate email
                cursor.execute("SELECT 1 FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    print(f"Skipping duplicate entry for email: {email}")
                    continue

                # Insert new record
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), name, email, age))

        connection.commit()
        print("Data inserted successfully from CSV file")

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Error as e:
        print("Error inserting data:", e)