from flask import Flask, render_template, request, redirect, url_for
from src.models.sms import Sms
from src.models.database import Database
from src.models.alert import Alert
from src.models.geodatas import GeoData
import requests
import json
import configs
from os import environ
import datetime

app = Flask(__name__, template_folder="src/templates/", static_folder="src/static")
Database.initialize()

@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:check_now>', methods=['GET'])
def home(check_now=None):
    geodata = GeoData.get_user_location()
    print("***** NEW USER FROM:", geodata['city'], 'in', geodata['country'], "*****")
    
    if check_now:
        # For testing purposes. Manually checks for and send active alerts
        print(check_now)
        print('checking alerts manually')
        Alert.send_alerts()
    return render_template('layout.html')
    

@app.route('/crypto_form_consumer', methods=["POST"])
def crypto_form_consumer():
    form_data = request.form.to_dict()
    Alert.save_alert_to_db(form_data)
    
    print('***** NEW ALERT CREATED: ', form_data, "******")
    
    return json.dumps({'status':'OK','coin': form_data['coin'],'price': form_data['alert_price']})
    
@app.route('/play', methods=['GET'])
def play():
    # Just for fun, plays a random ambient song
    from bs4 import BeautifulSoup as b
    import random
    options = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty-one', 'twenty-two', 'twenty-three', 'twenty-four', 'twenty-five', 'twenty-six', 'twenty-seven', 'twenty-eight', 'twenty-nine', 'thirty', 'thirty-one', 'thirty-two', 'thirty-three', 'thirty-four', 'thirty-five', 'thirty-six', 'thirty-seven', 'thirty-eight', 'thirty-nine', 'forty', 'forty-one', 'forty-two', 'forty-three', 'forty-four', 'forty-five', 'forty-six', 'forty-seven', 'forty-eight', 'forty-nine', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twentyone', 'twentytwo', 'twentythree', 'twentyfour', 'twentyfive', 'twentysix', 'twentyseven', 'twentyeight', 'twentynine', 'thirty', 'thirtyone', 'thirtytwo', 'thirtythree', 'thirtyfour', 'thirtyfive', 'thirtysix', 'thirtyseven', 'thirtyeight', 'thirtynine', 'forty', 'fortyone', 'fortytwo', 'fortythree', 'fortyfour', 'fortyfive', 'fortysix', 'fortyseven', 'fortyeight', 'fortynine']
    r = requests.get('https://musicforprogramming.net/?' + random.choice(options))
    soup = b(r.text)
    link = soup.find('div', {'class': 'playerControls noselect'}).next_sibling.next_sibling.get('href')
    return render_template('play.html', link=link)


if not environ.get('webrun'):
    app.run(host='0.0.0.0', port=8080, debug=True) if __name__ == '__main__' and configs.DEBUG else None


