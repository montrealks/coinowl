from flask import Flask, render_template, request, redirect, url_for
from src.models.sms import Sms
from src.models.database import Database
from src.models.alert import Alert
import requests
import json
import configs
from os import environ
import datetime 


app = Flask(__name__, template_folder="src/templates/", static_folder="src/static")

Database.initialize()
@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:check_now>', methods=['GET', 'POST'])
def home(check_now=None):
    # For testing purposes. Manually checks for and send active alerts
    if check_now:
        print(check_now)
        print('checking alerts manually')
        Alert.send_alerts()
    return render_template('layout.html')
    

@app.route('/crypto_form_consumer', methods=["POST"])
def crypto_form_consumer():
    form_data = request.form.to_dict()
    Alert.save_alert_to_db(form_data)
    
    print('new alert created: ', form_data)
    
    return json.dumps({'status':'OK','coin': form_data['coin'],'price': form_data['btc_alert_price']})


if not environ.get('webrun'):
    app.run(host='0.0.0.0', port=8080, debug=True) if __name__ == '__main__' and configs.DEBUG else None


