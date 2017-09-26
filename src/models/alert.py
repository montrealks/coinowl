__author__ = "Kris"
from bson.objectid import ObjectId
from src.models.database import Database
from src.models.crptocurrency import Currencies
from src.models.sms import Sms
from src.models.emails import Email


import json

class Alert(object):

    @staticmethod
    def save_alert_to_db(coin, price, sms, email, timestamp, btc_price_at_creation):
        json = {
            'coin': coin,
            'btc_alert_price': price,
            'sms': sms if sms is not None else None,
            'email': email if email is not None else None,
            'creation_time': timestamp,
            'btc_price_at_creation': btc_price_at_creation
        }
        Database.insert('altcoin_alerts', json)
        return json

    @staticmethod
    def get_alerts():
        Database.initialize()
        alerts = Database.find('altcoin_alerts', {})

        return alerts

    @staticmethod
    def find_active_alerts():
        current_prices = Currencies.get_current_price_btc()
        alerts = Alert.get_alerts()
        sent_alerts = 0
        alerts_to_send = []
        
        for alert in alerts:

            current = current_prices[alert['coin']]
            alert_price = alert['btc_alert_price']
            then = alert['btc_price_at_creation']
            
            print(alert)
            if current_prices[alert['coin']] < alert_price < then:
                alert['direction'] = 'fallen below'
                alerts_to_send.append(alert)
                Database.move_to_archive(alert, alert['_id'])
                
                sent_alerts += 1
                
            if then < alert_price < current:
                alert['direction'] = 'exceeded'
                alerts_to_send.append(alert)
                Database.move_to_archive(alert, alert['_id'])

                sent_alerts += 1
                
        return alerts_to_send

    @staticmethod
    def send_alerts():
        al = Alert.find_active_alerts()
        print(len(al), 'active alerts')
        if len(al) > 0:
            for ats in al: # ats = alert to send
                if ats['sms']:
                    target = ats['sms']
                    message = "Heads up. {} has {} BTC {}".format(ats['coin'], ats['direction'], ats['btc_alert_price'])
                    Sms.send(target=target, message=message)
                if ats['email']:
                    target = ats['email']
                    message = "Heads up. {} has {} BTC {}".format(ats['coin'], ats['direction'], ats['btc_alert_price'])
                    Email.send(target, message)
            return json.dumps({'status': 200})
        else:
            return json.dumps({'status': 'no alerts to send'})

