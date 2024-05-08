import re
import datetime


def extract_hands_from_zoom_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        text = f.read()
        return text.split("\n\n\n\n")


def hand_id(hand_text: str) -> str:
    matches = re.findall(r'Hand #(\d+):', hand_text)
    if len(matches) == 1:
        return matches[0]
    else:
        raise Exception("Could not find hand id")


def get_datetime(hand_text: str) -> datetime:
    match = re.search(r'(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2}) ET', hand_text)
    if match:
        return datetime.datetime(match.group(0), match.group(1), match.group(2), match.group(3), match.group(4),
                                 match.group(5))
    else:
        raise Exception("Could not find the datetime")


def button_seat(hand_text: str) -> int:
    matches = re.findall(r'Seat #(\d+) is the button', hand_text)
    if len(matches) == 1:
        return int(matches[0])
    else:
        raise Exception("Could not find button seat number")


def player_names(hand_text: str) -> list[str]:
    names = re.findall(r'Seat \d: (.+) \(.+ in chips\)', hand_text)
    if len(names) > 1:
        return names
    else:
        raise Exception("Could not find player names")


def blind_level(hand_text: str) -> tuple[float, float]:
    # Return format small_blind, big_blind
    first_line = hand_text.splitlines()[0]
    blinds = re.findall(r'\(\$(.+)/\$(.+)\)', first_line)
    if len(blinds) == 1:
        return float(blinds[0][0]), float(blinds[0][1])
    else:
        raise Exception("Could not find blind level")


def player_stacks(hand_text: str) -> list[float]:
    stacks = re.findall(r'Seat \d+: .+ \(\$(.+) in chips\)', hand_text)
    if len(stacks) > 1:
        return [float(stack) for stack in stacks]
    else:
        raise Exception("Could not find player stacks")


def actions(hand_text: str) -> list[tuple[str, str, float]]:
    # Return format is [(player_name, action_type, action_size), ...]'
    # The use of a letter for action types is standard in the poker community
    action_types = {'folds': 'F',
                    'checks': 'X',
                    'calls': 'C',
                    'bets': 'B',
                    'raises': 'R'}
    matches = re.findall(r'(.+): (folds|checks|calls|bets|raises) \$?([\d.]+)*', hand_text)
    if len(matches) > 0:
        formatted_actions = []
        for match in matches:
            player_name = match[0]
            action_type = action_types[match[1]]
            if match[2] == '':
                # Set the size to 0 for actions 'folds' and 'checks'
                size = 0
            else:
                size = float(match[2])
            formatted_actions.append((player_name, action_type, size))
        return formatted_actions
    else:
        raise Exception("Could not find actions")


def flop_cards(hand_text: str) -> list[str]:
    cards = re.findall(r'\*\*\* FLOP \*\*\* \[(.+)]', hand_text)
    # Ex value of 'cards': ['As Ac Ad']. ***Note: No need to verify card value as PokerStars hand history is trustworthy.
    if len(cards) == 1:
        return cards[0].split(' ')
    else:
        return []


def turn_card(hand_text: str) -> str:
    card = re.findall(r'\*\*\* TURN \*\*\* \[.+] \[(.{2})]', hand_text)
    if len(card) == 1:
        return card[0]
    else:
        return ''


def river_card(hand_text: str) -> str:
    card = re.findall(r'\*\*\* RIVER \*\*\* \[.+] \[(.{2})]', hand_text)
    if len(card) == 1:
        return card[0]

    else:
        return ''


def hero_name(hand_text: str) -> str:
    matches = re.findall(r'Dealt to (.+) \[.+]', hand_text)
    if len(matches) == 1:
        return matches[0]
    else:
        raise Exception("Could not find hero name")


def hero_cards(hand_text: str) -> list[str]:
    matches = re.findall(r'Dealt to .+ \[(.+)]', hand_text)
    if len(matches) == 1:
        return matches[0].split(' ')
    else:
        raise Exception("Could not find hero cards")


def get_showdown(hand_text: str) -> list[tuple[str, list[str]]]:
    # Return format: [(player_name, [As, Ac]), ...]
    showdown = []
    matches = re.findall(r'(.+): shows \[(.+)]', hand_text)
    if len(matches) > 0:
        for match in matches:
            cards = match[1].split(' ')
            showdown.append((match[0], cards))
    return showdown


def total_pot(hand_text: str) -> float:
    matches = re.findall(r'Total pot \$?([\d.]+)', hand_text)
    if len(matches) == 1:
        return float(matches[0])
    else:
        raise Exception("Could not find total pot")


def rake(hand_text: str) -> float:
    matches = re.findall(r'Rake \$?([\d.]+)', hand_text)
    if len(matches) == 1:
        return float(matches[0])
    else:
        raise Exception("Could not find rake")


def get_collectors(hand_text: str) -> list[tuple[str, float]]:
    # Return format: [(player_name, amount_won), ...]
    matches = re.findall(r'(.+) collected \$?([\d.]+)', hand_text)
    if len(matches) > 0:
        collectors = []
        for match in matches:
            collectors.append((match[0], match[1]))
        return collectors
    else:
        raise Exception("Could not find collectors")

