from mqqtClient import Client
from device import Device
import json
import cherrypy
class ConnectorRest(object):
	exposed = True

	def __init__(self, connector):
		self.tripStatus = False
		self.connector = connector

	def GET(self, *uri, **params):
		if len(uri) != 0 :
			cmd = uri[0]
			if(cmd == "startTrip"):
				self.tripStatus = True
			elif(cmd == "endTrip"):
				self.tripStatus = False

	def POST(self, *uri, **params):
		if len(uri) != 0 :
			cmd = uri[0]
			rawData = cherrypy.request.body.read()
			data = json.loads(rawData)
			if(cmd == "setDetails"):
				data = json.loads(data)
				if data != {}:
					self.connector.broker = data['broker']
					self.connector.portNumber = data['port_number']
					self.connector.userId = data['userId']

					return json.dumps(data)
