import sqlite3
from sqlite3 import Error

"""
Script to create a connection to the database and perform SQL operations
"""


def create_connection(db_path):
    """
    Create a database connection to the SQLite database specified by db_path.
    :param db_path: database file path
    :return: Connection object or None
    """
    conn = None
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect(db_path, check_same_thread=False)
        # Set row factory to sqlite3.Row for named column access
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        # Print any connection errors
        print(e)
    return conn


def sql_select_query(conn, query, var):
    """
    Execute a SELECT query and fetch the results.
    :param conn: Connection object
    :param query: SELECT query
    :param var: tuple of variables for the query
    :return: list of rows
    """
    cur = conn.cursor()
    # Execute the SELECT query
    cur.execute(query, var)
    # Fetch all the results of the query
    rows = cur.fetchall()
    return rows


def sql_insert_query(conn, query, var):
    """
    Execute an INSERT query.
    :param conn: Connection object
    :param query: INSERT query
    :param var: tuple of variables for the query
    """
    cur = conn.cursor()
    # Execute the INSERT query
    cur.execute(query, var)
    # Commit the transaction
    conn.commit()
