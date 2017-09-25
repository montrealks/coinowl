__author__ = "Kris"
import requests



class Currencies(object):
    CURRENCIES = None

    @staticmethod
    def get_all_currencies():
        r = requests.get("https://api.coinmarketcap.com/v1/ticker/")
        Currencies.CURRENCIES = r.json()

    @staticmethod
    def get_currency_names():
        currency_names = []
        for currency in Currencies.CURRENCIES:
            currency_names.append(currency['name'])
        return currency_names

    @staticmethod
    def get_ticker_symbols():
        ticker_symbols = []
        for currency in Currencies.CURRENCIES:
            ticker_symbols.append(currency['symbol'])
        return ticker_symbols

    @staticmethod
    def get_current_price_btc():
        Currencies.get_all_currencies()
        prices = {}
        for currency in Currencies.CURRENCIES:
            prices[currency['name']] = currency['price_btc']
        return prices
