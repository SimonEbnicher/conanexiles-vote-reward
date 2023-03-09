#!/usr/bin/python3

import json
import requests

class API:
    def __init__(self, key):
        self.key  = key

    def get_votes(self):
        req = requests.get('https://conan-exiles.com/api/?object=servers&element=votes&key={key}&format=json&limit=1000'.format(key=self.key))
        rdata = json.loads(str(req.text))
        data = []
        for x in rdata['votes']:
            # nickname input validation is not done here, we trust guidelines of conan-exiles.com, only alphanumeric and underscore allowed
            data.append( {'steamid':x['steamid'], 'name':x['nickname'], 'ts_voted':x['timestamp']} )
        return data

    def get_server_data(self):
        req = requests.get('https://conan-exiles.com/api/?object=servers&element=detail&key={key}'.format(key=self.key))
        return str(req.text)
        
