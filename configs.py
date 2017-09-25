from os import environ


DEBUG = True

TWILIO_SENDER_NUMBER = "+1 438-795-2675"


if not environ.get('webrun'):
    import keys
    MAILGUN_API = keys.MAILGUN_API
    TWILIO_SID = keys.TWILIO_SID
    TWILIO_TOKEN = keys.TWILIO_TOKEN
else:
    MAILGUN_API = environ.get('MAILGUN_API')
    TWILIO_SID = environ.get('TWILIO_SID')
    TWILIO_TOKEN = environ.get('TWILIO_TOKEN')