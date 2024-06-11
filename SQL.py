import sqlite3
from sqlite3 import Error

# Functions to create database connections and perform SQL operations


def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file.
    :param db_file: database file path
    :return: Connection object or None
    """
    conn = None
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        # Print any connection errors
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """
    Create a table from the create_table_sql statement.
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        # Execute the CREATE TABLE statement
        c.execute(create_table_sql)
    except Error as e:
        # Print any table creation errors
        print(e)


def create_object(path):
    """
    Create a cursor object for the database connection.
    :param path: database file path
    :return: Cursor object
    """
    conn = create_connection(path)
    # Create and return a cursor object
    c = conn.cursor()
    return c


def main():
    """
    Main function to create the database and tables,
    and print the contents of the tables.
    """
    # SQL statements for creating users and transactions tables
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        uname text NOT NULL,
        password text NOT NULL,
        balance double precision NOT NULL DEFAULT 0
    );
    """
    sql_create_transactions_table = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id integer NOT NULL,
        reason text NOT NULL,
        type text NOT NULL,
        amount double precision NOT NULL,
        timestamp timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """

    # Create a database connection
    conn = create_connection("app_database.db")

    if conn is not None:
        # Create tables
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_transactions_table)
    else:
        print("Error! Cannot create database connection")

    # Uncomment the following lines to insert a sample user
    # conn.execute("INSERT INTO users (uname, password) VALUES ('jun', 'jun')")
    # conn.commit()

    # Print all users
    print("Users")
    users = conn.execute("SELECT * FROM users")
    for row in users:
        print(row)

    # Print all transactions
    print("Transactions")
    transactions = conn.execute("SELECT * FROM transactions")
    for row in transactions:
        print(row)

    # Close the connection
    conn.close()


if __name__ == '__main__':
    main()
