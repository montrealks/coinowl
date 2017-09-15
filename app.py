from flask import Flask
import requests
from configs import DEBUG
from twilio.rest import Client
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def getting_started():
    # Mailgun
    def send_simple_message():
        print("sending mail")
        return requests.post(
            "https://api.mailgun.net/v3/sandboxa8e484718ff94915893b6851f8874884.mailgun.org/messages",
            auth=("api", "key-3ac3180cb95d26588b96113d0f751d14"),
            data={"from": "Excited User <mailgun@sandboxa8e484718ff94915893b6851f8874884.mailgun.org>",
                  "to": ["kristifer.szabo@gmail.com"],
                  "subject": "Hello",
                  "text": "Testing some Mailgun awesomness!"})
    send_simple_message()

    # Twilio
    # Your Account SID from twilio.com/console
    account_sid = "AC5e763900f02b15a2670b6aea6d3ee111"
    # Your Auth Token from twilio.com/console
    auth_token  = "66c518075a5c322e72766bf8c336510c"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+15148065753",
        from_="+14387952675",
        body="Hello from Python!")

    print(message.sid)
    return "Hello World"


# app.run(debug=True) if __name__ == '__main__' and DEBUG else None


