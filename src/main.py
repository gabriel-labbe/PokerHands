import hand_parser
import mysql.connector
from mysql.connector import Error
from config import pw
from populate_db import populate_db
from os import listdir
from os.path import isfile, join


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


if __name__ == "__main__":
    db = "pokerhand"
    connection = create_db_connection("localhost", "root", pw, db)

    zoom_data_path = "../data/zoom/"
    file_names = [zoom_data_path + f for f in listdir(zoom_data_path) if isfile(join(zoom_data_path, f))]

    for file_name in file_names:
        print("Processing file " + file_name)
        hands = hand_parser.extract_hands_from_zoom_file(file_name)
        for hand in hands:
            try:
                populate_db(connection, hand)
            except Exception as e:
                try:
                    print("Failed at hand " + hand_parser.hand_id(hand))
                    print(e)
                except:
                    print("Trouble with this hand: ")
                    print(hand)
