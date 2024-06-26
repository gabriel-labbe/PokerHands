import re


def extract_hands_from_zoom_file(file_name: str) -> list[str]:
    with open(file_name, encoding='utf8') as f:
        text = f.read()
        return re.split(r'\n{2,}', text)


def hand_id(hand_history: str) -> str:
    matches = re.findall(r'Hand #(\d+):', hand_history)
    if len(matches) == 1:
        return matches[0]
    else:
        raise Exception("Could not find hand id")


def get_datetime(hand_history: str) -> str:
    match = re.search(r'(\d{4}/\d{2}/\d{2} \d{1,2}:\d{2}:\d{2}) ET', hand_history)
    if match:
        return match.group(1).replace('/', '-')
    else:
        raise Exception("Could not find the datetime")


def button_seat(hand_history: str) -> int:
    matches = re.findall(r'Seat #(\d+) is the button', hand_history)
    if len(matches) == 1:
        return int(matches[0])
    else:
        raise Exception("Could not find button seat number")


def player_names(hand_history: str) -> list[str]:
    names = re.findall(r'Seat \d: (.+) \(.+ in chips\)', hand_history)
    if len(names) > 1:
        return names
    else:
        raise Exception("Could not find player names")


def ante_level(hand_history: str) -> float:
    matches = re.findall(r'posts the ante \$?([\d.]+)', hand_history)
    if len(matches) == 0:
        return 0.0
    ante_posted = list(map(float, matches))
    return max(ante_posted)


def blind_level(hand_history: str) -> tuple[float, float]:
    # Return format small_blind, big_blind
    first_line = hand_history.splitlines()[0]
    blinds = re.findall(r'\(\$(.+)/\$(.+)\)', first_line)
    if len(blinds) == 1:
        return float(blinds[0][0]), float(blinds[0][1])
    else:
        raise Exception("Could not find blind level")


def starting_stacks(hand_history: str) -> list[float]:
    stacks = re.findall(r'Seat \d+: .+ \(\$(.+) in chips\)', hand_history)
    if len(stacks) > 1:
        return [float(stack) for stack in stacks]
    else:
        raise Exception("Could not find player stacks")


def get_posts(hand_history: str) -> list[tuple[str, str, float]]:
    post_types = {'the ante': 'ante',
                  'small blind': 'sb',
                  'big blind': 'bb'}
    matches = re.findall(r'(.*): posts (small blind|big blind|the ante) \$?([\d.]+)', hand_history)
    posts = []
    if len(matches) > 0:
        for player_name, post_type, posted_amount in matches:
            posts.append((player_name, post_types[post_type], float(posted_amount)))
        return posts
    else:
        raise Exception("Could not find any posts")


def actions(hand_history: str) -> list[tuple[str, str, float, str]]:
    # The use of a letter for action types is standard in the poker community
    action_types = {'folds': 'F',
                    'checks': 'X',
                    'calls': 'C',
                    'bets': 'B',
                    'raises': 'R'}
    streets = ['preflop', 'flop', 'turn', 'river']
    current_street_index = 0
    change_of_street_indexes = _get_change_of_street_indexes(hand_history)
    matches = re.finditer(r'(.+): (folds|checks|calls|bets|raises) \$?([\d.]+)*', hand_history)
    formatted_actions = []
    for match in matches:
        player_name = match[1]
        action_type = action_types[match[2]]
        if match[3]:
            # Set the size to 0 for actions 'folds' and 'checks'
            action_size = float(match[3])
        else:
            action_size = 0.0
        if len(change_of_street_indexes) > 0:
            if match.start() > change_of_street_indexes[0]:
                current_street_index += 1
                change_of_street_indexes.pop(0)
        formatted_actions.append((player_name, action_type, action_size, streets[current_street_index]))
    return formatted_actions


def _flop_index(hand_history: str) -> int:
    match = re.search(r'\*\*\* FLOP \*\*\*', hand_history)
    if match:
        return match.start()
    else:
        return -1


def _turn_index(hand_history: str) -> int:
    match = re.search(r'\*\*\* TURN \*\*\*', hand_history)
    if match:
        return match.start()
    else:
        return -1


def _river_index(hand_history: str) -> int:
    match = re.search(r'\*\*\* RIVER \*\*\*', hand_history)
    if match:
        return match.start()
    else:
        return -1


def _get_change_of_street_indexes(hand_history: str) -> list[int]:
    indexes = []
    if _flop_index(hand_history) > 0:
        indexes.append(_flop_index(hand_history))
    if _turn_index(hand_history) > 0:
        indexes.append(_turn_index(hand_history))
    if _river_index(hand_history) > 0:
        indexes.append(_river_index(hand_history))
    return indexes


def flop_cards(hand_history: str) -> list[str] | list[None]:
    cards = re.findall(r'\*\*\* FLOP \*\*\* \[(.+)]', hand_history)
    # Ex value of 'cards': ['As Ac Ad'].
    if len(cards) == 1:
        return cards[0].split(' ')
    else:
        return [None, None, None]


def turn_card(hand_history: str) -> str | None:
    card = re.findall(r'\*\*\* TURN \*\*\* \[.+] \[(.{2})]', hand_history)
    if len(card) == 1:
        return card[0]
    else:
        return None


def river_card(hand_history: str) -> str | None:
    card = re.findall(r'\*\*\* RIVER \*\*\* \[.+] \[(.{2})]', hand_history)
    if len(card) == 1:
        return card[0]

    else:
        return None


def hero_name(hand_history: str) -> str:
    matches = re.findall(r'Dealt to (.+) \[.+]', hand_history)
    if len(matches) == 1:
        return matches[0]
    else:
        raise Exception("Could not find hero name")


def hero_cards(hand_history: str) -> list[str]:
    matches = re.findall(r'Dealt to .+ \[(.+)]', hand_history)
    if len(matches) == 1:
        return matches[0].split(' ')
    else:
        raise Exception("Could not find hero cards")


def get_showdown(hand_history: str) -> list[tuple[str, str, str]]:
    # Return format: [(player_name, card_1, card_2), ...]
    showdown = []
    matches = re.findall(r'(.+): shows \[(.+)]', hand_history)
    if len(matches) > 0:
        for match in matches:
            card_1, card_2 = match[1].split(' ')
            showdown.append((match[0], card_1, card_2))
    return showdown


def total_pot(hand_history: str) -> float:
    matches = re.findall(r'Total pot \$?([\d.]+)', hand_history)
    if len(matches) == 1:
        return float(matches[0])
    else:
        raise Exception("Could not find total pot")


def rake(hand_history: str) -> float:
    matches = re.findall(r'Rake \$?([\d.]+)', hand_history)
    if len(matches) == 1:
        return float(matches[0])
    else:
        raise Exception("Could not find rake")


def get_collectors(hand_history: str) -> list[tuple[str, float]]:
    # Return format: [(player_name, amount_won), ...]
    matches = re.findall(r'(.+) collected \$?([\d.]+)', hand_history)
    collectors = []
    if len(matches) > 0:
        for match in matches:
            collectors.append((match[0], float(match[1])))
    return collectors


def get_cash_outs(hand_history: str) -> list[tuple[str, float]]:
    # Return format: [(player_name, amount_won), ...]
    matches = re.findall(r'(.+) cashed out the hand for \$?([\d.]+)', hand_history)
    cash_outs = []
    if len(matches) > 0:
        for match in matches:
            cash_outs.append((match[0], float(match[1])))
        return cash_outs
    return cash_outs


def uncalled_bet(hand_history: str) -> tuple[str, float]:
    # Return format: player_name, amount_returned
    matches = re.findall(r'Uncalled bet \(\$([\d.]+)\) returned to (.*)', hand_history)
    if len(matches) == 1:
        return matches[0][1], float(matches[0][0])
    else:
        raise Exception("No uncalled bet were found")


def get_seat_number(hand_history: str) -> dict[str, int]:
    matches = re.findall(r'Seat (\d): (.+) \(\$?[\d.]+ in chips\)', hand_history)
    dico = {}
    for match in matches:
        dico[match[1]] = int(match[0])
    return dico
