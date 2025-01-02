import psycopg2
from psycopg2 import sql
import datetime
from app.settings import Config

def use_db(query, data=None, fetch=False):
    """A generic function to run a query and optionally return data.
    
    Args:
        query (str): The SQL query to execute.
        data (tuple, optional): The data to insert or query (default is None).
        fetch (bool, optional): If True, the function will return query results (default is False).
    
    Returns:
        list: If fetch=True, returns the query results.
        None: If fetch=False, performs the operation and commits.
    """
    connection = None
    cursor = None
    result = None

    try:
        # Connect to the database
        connection = psycopg2.connect(
            host=Config.DB_HOST,
            user=Config.POSTGRES_USER,
            password=Config.POSTGRES_PASSWORD,
            port=Config.DB_PORT,
            database=Config.POSTGRES_DB
        )
        cursor = connection.cursor()

        # Execute the query with data if provided
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)

        # If fetch is True, return the result
        if fetch:
            result = cursor.fetchall()
        else:
            # Commit the transaction for insert/update/delete queries
            connection.commit()

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return result

def list_table():
    connection = psycopg2.connect(
        host=Config.DB_HOST,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD,
        port=Config.DB_PORT,
        database=Config.POSTGRES_DB
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # SQL query to list all tables
    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    tables = cursor.fetchall()

    # Print the table names
    print("Tables in the database:")
    for table in tables:
        print(table[0])

    # Close the cursor and connection
    cursor.close()
    connection.close()