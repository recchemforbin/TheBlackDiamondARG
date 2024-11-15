# messenger_utils.py

import requests
from config import PAGE_ACCESS_TOKEN

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
