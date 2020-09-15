import json
from datetime import datetime
import pytz
utc = pytz.utc

class SpeedEmulator(object):

    def __init__(self):
        self.speed = 0

    def increaseSpeed(self):
        increaseInit = 0.5
        increaseLater = 0.01
        if self.speed == 0:
            self.speed = self.speed + 1
        elif self.speed < 15:
            self.speed = self.speed + self.speed*increaseInit
        else:
            self.speed = self.speed + self.speed*increaseLater

    def decreaseSpeed(self):
        decreaseInit = 0.5
        decreaseLater = 0.01
        if self.speed == 0:
            self.speed = 0
        elif self.speed > 10:
            self.speed = self.speed - self.speed*decreaseInit
        else:
            self.speed = self.speed - self.speed*decreaseLater

    def park(self):
        self.speed = 0


    def sendValue(self):
        data = {}
        data['type'] = 'speed'
        data['timestamp'] = datetime.now(utc).strftime("%b %d %Y %H:%M:%S %Z")
        data['value'] = round(self.speed,2)
        data['unit'] = 'km/h'
        result = json.dumps(data)
        return result