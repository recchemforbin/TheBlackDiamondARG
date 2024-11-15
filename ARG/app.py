# app.py

from flask import Flask, request
from riddle_logic import handle_player_response
from config import VERIFY_TOKEN

app = Flask(__name__)

# Webhook verification and incoming message handling
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN:
            return challenge
        return "Verification failed", 403

    elif request.method == "POST":
        data = request.get_json()
        if data.get("object") == "page":
            for entry in data["entry"]:
                for message_event in entry.get("messaging", []):
                    sender_id = message_event["sender"]["id"]
                    if "message" in message_event:
                        player_answer = message_event["message"].get("text", "").lower().strip()
                        handle_player_response(sender_id, player_answer)
        return "Event received", 200

if __name__ == "__main__":
    app.run(port=5000)
