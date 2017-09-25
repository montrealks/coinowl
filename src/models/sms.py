__author__ = "Kris"

import datetime

from src.models.database import Database
from twilio.rest import Client



class Sms(object):
    def __init__(self,
                 message = None,
                 delivery_time = None,
                 sender="+14387952675",
                 target=None):

        self.sender = sender
        self.delivery_time = delivery_time if delivery_time is not None else datetime.datetime.now() + datetime.timedelta(minutes=10)
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


    def retrieve(self):
        sms_messages = Database.find('sms_jobs', {'message.delivery_time': {'$gt': self.current_time}})
        if sms_messages.count() == 0:
            return False
        else:
            return sms_messages



    def send(self):
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

