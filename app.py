from flask import Flask, render_template, request
import requests
from configs import DEBUG
from os import environ
from twilio.rest import Client
app = Flask(__name__, template_folder="src/templates/")

local_or_remote = " web" if environ.get('webrun') else " local"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        choice = request.form.get('choice')
        body = request.form.get('body')

        if choice == "sms":
            return twilio_api(body=body)
        elif choice == "email":
            return mailgun_api(body=body)
        else:
            return render_template('home.html')


@app.route('/mail', methods=['GET', 'POST'])
def mailgun_api(body=None):
    print(body)
    message = body if body is not None else "Hello from" + local_or_remote
    print(message)
    # Mailgun
    def send_simple_message():
        print("sending mail")
        return requests.post(
            "https://api.mailgun.net/v3/sandboxa8e484718ff94915893b6851f8874884.mailgun.org/messages",
            auth=("api", "key-3ac3180cb95d26588b96113d0f751d14"),
            data={"from": "Excited User <mailgun@sandboxa8e484718ff94915893b6851f8874884.mailgun.org>",
                  "to": ["kristifer.szabo@gmail.com"],
                  "subject": "Hello",
                  "text": message})
    send_simple_message()
    return "Sending mail from" + local_or_remote

@app.route('/sms', methods=['GET', 'POST'])
def twilio_api(body=None):
    print(body)
    message = body if body is not None else "Hello from" + local_or_remote
    print(message)
    # Twilio
    # Your Account SID from twilio.com/console
    account_sid = "AC5e763900f02b15a2670b6aea6d3ee111"
    # Your Auth Token from twilio.com/console
    auth_token  = "66c518075a5c322e72766bf8c336510c"
    client = Client(account_sid, auth_token)
    client.messages.create(
        to="+15148065753",
        from_="+14387952675",
        body=message)

    return "Sending SMS from" + local_or_remote


if not environ.get('webrun'):
    app.run(debug=True) if __name__ == '__main__' and DEBUG else None


