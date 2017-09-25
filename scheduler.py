
from src.models.alert import Alert

if __name__ == '__main__':
    print("running from heroku scheduler")
    Alert.send_alerts()