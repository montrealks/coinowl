__author__ = "Kris"
import datetime
import configs
from twilio.rest import Client


class Sms(object):

    @staticmethod
    def send(target, message, sender=configs.TWILIO_SENDER_NUMBER):
        # Twilio
        # Your Account SID from twilio.com/console
        account_sid = configs.TWILIO_SID
        # Your Auth Token from twilio.com/console
        auth_token  = configs.TWILIO_TOKEN
        client = Client(account_sid, auth_token)

        client.messages.create(
            to=target,
            from_=sender,
            body=message)

