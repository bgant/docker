# flaskapp.py

import requests
from flask import Flask
from authenticate import USER_LIST, CLIENTID_LIST
app = Flask(__name__)

@app.route("/")
def index():
    r = requests.get('https://api.thingspeak.com/channels/946198/fields/1/last.txt')
    response = '<h1> The temperature is ' + str(round(float(r.text), 1)) + 'F</h1>'
    return response

@app.route("/update/user=<user>/clientid=<clientid>/field=<int:field>/data=<data>", methods=['GET'])
def write_data_point(user, clientid, field, data):
    if (str(user) in USER_LIST and str(clientid) in CLIENTID_LIST):
        return data
    else:
        return "Failed"
    #return render_template("update.html", data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
