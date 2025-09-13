#!/usr/bin/env python3
"""
Memory-efficient aggregation module for calculating average user age.
This module uses generators to compute aggregates without loading all data into memory.
"""

import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.
    
    Yields:
        int: User age values
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
        
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Use a single loop to yield ages one by one
        for row in cursor:
            yield int(row[0])
            
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error streaming user ages: {e}")
        return


def calculate_average_age():
    """
    Calculate the average age using the age generator.
    This function processes ages one by one without loading all data into memory.
    
    Returns:
        float: Average age of all users
    """
    total_age = 0
    count = 0
    
    # Use a single loop to accumulate sum and count
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0.0
    
    return total_age / count


if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")