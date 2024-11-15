import requests
import random
import time
from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

# Facebook Page Access Token
PAGE_ACCESS_TOKEN = 'EAAM9iMIKZCZCABOywMglUDokC9ZBQJPuiKWHM2HspbZCIYI7ZBSvyyrHDXdFZCTLhETCWO5rEWgimZCgK1vc2FZAsMvIdj1osFsYjILku5msicVHuWGkoCPWkxIx2tmc0limiaEDN1ivQzGpPqLGMUlho9BMKaptfNjKEt2VSVZAZCD913nbOvwsqxByV7LVAHZAXIZD'

# Correct answers list for flexibility in answer formats (case-sensitive)
CORRECT_ANSWERS = [
    "north star", "North star", "NORTH STAR", 
    "the north star", "The north star", "THE NORTH STAR", 
    "northstar", "Northstar", "NORTHSTAR", 
    "the northstar", "The northstar", "THE NORTHSTAR"
]

# Dictionary to store player data (attempts, last message timestamp, etc.)
players = {}

# Function to send a message to the player
def send_facebook_message(recipient_id, message_text):
    url = f'https://graph.facebook.com/v14.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")

# Handle webhook verification and incoming messages
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "bababooey":
            return challenge
        return "Verification failed", 403

    elif request.method == "POST":
        data = request.get_json()
        if data.get("object") == "page":
            for entry in data["entry"]:
                for message_event in entry.get("messaging", []):
                    sender_id = message_event["sender"]["id"]
                    if "message" in message_event:
                        handle_player_response(sender_id, message_event["message"].get("text", "").lower().strip())
        return "Event received", 200

# Handle player responses and track progress
def handle_player_response(player_id, player_answer):
    # Set the minimum typing delay in seconds (between 2 to 5 seconds)
    TYPING_DELAY = random.randint(2, 5)  # Randomized typing delay for realism

    # If the player is new, initialize their data
    if player_id not in players:
        players[player_id] = {
            "attempts": 0,
            "last_message_timestamp": datetime.now(),
            "has_received_riddle": False,  # Track whether they've received the initial riddle
            "has_solved_riddle": False,   # Track whether they've solved the riddle
            "current_level": 1            # Track the player's current level
        }

    # Simulate typing delay before responding
    print(f"Simulating typing... Waiting {TYPING_DELAY} seconds before sending message.")
    time.sleep(TYPING_DELAY)  # Simulate the delay of someone typing

    player_data = players[player_id]

    # If the player hasn't received the riddle yet, send it
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
        # Mark that the riddle has been sent
        player_data["has_received_riddle"] = True
        players[player_id] = player_data  # Update player data

    # Check if the player's answer is correct
    elif player_answer in CORRECT_ANSWERS and not player_data["has_solved_riddle"]:
        send_facebook_message(player_id, "Well done, Seeker! You've proven yourself worthy. Prepare for the next challenge.")
        
        # After solving, mark as solved and move to next level
        player_data["has_solved_riddle"] = True
        player_data["current_level"] = 2  # Player moves to level 2
        players[player_id] = player_data  # Update player data
        
        # Send cryptic message for the next level
        cryptic_message = (
            "As you have unlocked the first path, the next will test your mind. "
            "Beware the shadow that lurks beneath, where all things are reversed. "
            "Think not with your eyes, but with your heart. This is where the true journey begins."
        )
        send_facebook_message(player_id, cryptic_message)

    elif player_data["has_solved_riddle"]:
        # If the player has already solved the riddle and is messaging again
        awaiting_message = (
            "Patience, Seeker. The veil will lift only when the time is right. "
            "Await further revelation, for the truth shall emerge when least expected."
        )
        send_facebook_message(player_id, awaiting_message)

    else:
        # Increment the number of attempts for this player
        player_data["attempts"] += 1

        # Simulate typing delay before responding
        print(f"Simulating typing... Waiting {TYPING_DELAY} seconds before sending message.")
        time.sleep(TYPING_DELAY)  # Simulate the delay of someone typing

        # Provide hints based on the number of incorrect attempts
        if player_data["attempts"] == 2:
            send_facebook_message(player_id, "Hint 1: Look up when you're lost at night. Sometimes the answer is above you.")
        elif player_data["attempts"] == 5:
            send_facebook_message(player_id, "Hint 2: This guide remains fixed in the northern sky, constant and bright.")

        # If the player hasn't guessed correctly, let them know to try again
        else:
            send_facebook_message(player_id, "That answer isn’t quite right. Try again, Seeker.")

        players[player_id] = player_data  # Update player data

if __name__ == "__main__":
    app.run(port=5000)
