# flaskapp.py
# Source: https://pythonforundergradengineers.com/flask-iot-server-database.html
# Source: https://likegeeks.com/python-sqlite3-tutorial/
# Source: http://numericalexpert.com/blog/sqlite_blob_time/sqlite_time_etc.html
# Source: https://stackoverflow.com/questions/4272908/sqlite-date-storage-and-conversion

import requests
from flask import Flask
from authenticate import USER_LIST, CLIENTID_LIST
from datetime import datetime
import pytz
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
    cursorObj = conn.cursor()
    cursorObj.execute('INSERT INTO data(timestamp, user, clientid, field, data) VALUES(?, ? ,?, ?, ?)', entities)
    conn.commit()

def sql_last(user, clientid, field):
    conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
    cursorObj = conn.cursor()                                                                                    
    cursorObj.execute("SELECT data, timestamp, MAX(rowid) FROM data WHERE user=? AND clientid=? AND field=?", (user, clientid, field,))                      
    last_data, last_timestamp, *other = cursorObj.fetchone()
    conn.close()
    return str(last_timestamp.isoformat()) + '   ' + str(last_data)

app = Flask(__name__)

@app.route("/last/user=<user>&clientid=<clientid>&field=<int:field>", methods=['GET'])
def index(user, clientid, field):
    last_entry = sql_last(user, clientid, field)

    #c.execute("SELECT data, date_time, MAX(rowid) FROM data WHERE field=?", ('2',))
    #row2 = c.fetchone()
    #data1 = str(round((float(row1[0]) * 1.8) + 32))
    #data2 = str(round((float(row2[0]) * 1.8) + 32))
    #time_str1 = row1[1]
    #t1 = dateutil.parser.parse(time_str1)
    #t_pst1 = t1.astimezone(pytz.timezone('US/Pacific'))
    #time_stamp1 = t_pst1.strftime('%I:%M:%S %p   %b %d, %Y')
    #time_str2 = row2[1]
    #t2 = dateutil.parser.parse(time_str2)
    #t_pst2 = t2.astimezone(pytz.timezone('US/Pacific'))
    #time_stamp2 = t_pst2.strftime('%I:%M:%S %p   %b %d, %Y')

    return last_entry

@app.route("/update/user=<user>&clientid=<clientid>&field=<int:field>&data=<data>", methods=['GET'])
def write_data_point(user, clientid, field, data):
    if (str(user) in USER_LIST and str(clientid) in CLIENTID_LIST):
        timestamp = datetime.now(tz=pytz.utc)
        entities = (timestamp, str(user), str(clientid), int(field), round(float(data), 2))

        conn = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)
        sql_insert(conn, entities)
        conn.close()

        return data

    else:
        return "Failed"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
