__author__ = "Kris"
import requests
import configs


class Email(object):

    @staticmethod
    def send(target='kristifer.szabo@gmail.com', message="functionality test", sender=None, subject="Crypto Price Alert"):
        print("sending mail")

        return requests.post(
            configs.MAILGUN_POST,
            auth=("api", configs.MAILGUN_API),
            data={"from": configs.MAILGUN_FROM,
                  "to": target,
                  "subject": subject,
                  "text": message})


