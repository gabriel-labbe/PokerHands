from hand_parser import player_names, starting_stacks, actions, get_collectors, uncalled_bet, get_posts
import pandas as pd


def calculate_ending_stacks(hand_history: str) -> list[float]:
    names = player_names(hand_history)
    stacks = starting_stacks(hand_history)
    status_df = pd.DataFrame({"name": names, "stack": stacks, "to_call": [0.0] * len(names)})

    status_df = subtract_posts_from_stacks(hand_history, status_df)
    status_df = subtract_actions_from_stacks(hand_history, status_df)
    status_df = add_uncalled_bets_to_stacks(hand_history, status_df)
    status_df = add_chips_to_winners(hand_history, status_df)
    status_df = status_df.round({"stack": 2})

    return status_df["stack"].to_list()


def subtract_posts_from_stacks(hand_history: str, status: pd.DataFrame) -> pd.DataFrame:
    for name, _, amount in get_posts(hand_history):
        status.loc[status['name'] == name, "stack"] -= amount
        to_call = amount - float(status.loc[status['name'] == name, "to_call"].item())
        if to_call > 0:
            status.loc[status['name'] == name, "to_call"] = 0.0
            status.loc[status['name'] != name, "to_call"] += to_call
    return status


def subtract_actions_from_stacks(hand_history: str, status: pd.DataFrame) -> pd.DataFrame:
    for name, action_type, amount in actions(hand_history):
        if action_type == 'C':
            status.loc[status['name'] == name, "to_call"] = 0.0
            status.loc[status['name'] == name, "stack"] -= amount
        elif action_type == 'B':
            status.loc[status['name'] != name, "to_call"] = amount
            status.loc[status['name'] == name, "stack"] -= amount
        elif action_type == 'R':
            status.loc[status['name'] != name, "to_call"] += amount
            bet_amount = (amount + status.loc[status['name'] == name, "to_call"])
            status.loc[status['name'] == name, "stack"] -= bet_amount
            status.loc[status['name'] == name, "to_call"] = 0.0
    return status


def add_uncalled_bets_to_stacks(hand_history: str, status: pd.DataFrame) -> pd.DataFrame:
    try:
        name, amount = uncalled_bet(hand_history)
        status.loc[status['name'] == name, "stack"] += amount
    except:
        # No uncalled bet, do nothing
        pass
    finally:
        return status


def add_chips_to_winners(hand_history: str, status: pd.DataFrame) -> pd.DataFrame:
    collectors = get_collectors(hand_history)
    for name, amount in collectors:
        status.loc[status['name'] == name, "stack"] += amount
    return status
