__author__ = "Kris"
from bson.objectid import ObjectId
from src.models.database import Database
from src.models.crptocurrency import CryptoCurrencies, ExchangeRates
from src.models.sms import Sms
from src.models.emails import Email


import json

class Alert(object):

    @staticmethod
    def save_alert_to_db(data):
        return Database.insert('altcoin_alerts', data)


    @staticmethod
    def get_alerts():
        # Returns an iterable MongoDB cursor object
        Database.initialize()
        alerts = Database.find('altcoin_alerts', {})

        return alerts

    @staticmethod
    def find_active_alerts():
        current_prices = CryptoCurrencies.get_current_price_btc_usd()
        exchange_rates = ExchangeRates.exchange_rates()
        alerts = Alert.get_alerts()
        # print(current_prices)
        # print(exchange_rates)

        sent_alerts = 0
        alerts_to_send = []
        
        for alert in alerts:
            print(alert)
            # current_price = current_prices[alert['coin']]
            alert_price = float(alert['alert_price'])
            then_price = float(alert['coin_current_price'])
            
            if alert['alert_currency'] == "BTC":
                current_price = current_prices[alert['coin']]['BTC']
        
            elif alert['alert_currency'] == "USD":
                current_price = current_prices[alert['coin']]['USD']
                
            elif alert['alert_currency'] == "ETH":
                btc_current_price = current_prices[alert['coin']]['BTC']
                current_price =  btc_current_price / current_prices['Ethereum']['BTC']
                
            else:
                current_price = current_prices[alert['coin']]['USD'] * exchange_rates['CAD']
                
                
            # usd_current_price = current_prices[alert['coin']]['USD']
            # cad_current_price = current_prices[alert['coin']]['USD'] * exchange_rates['CAD']
            # btc_current_price = current_prices[alert['coin']]['BTC']
            # eth_current_price = btc_current_price / current_prices['Ethereum']['BTC']
            
            
            
            if current_price < alert_price < then_price:
                alert['direction'] = 'fallen below'
                alerts_to_send.append(alert)
                Database.move_to_archive(alert, alert['_id'])
                sent_alerts += 1
                
            if then_price < alert_price < current_price:
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
                    message = "Heads up. {} has {} BTC {}".format(ats['coin'], ats['direction'], ats['alert_price'])
                    Sms.send(target=target, message=message)
                if ats['email']:
                    target = ats['email']
                    message = "Heads up. {} has {} BTC {}".format(ats['coin'], ats['direction'], ats['alert_price'])
                    Email.send(target, message)
            return json.dumps({'status': 200})
        else:
            return json.dumps({'status': 'no alerts to send'})

