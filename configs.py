from os import environ


DEBUG = True

TWILIO_SENDER_NUMBER = "+1 438-795-2675"
MAILGUN_POST = "https://api.mailgun.net/v3/sandboxa8e484718ff94915893b6851f8874884.mailgun.org/messages"
MAILGUN_FROM = "Coin Alert <mailgun@sandboxa8e484718ff94915893b6851f8874884.mailgun.org>"


if not environ.get('webrun'):
    import keys
    MONGO_URI = keys.MONGO_URI
    MAILGUN_API = keys.MAILGUN_API
    TWILIO_SID = keys.TWILIO_SID
    TWILIO_TOKEN = keys.TWILIO_TOKEN
else:
    MAILGUN_API = environ.get('MAILGUN_API')
    TWILIO_SID = environ.get('TWILIO_SID')
    TWILIO_TOKEN = environ.get('TWILIO_TOKEN')
    MONGO_URI = environ.get('MONGO_URI')