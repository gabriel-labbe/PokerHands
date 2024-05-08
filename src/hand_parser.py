import re

def get_number_of_players(hand_text):
    seats = re.findall("Seat", hand_text)
    return int((len(seats) - 1) / 2)

def get_button_seat(hand_text):
    text = re.search("Seat #\d is the button", hand_text)
    return text.group()[6]

def get_involved_players_name(hand_text):
    players_name = []
    pattern = r"FLOP[\s\S]*TURN"
    text = re.search(pattern, hand_text)
    relevant_lines = text.group().split('\n')[1:-1]
    for line in relevant_lines:
        players_name.append(line.split(':')[0])
    no_duplicate_names = list(dict.fromkeys(players_name))
    return no_duplicate_names

def get_player_seat(hand_text, player_name):
    text = re.search("Seat \d: " + player_name, hand_text)
    return text.group()[5]

def get_player_stack(hand_text, player_name):
    text = re.search(player_name + r".*in\schips\)", hand_text)
    chips = re.search(r"\d+", text.group())
    return chips.group()

def get_flop_cards(hand_text):
    pattern = r"\*\*\* FLOP \*\*\* \[.*\]"
    text = re.search(pattern, hand_text)
    return text.group()[14:-1].split(" ")

def get_blinds_level(hand_text):
    text = re.search(r"\(\d+/\d+\)", hand_text)
    small_blind = int(re.search(r"\d+/", text.group()).group()[:-1])
    big_blind = int(re.search(r"/\d+", text.group()).group()[1:])
    return small_blind, big_blind

def get_starting_pot(hand_text):
    additions = re.findall(r"posts.*\d+", hand_text)
    pot = 0
    for addition in additions:
        chips_to_add = re.search(r"\d+", addition)
        pot += int(chips_to_add.group())
    return pot


def get_stacks(hand_text):
    stacks = []
    seats = re.findall("\d+\sin\schips", hand_text)
    for seat in seats:
        chips = re.search(r"\d+", seat)
        stacks.append(int(chips.group()))

    # We reorder the stack list to get BB first, then SB, BU, CO, ...
    split_index = (int(get_button_seat(hand_text)) + 2) % len(stacks)

    stacks = stacks[split_index:] + stacks[:split_index]
    stacks.reverse()

    # Remove ante from stacks
    ante = get_ante(hand_text)
    stacks = [stack - ante for stack in stacks]

    # Remove blinds from stacks
    sb, bb = get_blinds_level(hand_text)
    stacks[0] = max(stacks[0] - bb, 0)
    stacks[1] = max(stacks[1] - sb, 0)

    return stacks


def get_ante(hand_text):
    text = re.search(r"ante\s\d+", hand_text)
    chips = re.search(r"\d+", text.group())
    return int(chips.group())
