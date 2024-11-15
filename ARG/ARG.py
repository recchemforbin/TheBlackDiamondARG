import vonage

# Replace with your API key and secret
API_KEY = '15582e33'
API_SECRET = '70EN9IbuwlTb8fOJ'

# Create a Vonage client
client = vonage.Client(key=API_KEY, secret=API_SECRET)

# Create an SMS client
sms = vonage.Sms(client)

# Send an SMS message
responseData = sms.send_message(
    {
        "from": "Nexmo",             # This can be a text identifier or phone number
        "to": "+18284432686",  # Replace with the player's phone number
        "text": "Welcome to the ARG! Here’s your first clue.",
    }
)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
