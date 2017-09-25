__author__ = "Kris"
from src.models.database import Database
import datetime
import requests
import configs


class Email(object):

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


