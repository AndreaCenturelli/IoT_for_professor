import json
from datetime import datetime
import pytz
utc = pytz.utc

class CollisionDetectorEmulator(object):

	def __init__(self):
		self.collision = False

	def sendValue(self):
		data = {}
		data['type'] = "collision"
		data['timestamp'] = datetime.now(utc).strftime("%b %d %Y %H:%M:%S %Z")
		if self.collision:
			data['Status'] = "Accident"
		else:
			data['Status'] = "Ok"
		result = json.dumps(data)
		return result

	def changeValue(self, flag):
		self.collision = flag
