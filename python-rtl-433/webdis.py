'''
from webdis import WEBDIS
webdis = WEBDIS()

webdis.ping()

webdis.get('foo')
webdis.response_text
webdis.response_json  <-- None

webdis.get('json-epa-aqi')
webdis.response_text
webdis.response_json  <-- JSON 
'''

import requests
import json

class WEBDIS:
    def __init__(self):
        self.host = '10.88.0.1'
        self.port = '7379'
        self.URL_base = f'http://{self.host}:{self.port}/' 

    def ping(self):
        self.URL = self.URL_base + f'PING'
        self.send(command='PING')

    def set(self,key=None,value=None):
        self.URL = self.URL_base + f'SET/{key}/{value}'
        self.send(command='SET')

    def get(self,key=None):
        self.URL = self.URL_base + f'GET/{key}'
        self.send(command='GET')

    def timeseries(self,key=None,value=None):
        self.URL = self.URL_base + f'TS.ADD/{key}/*/{value}'
        self.send(command='TS.ADD')
        
    def timeseriesget(self,key=None):
        self.URL = self.URL_base + f'TS.GET/{key}'
        self.send(command='TS.GET')

    def send(self, command=None):
        try:
            r = requests.get(self.URL)
            self.webdis_json = r.json()
            self.response_text = self.webdis_json[command]  # Webdis adds a JSON ['COMMAND'] before string response
        except:
            self.response_text = None
        try:
            self.response_json = json.loads(self.response_text)  # If Webdis string is JSON, convert to JSON format
        except:
            self.response_json = None


