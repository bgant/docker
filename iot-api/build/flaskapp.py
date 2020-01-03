# flaskapp.py
# Source: https://pythonforundergradengineers.com/flask-iot-server-database.html
# Source: https://likegeeks.com/python-sqlite3-tutorial/
# Source: http://numericalexpert.com/blog/sqlite_blob_time/sqlite_time_etc.html
# Source: https://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion

from flask import Flask, request, Response
from authenticate import API_KEY
from datetime import datetime, timezone
import sqlite3

dbfile = '/opt/data/data.db'

app = Flask(__name__)


##########################################################################
# Initialize Database if Needed
##########################################################################

# Open database or create file if it does not already exist
conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
# Create Table structure if it does not already exist
cursorObj = conn.cursor()
cursorObj.execute('''
        CREATE TABLE IF NOT EXISTS data (
        key integer PRIMARY KEY AUTOINCREMENT,
        [timestamp] timestamp,
        api_key text,
        field1 real,
        field2 real)
        ''')
conn.commit()
conn.close()


##########################################################################
# IoT Data Updates
##########################################################################

def sql_insert(entities):
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    cursorObj = conn.cursor()
    cursorObj.execute('INSERT INTO data(timestamp, api_key, field1, field2) VALUES(? ,?, ?, ?)', entities)  #entities is a tuple
    conn.commit()
    conn.close()

# Usage: http://<SERVER>/update?api_key=TOM&field1=77.8&field2=45.6
#@app.route("/update/api_key=<api_key>&field1=<field1>&field2=<field2>", methods=['GET'])
#def write_data_point(api_key, field1, field2):
@app.route("/update", methods=['GET'])
def update():
    api_key = request.args.get('api_key', type=str)
    field1 = request.args.get('field1', type=float)
    field2 = request.args.get('field2', default=None, type=float)

    if str(api_key) in API_KEY:
        timestamp = datetime.now(timezone.utc)
        entities = (timestamp, api_key, field1, field2)
        sql_insert(entities)
        return str(field1)
    else:
        return "Failed"


##########################################################################
# Request Last Data Entry
##########################################################################

def sql_last(api_key):
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    cursorObj = conn.cursor()                                                                                    
    cursorObj.execute("SELECT timestamp, field1, field2, MAX(rowid) FROM data WHERE api_key=?", (api_key,)) # api_key is a tuple of one
    last_timestamp, last_field1, last_field2, entry_id = cursorObj.fetchone()
    conn.close()
    return (last_timestamp, last_field1, last_field2, entry_id)

# Usage: http://<SERVER>/last?channel=TOM
@app.route("/last", methods=['GET'])
def last():
    api_key = request.args.get('channel', type=str)
    last_timestamp, last_field1, last_field2, entry_id = sql_last(api_key)
    return str(last_timestamp.isoformat()) + '   ' + str(last_field1) + '   ' + str(last_field2)

# ThingSpeak Text Format: https://api.thingspeak.com/channels/946198/fields/1/last.txt
@app.route("/channels/<api_key>/fields/<field>/last.txt", methods=['GET'])
def last_txt(api_key, field):
    last_timestamp, last_field1, last_field2, entry_id = sql_last(api_key)
    if field == '1':
        return Response(str(last_field1), mimetype='text/plain')
    elif field == '2':
        return Response(str(last_field2), mimetype='text/plain')
    else:
        return None

# ThingSpeak JSON Format: https://api.thingspeak.com/channels/946198/fields/1/last.json
#       Example Response: {"created_at":"2020-01-02T20:47:35Z","entry_id":3306,"field1":"70.6"}
@app.route("/channels/<api_key>/fields/<field>/last.json", methods=['GET'])
def last_json(api_key, field):
    last_timestamp, last_field1, last_field2, entry_id = sql_last(api_key)
    last_timestamp_string = last_timestamp.isoformat().split('.')[0] + 'Z'  # Convert to ThingSpeak format
    import json
    if field == '1':
        output_dict = {'created_at': last_timestamp_string, 'entry_id': entry_id, 'field1': last_field1}
        output_json = json.dumps(output_dict)
        #return str(output_json)
        return Response(output_json, mimetype='application/json')
    elif field == '2':
        output_dict = {'created_at': last_timestamp_string, 'entry_id': entry_id, 'field2': last_field2}
        output_json = json.dumps(output_dict) 
        return Response(output_json, mimetype='application/json')
    else:
        return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
