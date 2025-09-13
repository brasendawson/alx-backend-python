#!/usr/bin/env python3
"""
Lazy pagination module for streaming paginated user data.
This module provides lazy loading of user data pages using generators.
"""

import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Offset for pagination
        
    Returns:
        list: List of user dictionaries
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev',
            autocommit=True
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return rows
        
    except Error as e:
        print(f"Error fetching paginated data: {e}")
        return []


def lazy_paginate(page_size):
    """
    Generator function that lazily loads pages of user data.
    
    Args:
        page_size (int): Number of users per page
        
    Yields:
        list: List of user dictionaries for each page
    """
    offset = 0
    
    # Use a single loop to yield pages until no more data
    while True:
        page = paginate_users(page_size, offset)
        
        # If no more data, stop iteration
        if not page:
            break
            
        yield page
        offset += page_size