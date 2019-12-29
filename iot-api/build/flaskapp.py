# flaskapp.py

from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def index():
    r = requests.get('https://api.thingspeak.com/channels/946198/fields/1/last.txt')
    response = '<h1> The temperature is ' + str(round(float(r.text), 1)) + 'F</h1>'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
