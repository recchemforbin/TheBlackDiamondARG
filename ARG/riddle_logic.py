# riddle_logic.py

import random
import time
from datetime import datetime
from messenger_utils import send_facebook_message
from player_state import get_or_create_player, update_player_data

# Riddle answers
CORRECT_ANSWERS = ["north star", "North star", "NORTH STAR", 
                   "the north star", "The north star", "THE NORTH STAR", 
                   "northstar", "Northstar", "NORTHSTAR", 
                   "the northstar", "The northstar", "THE NORTHSTAR"]

# Process player's response to the riddle
def handle_player_response(player_id, player_answer):
    TYPING_DELAY = random.randint(2, 5)
    print(f"Simulating typing... Waiting {TYPING_DELAY} seconds.")
    time.sleep(TYPING_DELAY)

    player_data, players = get_or_create_player(player_id)

    # Send initial riddle if the player has not received it
    if not player_data["has_received_riddle"]:
        initial_message = (
            "Welcome, Seeker. We are the Order of the Celestial Veil.\n\n"
            "'I am not what I seem; yet I guide you true. "
            "A friend to the lost, in both darkness and blue. "
            "Follow my lead, though I drift and I sway, "
            "And I’ll show you the path, come night or come day. "
            "What am I?'"
        )
        send_facebook_message(player_id, initial_message)
        player_data["has_received_riddle"] = True

    # Check if the answer is correct
    elif player_answer in CORRECT_ANSWERS and not player_data["has_solved_riddle"]:
        send_facebook_message(player_id, "Well done, Seeker! You've proven yourself worthy. Prepare for the next challenge.")
        player_data["has_solved_riddle"] = True
        player_data["current_level"] = 2
        cryptic_message = (
            "As you have unlocked the first path, the next will test your mind. "
            "Beware the shadow that lurks beneath, where all things are reversed. "
            "Think not with your eyes, but with your heart. This is where the true journey begins."
        )
        send_facebook_message(player_id, cryptic_message)

    elif player_data["has_solved_riddle"]:
        awaiting_message = (
            "Patience, Seeker. The veil will lift only when the time is right. "
            "Await further revelation, for the truth shall emerge when least expected."
        )
        send_facebook_message(player_id, awaiting_message)

    else:
        player_data["attempts"] += 1
        if player_data["attempts"] == 2:
            send_facebook_message(player_id, "Hint 1: Look up when you're lost at night. Sometimes the answer is above you.")
        elif player_data["attempts"] == 5:
            send_facebook_message(player_id, "Hint 2: This guide remains fixed in the northern sky, constant and bright.")
        else:
            send_facebook_message(player_id, "That answer isn’t quite right. Try again, Seeker.")

    update_player_data(player_id, player_data)
