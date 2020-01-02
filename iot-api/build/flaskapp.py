# flaskapp.py
# Source: https://pythonforundergradengineers.com/flask-iot-server-database.html
# Source: https://likegeeks.com/python-sqlite3-tutorial/
# Source: http://numericalexpert.com/blog/sqlite_blob_time/sqlite_time_etc.html
# Source: https://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion

from flask import Flask, request
from authenticate import USER_LIST, CLIENTID_LIST
from datetime import datetime, timezone
import sqlite3

dbfile = '/opt/data/data.db'

# Open database or create file if it does not already exist
conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
# Create Table structure if it does not already exist
cursorObj = conn.cursor()
cursorObj.execute('''
        CREATE TABLE IF NOT EXISTS data (
        key integer PRIMARY KEY AUTOINCREMENT,
        [timestamp] timestamp,
        user text,
        clientid text,
        field integer,
        data real)
        ''')
conn.commit()
conn.close()

def sql_insert(conn, entities):
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    cursorObj = conn.cursor()
    cursorObj.execute('INSERT INTO data(timestamp, user, clientid, field, data) VALUES(?, ? ,?, ?, ?)', entities)
    conn.commit()
    conn.close()

def sql_last(user, clientid, field):
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    cursorObj = conn.cursor()                                                                                    
    cursorObj.execute("SELECT data, timestamp, MAX(rowid) FROM data WHERE user=? AND clientid=? AND field=?", (user, clientid, field,))                      
    last_data, last_timestamp, *other = cursorObj.fetchone()
    conn.close()
    return str(last_timestamp.isoformat()) + '   ' + str(last_data)

app = Flask(__name__)

# Usage: http://<SERVER>/last?user=TOM&clientid=999&field=1
#@app.route("/last/user=<user>&clientid=<clientid>&field=<int:field>", methods=['GET'])
#def index(user, clientid, field):
@app.route("/last", methods=['GET'])
def last():
    user = request.args.get('user', type=str)
    clientid = request.args.get('clientid', type=str)
    field = request.args.get('field', default = 1, type=int)
    last_entry = sql_last(user, clientid, field)
    return str(last_entry)

# Usage: http://<SERVER>/update?user=TOM&clientid=999&field=1&data=77.8
#@app.route("/update/user=<user>&clientid=<clientid>&field=<int:field>&data=<data>", methods=['GET'])
#def write_data_point(user, clientid, field, data):
@app.route("/update", methods=['GET'])
def update():
    user = request.args.get('user', type=str)                                                                          
    clientid = request.args.get('clientid', type=str)                                                                  
    field = request.args.get('field', default = 1, type=int)   
    data = request.args.get('data', type=float)

    if (str(user) in USER_LIST and str(clientid) in CLIENTID_LIST):
        timestamp = datetime.now(timezone.utc)
        entities = (timestamp, str(user), str(clientid), int(field), round(float(data), 2))
        sql_insert(conn, entities)
        return str(data)
    else:
        return "Failed"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
