from init_db import create_db_connection, execute_query
import config


if __name__ == "__main__":
    connection = create_db_connection("localhost", "root", config.PW, config.DB_NAME)

    drop_tables = [
        "DROP TABLE cards;",
        "DROP TABLE post;",
        "DROP TABLE action;",
        "DROP TABLE participant;",
        "DROP TABLE hand;"
    ]

    for sql in drop_tables:
        execute_query(connection, sql)

