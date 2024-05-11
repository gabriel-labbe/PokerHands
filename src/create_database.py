import mysql.connector
from mysql.connector import Error
from config import pw


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


if __name__ == "__main__":
    connection = create_server_connection("localhost", "root", pw)

    create_database_query = "CREATE DATABASE pokerhand"
    create_database(connection, create_database_query)


