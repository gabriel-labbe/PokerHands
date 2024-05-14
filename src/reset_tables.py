import mysql.connector
from mysql.connector import Error
from config import pw


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Request query: " + query)
        print("Query executed successfully")
    except Error as err:
        print(f"Error: '{err}'")


if __name__ == "__main__":
    db = "pokerhand"
    connection = create_db_connection("localhost", "root", pw, db)

    drop_tables = """
    DROP TABLE cards;
    DROP TABLE post;
    DROP TABLE action;
    DROP TABLE participant;
    DROP TABLE hand;
    """

    execute_query(connection, drop_tables)

