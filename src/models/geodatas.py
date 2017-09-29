import requests
from flask import request

class GeoData(object):
    
    @staticmethod
    def get_user_location():
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        r = requests.get("http://ip-api.com/json/" + ip_address).json()
        return r