# Python Generators 0x00 - Database Seeding

This project provides a MySQL database seeding solution for the ALX_prodev database with user data.

## Files

- `seed.py` - Main seeding module with database functions
- `user_data.csv` - Sample user data for seeding
- `0-main.py` - Test script to verify functionality

## Requirements

- Python 3.x
- MySQL server running locally
- mysql-connector-python package

## Installation

1. Install MySQL server if not already installed:
   ```bash
   # On macOS
   brew install mysql
   brew services start mysql
   
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install mysql-server
   sudo systemctl start mysql
   ```

2. Install Python dependencies:
   ```bash
   pip install mysql-connector-python
   ```

## Database Schema

The script creates a database `ALX_prodev` with a table `user_data`:

```sql
CREATE TABLE user_data (
    user_id CHAR(36) PRIMARY KEY,    -- UUID format
    name VARCHAR(255) NOT NULL,      -- User full name
    email VARCHAR(255) NOT NULL,     -- User email address
    age DECIMAL(3,0) NOT NULL,       -- User age
    INDEX idx_user_id (user_id)      -- Index on user_id
);
```

## Functions

### `connect_db()`
Connects to the MySQL database server using common configuration attempts.

### `create_database(connection)`
Creates the ALX_prodev database if it doesn't exist.

### `connect_to_prodev()`
Connects specifically to the ALX_prodev database.

### `create_table(connection)`
Creates the user_data table with the required schema if it doesn't exist.

### `insert_data(connection, csv_file)`
Inserts data from a CSV file into the user_data table, avoiding duplicates.

## Usage

### Basic Usage

```python
import seed

# Connect to MySQL server
connection = seed.connect_db()
if connection:
    # Create database
    seed.create_database(connection)
    connection.close()
    
    # Connect to ALX_prodev database
    connection = seed.connect_to_prodev()
    if connection:
        # Create table
        seed.create_table(connection)
        
        # Insert data from CSV
        seed.insert_data(connection, 'user_data.csv')
        
        connection.close()
```

### Running the Test Script

```bash
chmod +x 0-main.py
./0-main.py
```

Expected output:
```
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
```

## CSV Format

The CSV file should have the following columns:
- `user_id`: UUID string (36 characters)
- `name`: Full name string
- `email`: Email address string
- `age`: Integer age value

Example:
```csv
user_id,name,email,age
00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
```

## Error Handling

The script includes robust error handling for:
- MySQL connection failures
- Database creation errors
- Table creation errors
- Data insertion errors
- Invalid UUID formats
- Missing CSV files

## MySQL Connection

The script attempts multiple common MySQL configurations:
- localhost with root user (no password)
- localhost with root user (password: root)
- localhost with mysql user (no password)
- 127.0.0.1 with root user (no password)
- 127.0.0.1 with root user (password: root)

Modify the connection parameters in the functions if your MySQL setup differs.

## Troubleshooting

1. **MySQL not running**: Ensure MySQL server is started
2. **Connection refused**: Check MySQL is listening on port 3306
3. **Access denied**: Verify MySQL user credentials
4. **Database exists**: The script safely handles existing databases and tables
5. **Import errors**: Ensure mysql-connector-python is installed in your environment
