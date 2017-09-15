from flask import Flask
from configs import DEBUG

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def getting_started():
    return "Hello World"


# app.run(debug=True) if __name__ == '__main__' and DEBUG else None


