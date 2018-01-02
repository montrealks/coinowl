__author__ = "Kris"
import requests



class CryptoCurrencies(object):
    CRYPTO_CURRENCIES = None
    """
from src.models.crptocurrency import CryptoCurrencies as cc
c = cc()
c.crypto_current_values()
c.get_current_price_btc_usd()
    """
    @staticmethod
    def crypto_current_values():
        r = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0")
        CryptoCurrencies.CRYPTO_CURRENCIES = r.json()

    @staticmethod
    def crypto_names():
        currency_names = []
        for currency in CryptoCurrencies.CRYPTO_CURRENCIES:
            currency_names.append(currency['name'])
        return currency_names

    @staticmethod
    def crypto_ticker_symbols():
        ticker_symbols = []
        for currency in CryptoCurrencies.CRYPTO_CURRENCIES:
            ticker_symbols.append(currency['symbol'])
        return ticker_symbols

    @staticmethod
    def get_current_price_btc_usd():
        CryptoCurrencies.crypto_current_values()
        prices = {}
        
        for currency in CryptoCurrencies.CRYPTO_CURRENCIES:
            if currency['price_usd'] == None or currency['price_btc'] == None:
                continue
            prices[currency['name']] = {
                'USD': float(currency['price_usd']),
                'BTC': float(currency['price_btc']),
                                    }
        return prices
        
        
class ExchangeRates(object):
    EXCHANGE_RATES = None
    
    @staticmethod
    def exchange_rates():
        r = requests.get("https://api.fixer.io/latest?base=USD")
        ExchangeRates.EXCHANGE_RATES = r.json()['rates']
        return ExchangeRates.EXCHANGE_RATES
        