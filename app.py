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
local_or_remote = " web" if environ.get('webrun') else " local"

print(configs.MAILGUN_API)

Database.initialize()



@app.route('/', methods=['GET', 'POST'])
def home():
    print('hello')
    if request.method == 'GET':
        return render_template('layout.html', today=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
    return None



@app.route('/reminder_form_consumer', methods=["POST"])
def reminder_form_consumer():
    print(request.form.get)
    delivery_time = datetime.datetime.strptime(request.form['date-time'], '%d/%m/%Y %H:%M:%S')
    body = request.form['body']
    choice = request.form['sms_or_email']

    if choice == "sms":
        # Sms(body, delivery_time).save_to_mongo()
        return json.dumps({'status':'OK','body':body,'choice':choice, 'delivery date': delivery_time.timestamp()})
    elif choice == "email":
        # Email(body, delivery_time).save_to_mongo()
        return json.dumps({'status':'OK','body':body,'choice':choice, 'delivery date': delivery_time.timestamp()})
    else:
        # Email(body, delivery_time).save_to_mongo()
        # Sms(body, delivery_time).save_to_mongo()
        return json.dumps({'status':'OK','body':body,'choice':choice, 'delivery date': delivery_time.timestamp()})


@app.route('/crypto_form_consumer', methods=["POST"])
def crypto_form_consumer():
    delivery_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    coin = request.form['crypto_chooser']
    price = request.form['amount_chooser']
    email = request.form['user_email']
    sms = request.form['user_phone']
    btc_price_at_creation = request.form['btc_price_at_creation']

    Alert.save_alert_to_db(coin, price, sms, email, delivery_time, btc_price_at_creation)

    return json.dumps({'status':'OK','coin':coin,'price':price, 'delivery date': delivery_time})


if not environ.get('webrun'):
    app.run(host='0.0.0.0', port=8080, debug=True) if __name__ == '__main__' and configs.DEBUG else None


