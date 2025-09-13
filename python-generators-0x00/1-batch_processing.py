#!/usr/bin/env python3
"""
Batch processing module for streaming user data in batches.
This module provides functions to fetch and process user data in batches.
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that streams users in batches from the user_data table.
    
    Args:
        batch_size (int): Number of users to include in each batch
        
    Yields:
        list: List of user dictionaries, each containing user data
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
        
        batch = []
        # Use a single loop to process rows and create batches
        for row in cursor:
            # Convert Decimal age to int for consistent output
            row['age'] = int(row['age'])
            batch.append(row)
            
            # When batch is full, yield it and start a new batch
            if len(batch) == batch_size:
                yield batch
                batch = []
        
        # Yield any remaining users in the last batch
        if batch:
            yield batch
            
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error fetching data: {e}")
        return


def batch_processing(batch_size):
    """
    Processes batches of users and yields only those over age 25.
    
    Args:
        batch_size (int): Size of batches to process
        
    Yields:
        dict: Individual user dictionaries for users over age 25
    """
    # Process each batch from the batch generator
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25 and yield them individually
        for user in batch:
            if user['age'] > 25:
                yield user