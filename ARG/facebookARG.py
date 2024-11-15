import requests

# Your Facebook Page Access Token
PAGE_ACCESS_TOKEN = 'EAAM9iMIKZCZCABOywMglUDokC9ZBQJPuiKWHM2HspbZCIYI7ZBSvyyrHDXdFZCTLhETCWO5rEWgimZCgK1vc2FZAsMvIdj1osFsYjILku5msicVHuWGkoCPWkxIx2tmc0limiaEDN1ivQzGpPqLGMUlho9BMKaptfNjKEt2VSVZAZCD913nbOvwsqxByV7LVAHZAXIZD'

# The function to send a message
def send_facebook_message(recipient_id, message_text):
    url = f'https://graph.facebook.com/v14.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Test by sending a message (replace recipient_id with the player's Facebook ID)
recipient_id = "player_facebook_id"  # Replace with the actual recipient ID
send_facebook_message(recipient_id, "Welcome to the ARG! Here’s your first clue.")
