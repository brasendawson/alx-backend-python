#!/usr/bin/env python3
"""
Database seeding module for ALX_prodev MySQL database.
This module provides functions to connect to MySQL, create database and table,
and insert sample data from CSV file.
"""

import mysql.connector
from mysql.connector import Error
import csv
import os
import uuid


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        mysql.connector.connection: Database connection object or None if failed
    """
    # Try different common MySQL configurations
    configs = [
        {'host': 'localhost', 'user': 'root', 'password': ''},
        {'host': 'localhost', 'user': 'root', 'password': 'root'},
        {'host': 'localhost', 'user': 'mysql', 'password': ''},
        {'host': '127.0.0.1', 'user': 'root', 'password': ''},
        {'host': '127.0.0.1', 'user': 'root', 'password': 'root'}
    ]
    
    for config in configs:
        try:
            connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                autocommit=True
            )
            
            if connection.is_connected():
                print(f"Connected to MySQL server successfully with user: {config['user']}")
                return connection
                
        except Error as e:
            continue  # Try next configuration
    
    print("Error: Could not connect to MySQL server with any configuration")
    print("Please ensure MySQL is running and check your credentials")
    print("Common solutions:")
    print("1. Install MySQL: brew install mysql (on macOS)")
    print("2. Start MySQL service: brew services start mysql")
    print("3. Set MySQL root password if needed")
    return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully or already exists")
        cursor.close()
        
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        mysql.connector.connection: Database connection object or None if failed
    """
    # Try different common MySQL configurations
    configs = [
        {'host': 'localhost', 'user': 'root', 'password': ''},
        {'host': 'localhost', 'user': 'root', 'password': 'root'},
        {'host': 'localhost', 'user': 'mysql', 'password': ''},
        {'host': '127.0.0.1', 'user': 'root', 'password': ''},
        {'host': '127.0.0.1', 'user': 'root', 'password': 'root'}
    ]
    
    for config in configs:
        try:
            connection = mysql.connector.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                database='ALX_prodev',
                autocommit=True
            )
            
            if connection.is_connected():
                print(f"Connected to ALX_prodev database successfully with user: {config['user']}")
                return connection
                
        except Error as e:
            continue  # Try next configuration
    
    print("Error: Could not connect to ALX_prodev database with any configuration")
    print("Please ensure MySQL is running and the ALX_prodev database exists")
    return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
    """
    try:
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        
        cursor.execute(create_table_query)
        print("Table user_data created successfully")
        cursor.close()
        
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist.
    
    Args:
        connection: MySQL connection object to ALX_prodev database
        csv_file: Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Data already exists in user_data table ({count} rows)")
            cursor.close()
            return
        
        # Read CSV file and insert data
        if not os.path.exists(csv_file):
            print(f"CSV file {csv_file} not found")
            cursor.close()
            return
            
        insert_query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        
        rows_inserted = 0
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Validate UUID format
                try:
                    uuid.UUID(row['user_id'])
                except ValueError:
                    print(f"Invalid UUID format: {row['user_id']}, skipping row")
                    continue
                
                # Insert the row
                cursor.execute(insert_query, (
                    row['user_id'],
                    row['name'],
                    row['email'],
                    int(row['age'])
                ))
                rows_inserted += 1
        
        print(f"Successfully inserted {rows_inserted} rows into user_data table")
        cursor.close()
        
    except Error as e:
        print(f"Error inserting data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Test the functions
    print("Testing database setup...")
    
    # Connect to MySQL server
    conn = connect_db()
    if conn:
        # Create database
        create_database(conn)
        conn.close()
        
        # Connect to ALX_prodev database
        prodev_conn = connect_to_prodev()
        if prodev_conn:
            # Create table
            create_table(prodev_conn)
            
            # Insert data
            insert_data(prodev_conn, 'user_data.csv')
            
            # Show some sample data
            cursor = prodev_conn.cursor()
            cursor.execute("SELECT * FROM user_data LIMIT 5")
            rows = cursor.fetchall()
            print("\nSample data from user_data table:")
            for row in rows:
                print(row)
            
            cursor.close()
            prodev_conn.close()
