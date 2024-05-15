import mysql.connector
from mysql.connector import Error
import config


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
    connection = create_server_connection(config.HOST, config.USER, config.PW)
    create_database_query = "CREATE DATABASE " + config.DB_NAME
    create_database(connection, create_database_query)
    connection = create_db_connection(config.HOST, config.USER, config.PW, config.DB_NAME)

    create_hand_table = """
        CREATE TABLE hand (
            id CHAR(12) PRIMARY KEY,
            datetime DATETIME NOT NULL,
            button INT NOT NULL,
            small_blind FLOAT NOT NULL,
            big_blind FLOAT NOT NULL,
            ante FLOAT NOT NULL,
            flop_1 VARCHAR(2),
            flop_2 VARCHAR(2),
            flop_3 VARCHAR(2),
            turn VARCHAR(2),
            river VARCHAR(2),
            total_pot FLOAT NOT NULL,
            rake FLOAT NOT NULL,
            is_showdown BOOL NOT NULL
            );
        """

    create_participant_table = """
        CREATE TABLE participant (
            name VARCHAR(40),
            hand_id CHAR(12),
            starting_stack FLOAT NOT NULL,
            ending_stack FLOAT NOT NULL,
            PRIMARY KEY (name, hand_id)
            );        
        """

    create_action_table = """
        CREATE TABLE action (
            hand_id CHAR(12),
            action_number INT,
            street VARCHAR(7) NOT NULL,
            player_name VARCHAR(40) NOT NULL,
            type CHAR(1) NOT NULL,
            size FLOAT NOT NULL,
            PRIMARY KEY (hand_id, action_number)
            );
        """

    create_post_table = """
        CREATE TABLE post (
            post_number INT,
            hand_id CHAR(12),
            player_name VARCHAR(40) NOT NULL,
            type VARCHAR(4) NOT NULL,
            size FLOAT NOT NULL,
            PRIMARY KEY (hand_id, post_number)
            );
        """

    create_cards_table = """
        CREATE TABLE cards (
            hand_id CHAR(12),
            player_name VARCHAR(40),
            card_1 CHAR(2) NOT NULL,
            card_2 CHAR(2) NOT NULL,
            PRIMARY KEY (hand_id, player_name)
            );
        """

    alter_participant = """
        ALTER TABLE participant
        ADD FOREIGN KEY (hand_id)
        REFERENCES hand(id)
        ON DELETE CASCADE;
        """

    alter_action = """
        ALTER TABLE action
        ADD FOREIGN KEY (hand_id)
        REFERENCES hand(id)
        ON DELETE CASCADE;
        """

    alter_post = """
        ALTER TABLE post
        ADD FOREIGN KEY (hand_id)
        REFERENCES hand(id)
        ON DELETE CASCADE;
        """

    alter_cards = """
        ALTER TABLE cards
        ADD FOREIGN KEY (hand_id)
        REFERENCES hand(id)
        ON DELETE CASCADE;
        """

    execute_query(connection, create_hand_table)
    execute_query(connection, create_participant_table)
    execute_query(connection, create_post_table)
    execute_query(connection, create_action_table)
    execute_query(connection, create_cards_table)
    execute_query(connection, alter_participant)
    execute_query(connection, alter_post)
    execute_query(connection, alter_action)
    execute_query(connection, alter_cards)


