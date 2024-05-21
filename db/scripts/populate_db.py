from os import listdir
from os.path import isfile, join
import mysql.connector
from mysql.connector import Error

import db.hand_parser as parser
from init_db import create_db_connection
import config
from db.stacks_calculator import calculate_ending_stacks


def execute_query(connection: mysql.connector.MySQLConnection, query: str, val: tuple):
    cursor = connection.cursor()
    try:
        cursor.execute(query, val)
        connection.commit()
    except Error as err:
        print(err)


def populate_db(connection: mysql.connector.MySQLConnection, hand_history: str) -> None:
    insert_hand(connection, hand_history)
    insert_participants(connection, hand_history)
    insert_actions(connection, hand_history)
    insert_posts(connection, hand_history)
    insert_cards(connection, hand_history)


def insert_hand(connection: mysql.connector.MySQLConnection, hand_history: str) -> None:
    hand_id = parser.hand_id(hand_history)
    date_time = parser.get_datetime(hand_history)
    button = parser.button_seat(hand_history)
    small_blind, big_blind = parser.blind_level(hand_history)
    ante = 0
    flop_1, flop_2, flop_3 = parser.flop_cards(hand_history)
    turn = parser.turn_card(hand_history)
    river = parser.river_card(hand_history)
    total_pot = parser.total_pot(hand_history)
    rake = parser.rake(hand_history)
    is_showdown = len(parser.get_showdown(hand_history)) > 0
    sql_hand = '''
                INSERT INTO hand VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                '''
    val_hand = (hand_id, date_time, button, small_blind, big_blind, ante, flop_1, flop_2, flop_3, turn, river,
                total_pot, rake, is_showdown)

    execute_query(connection, sql_hand, val_hand)


def insert_participants(connection: mysql.connector.MySQLConnection, hand_history: str) -> None:
    hand_id = parser.hand_id(hand_history)
    player_names = parser.player_names(hand_history)
    starting_stacks = parser.starting_stacks(hand_history)
    ending_stacks = calculate_ending_stacks(hand_history)

    sql_participant = """
                    INSERT INTO participant VALUES
                    (%s, %s, %s, %s);
                """

    for i in range(len(player_names)):
        execute_query(connection, sql_participant, (player_names[i], hand_id, starting_stacks[i], ending_stacks[i]))


def insert_actions(connection: mysql.connector.MySQLConnection, hand_history: str) -> None:
    hand_id = parser.hand_id(hand_history)
    actions = parser.actions(hand_history)
    sql_action = """
                    INSERT INTO action VALUES
                    (%s, %s, %s, %s, %s, %s);
                """
    action_number = 0
    for player_name, action_type, action_size, street in actions:
        execute_query(connection, sql_action, (hand_id, action_number, street, player_name, action_type, action_size))
        action_number += 1


def insert_posts(connection: mysql.connector.MySQLConnection, hand_history: str) -> None:
    hand_id = parser.hand_id(hand_history)
    posts = parser.get_posts(hand_history)
    sql_post = """
                    INSERT INTO post VALUES
                    (%s, %s, %s, %s, %s);
                """
    post_number = 0
    for player_name, post_type, post_size in posts:
        execute_query(connection, sql_post, (post_number, hand_id, player_name, post_type, post_size))
        post_number += 1


def insert_cards(connection: mysql.connector.MySQLConnection, hand_history: str) -> None:
    hand_id = parser.hand_id(hand_history)
    hero_name = parser.hero_name(hand_history)
    hero_card_1, hero_card_2 = parser.hero_cards(hand_history)
    sql_cards = """
                    INSERT INTO cards VALUES
                    (%s, %s, %s, %s);
                """
    execute_query(connection, sql_cards, (hand_id, hero_name, hero_card_1, hero_card_2))

    showdown = parser.get_showdown(hand_history)
    for player_name, card_1, card_2 in showdown:
        execute_query(connection, sql_cards, (hand_id, player_name, card_1, card_2))


if __name__ == "__main__":
    connection = create_db_connection(config.HOST, config.USER, config.PW, config.DB_NAME)

    zoom_data_path = "../data/cash/"
    file_names = [zoom_data_path + f for f in listdir(zoom_data_path) if isfile(join(zoom_data_path, f))]

    for file_name in file_names:
        print("Processing file " + file_name)
        hands = parser.extract_hands_from_zoom_file(file_name)
        for hand in hands:
            try:
                populate_db(connection, hand)
            except Exception as e:
                try:
                    print("Failed at hand " + parser.hand_id(hand))
                    print(e)
                except:
                    print("Trouble with this hand: ")
                    print(hand)
