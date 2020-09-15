#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import uniform
import time
import json
import serial
from pprint import pprint
from datetime import datetime
import pytz
utc = pytz.utc


class GPSEmulator(object):

    def __init__(self):
        filePath = 'data/Polito_aeroporto.json'
        file = open(filePath)
        fileContent = file.read()
        filePythonDict = json.loads(fileContent)
        self.list_coordinates = filePythonDict['features'][2]['geometry']['coordinates'][0]
        self.index = 0
        file.close()

    def locationGenerator(self):
        self.longitude = self.list_coordinates[self.index][0]
        self.latitude = self.list_coordinates[self.index][1]
        data = {}
        data['type'] = 'gps'
        data['timestamp'] = datetime.now(utc).strftime("%b %d %Y %H:%M:%S %Z")
        data['latitude'] = self.latitude
        data['longitude'] = self.longitude
        result = json.dumps(data)
        return result

        
        
        
        