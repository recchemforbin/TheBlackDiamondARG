# player_state.py

import json
from datetime import datetime
from config import PLAYER_DATA_FILE

# Load player data from JSON
def load_player_data():
    try:
        with open(PLAYER_DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save player data to JSON
def save_player_data(players):
    with open(PLAYER_DATA_FILE, 'w') as file:
        json.dump(players, file, indent=4)

# Initialize or update a player's data
def get_or_create_player(player_id):
    players = load_player_data()
    if player_id not in players:
        players[player_id] = {
            "attempts": 0,
            "last_message_timestamp": datetime.now().isoformat(),
            "has_received_riddle": False,
            "has_solved_riddle": False,
            "current_level": 1
        }
    return players[player_id], players

# Update and save a specific player's data
def update_player_data(player_id, player_data):
    players = load_player_data()
    players[player_id] = player_data
    save_player_data(players)
