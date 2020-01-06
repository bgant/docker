# flaskapp.py
# Source: https://pythonforundergradengineers.com/flask-iot-server-database.html
# Source: https://likegeeks.com/python-sqlite3-tutorial/
# Source: http://numericalexpert.com/blog/sqlite_blob_time/sqlite_time_etc.html
# Source: https://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion

from flask import Flask, request, Response
from authenticate import API_KEY, CHANNELS
from datetime import datetime, timezone
import pytz
import sqlite3
import json

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
        key integer PRIMARY KEY,
        timestamp real,
        api_key text,
        field1 real,
        field2 real)
        ''')
conn.commit()
conn.close()


##########################################################################
# Input Validation
##########################################################################

# api_key is Alphanumeric
def valid_api_key(api_key):
    if api_key.isalnum():
        return True
    else:
        return False

# channel is Numeric in ThingSpeak but Alphanumeric might be find too
def valid_channel(channel):
    if str(channel).isnumeric():
    #if str(channel).isalnum():
        return True
    else:
        return False

# results is Numeric [0-9] (no minus sign)
def valid_results(results):
    if str(results).isnumeric():
        return True
    else:
        return False 

# field1 and field2 are Floaiting Point Numbers
def valid_field(field):
    try:
        float(field)
        return True
    except:
        return False

# timezone is Alphabet plus '/' and works
def valid_timezone(timezone):
    if timezone.replace('/', '').isalpha():
        try:
            pytz.timezone(timezone)
            return True
        except:
            return False
    else:
        return False


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
        timestamp = datetime.timestamp(datetime.now())  # Floating Point Number
        entities = (timestamp, api_key, field1, field2)
        sql_insert(entities)
        return str(field1)
    else:
        return Response('Failed', status=403, mimetype='text/plain')


##########################################################################
# Associate CHANNEL & API_KEY
##########################################################################

def find_api_key(channel):
    api_key = None
    for x in CHANNELS:
        if x['response']['channel']['id'] == channel:
            api_key = x['api_key']
    return api_key

def feed_info(channel):
    response = None
    for x in CHANNELS:
        if x['response']['channel']['id'] == channel:
            response = x['response']
    return response


##########################################################################
# Database Timestamp Float to String
##########################################################################

def timestamp_float_to_string(timestamp, timezone):
    return datetime.fromtimestamp(timestamp, tz=pytz.timezone(timezone)).replace(microsecond=0).isoformat()


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

# Usage: http://<SERVER>/last?channel=<numeric>
@app.route("/last", methods=['GET'])
def last():
    channel = request.args.get('channel', type=str)
    timezone = request.args.get('timezone', default='US/Central', type=str)
    if valid_channel(channel):
        if not valid_timezone(timezone):
            return Response('Unknown Timezone', status=403, mimetype='text/plain')

        api_key = find_api_key(channel)
        if api_key:
            timestamp, field1, field2, entry_id = sql_last(api_key)
            timestamp_string = timestamp_float_to_string(timestamp, timezone)
            return timestamp_string + '   ' + str(field1) + '   ' + str(field2)

    return Response('Failed', status=403, mimetype='text/plain') 

# ThingSpeak Text Format: https://api.thingspeak.com/channels/946198/fields/1/last.txt
@app.route("/channels/<channel>/fields/<field>/last.txt", methods=['GET'])
def last_txt(channel, field):
    api_key = find_api_key(channel)
    if api_key:
        last_timestamp, last_field1, last_field2, entry_id = sql_last(api_key)
        if field == '1':
            return Response(str(last_field1), mimetype='text/plain')
        elif field == '2':
            return Response(str(last_field2), mimetype='text/plain')
        else:
            return Response('Failed', status=403, mimetype='text/plain')
    else:
        return Response('Failed', status=403, mimetype='text/plain')

# ThingSpeak JSON Format: https://api.thingspeak.com/channels/946198/fields/1/last.json
#       Example Response: {"created_at":"2020-01-02T20:47:35Z","entry_id":3306,"field1":"70.6"}
@app.route("/channels/<channel>/fields/<field>/last.json", methods=['GET'])
def last_json(channel, field):
    timezone = request.args.get('timezone', default='US/Central', type=str)
    if valid_channel(channel):
        if not valid_timezone(timezone):
            return Response('Unknown Timezone', status=403, mimetype='text/plain')

        api_key = find_api_key(channel)
        if api_key:
            timestamp, field1, field2, entry_id = sql_last(api_key)
            timestamp_string = timestamp_float_to_string(timestamp, timezone)
            if field == '1':
                output_dict = {'created_at': timestamp_string, 'entry_id': entry_id, 'field1': field1}
                output_json = json.dumps(output_dict)
                return Response(output_json, mimetype='application/json')
            elif field == '2':
                output_dict = {'created_at': timestamp_string, 'entry_id': entry_id, 'field2': field2}
                output_json = json.dumps(output_dict) 
                return Response(output_json, mimetype='application/json')

    return Response('Failed', status=403, mimetype='text/plain')


########################################################################## 
# Request ThingSpeak styled feed.json
##########################################################################

def sql_feed(channel, results, timezone):
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    cursorObj = conn.cursor()
    api_key = find_api_key(channel)
    cursorObj.execute("SELECT key, timestamp, field1, field2 FROM data WHERE api_key=? ORDER BY key DESC LIMIT ?;", (api_key, results))  # Must be a Tuple even if only one variable: i.e. (api_key,)
    records = cursorObj.fetchall()

    response = feed_info(channel)
    feeds = response['feeds']
    feeds.clear()  # Clear list each run

    for row in records:
        key, timestamp, field1, field2 = row
        timestamp_string = timestamp_float_to_string(timestamp, timezone)
        if field2:
            output_dict = {'created_at': timestamp_string, 'entry_id': key, 'field1': field1, 'field2': field2}
        else:
            output_dict = {'created_at': timestamp_string, 'entry_id': key, 'field1': field1}
        feeds.append(output_dict)

    feeds.reverse() # Sort oldest to newest

    conn.close()
    return response

# ThingSpeak JSON Format: https://api.thingspeak.com/channels/946198/feeds.json?results=50&api_key=&timezone=America/Chicago
@app.route("/channels/<channel>/feeds.json", methods=['GET'])
def feeds_json(channel): 
    results = request.args.get('results', default=10, type=int)  # non-digits ignored
    timezone = request.args.get('timezone', default='US/Central', type=str)

    if valid_channel(channel) and valid_results(results):
        if not valid_timezone(timezone):
            return Response('Unknown Timezone', status=403, mimetype='text/plain')

        # Handle results=0 requests from Android IoT ThingSpeak Monitor Widget
        if results == 0:
            empty_feed = True
            results = 1  # To get last entry_id and created_at before clearing list
        elif results > 10:
            results = 10
            empty_feed = False
        else:
            empty_feed = False

        api_key = find_api_key(channel)
        if api_key:
            response = sql_feed(channel, results, timezone)
            response['channel']['last_entry_id'] = response['feeds'][-1]['entry_id']  # Set channel last_entry_id
            response['channel']['updated_at'] = response['feeds'][-1]['created_at']   # Set channel updated_at
            if empty_feed:
               response['feeds'].clear() 
            response_json = json.dumps(response)
            return Response(response_json, mimetype='application/json')

    return Response('Failed', status=403, mimetype='text/plain')


if __name__ == "__main__":
    main()
