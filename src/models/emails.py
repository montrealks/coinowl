__author__ = "Kris"
from src.models.database import Database
import datetime
import requests
import configs


class Email(object):
    def __init__(self,
                 message = None,
                 delivery_time = None,
                 sender="+14387952675",
                 target="+15148065753"):

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

        return Database.insert('email_jobs', {'message': json})


    def retrieve(self):
        messages = Database.find('email_jobs', {'message.delivery_time': {'$gt': self.current_time}})
        if messages.count() == 0:
            return False
        else:
            return messages

    @staticmethod
    def send(target, message, sender=None, subject="Crypto Price Alert"):
        print("sending mail")

        return requests.post(
            "https://api.mailgun.net/v3/sandboxa8e484718ff94915893b6851f8874884.mailgun.org/messages",
            auth=("api", configs.MAILGUN_API),
            data={"from": "Coin Alert <mailgun@sandboxa8e484718ff94915893b6851f8874884.mailgun.org>",
                  "to": target,
                  "subject": subject,
                  "text": message})


