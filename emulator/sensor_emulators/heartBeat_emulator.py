import json
from datetime import datetime
import pytz
utc = pytz.utc

class HeartBeatEmulator(object):

    def __init__(self):
        self.BPM = 85

    def increaseHeartBeat(self):
        increaseInit = 0.08
        increaseLater = 0.01
        if self.BPM <120:
            self.BPM = self.BPM + self.BPM*increaseInit
        else:
            self.BPM = self.BPM + self.BPM*increaseLater
    def decreaseHeartBeat(self):
        decreaseInit = 0.08
        decreaseLater = 0.01
        if self.BPM > 95:
            self.BPM = self.BPM - self.BPM*decreaseInit
        else:
            self.BPM = self.BPM - self.BPM*decreaseLater
    def park(self):
        self.BPM = 85


    def sendValue(self):
        data = {}
        data['type'] = 'heart_beat'
        data['timestamp'] = datetime.now(utc).strftime("%b %d %Y %H:%M:%S %Z")
        data['value'] = round(self.BPM)
        result = json.dumps(data)
        return result

