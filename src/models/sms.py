__author__ = "Kris"
from .database import Database
import datetime
from twilio.rest import Client


class Sms(object):
    def __init__(self,
                 message=None,
                 delivery_time=datetime.datetime.now() + datetime.timedelta(minutes=10),
                 sender="+14387952675",
                 target="+15148065753"):

        self.sender = sender
        self.delivery_time = delivery_time
        self.message = message
        self.target = target
        self.current_time = datetime.datetime.now()


    def save_to_mongo(self):
        json = {
            'sender': self.sender,
            'delivery_time': self.delivery_time,
            'message': self.message,
            'creation_time': self.current_time
        }

        return Database.insert('sms_jobs', {'message': json})


    def retrieve_sms_messages(self):
        return Database.find('sms_jobs', {'message.delivery_time': {'$gt': self.current_time}})


    def send_sms(self):
        # Twilio
        # Your Account SID from twilio.com/console
        account_sid = "AC5e763900f02b15a2670b6aea6d3ee111"
        # Your Auth Token from twilio.com/console
        auth_token  = "66c518075a5c322e72766bf8c336510c"
        client = Client(account_sid, auth_token)

        client.messages.create(
            to=self.target,
            from_=self.sender,
            body=self.message)
