#!/usr/bin/env python3
"""
Generator module for streaming user data from MySQL database.
This module provides a generator function to fetch rows one by one from the user_data table.
"""

import mysql.connector
from mysql.connector import Error
import csv
import os


def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    
    Yields:
        dict: Dictionary containing user data with keys: user_id, name, email, age
    """
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev',
            autocommit=True
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        
        # Use a single loop to yield rows one by one
        for row in rows:
            # Convert Decimal age to int for consistent output
            row['age'] = int(row['age'])
            yield row
            
    except Error as e:
        print(f"Error fetching data: {e}")
        return