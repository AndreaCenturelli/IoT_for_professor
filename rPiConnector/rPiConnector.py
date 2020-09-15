import requests
import json

class Connector(object):
	
	def __init__(self):
		self.url = 'http://127.0.0.1:8080'
		with open('config.json') as file:
			data = json.load(file)
		self.bikeID = data['bikeId']
		self.broker = ""
		self.userId = ""
		self.portNumber = 0

	def getBrokerAndUserDetials(self):
		uri = '/getbikedetails'
		params = {'bikeID' : self.bikeID}
		url = self.url + uri
		response = requests.get(url, params)
		result = response.text
		self.broker = result['broker']
		self.userId = result['userId']
		self.portNumber = result['port_number']

	def registerDevice(self, device):
		deviceData = {'deviceId' : device.deviceId, 'available_resources' : device.avResources, 'end_points' : device.endPoints}
		data = json.dumps(deviceData)
		uri = '/registerdevice'
		jsonData = data
		url = self.url + uri
		response = requests.post(url, json = jsonData)
