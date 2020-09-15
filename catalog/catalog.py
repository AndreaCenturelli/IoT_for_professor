import cherrypy
import json
from catalogOperations import CatalogOperations

class Catalog(CatalogOperations):
	exposed = True

	def __init__(self):
		CatalogOperations.__init__(self)

	def GET(self, *uri, **params):
		if len(uri) != 0 :
			cmd = uri[0]
			if(cmd == "getbikedetails"):
				if params != {}:
					bikeID = params['bikeID']
					return self.retrieveBrokerAndUserId(bikeID)

			elif(cmd == "getalldevices"):
				if params != {}:
					deviceType = params['deviceType']
					return self.getAllDevices(deviceType)

			elif(cmd == "getuser"):
				if params != {}:
					userId = params['userId']
					return self.retrieveUser(userId)

			elif(cmd in self.SensorNameList):
				if params != {}:
					userId = params['UserID']
					return self.microserviceGet(userId, cmd)

			elif (cmd == 'Users'):
				return self.usersGet()

			elif(cmd == "getAllTrips"):
				if params != {}:
					userId = params['userId']
					return self.getAllTrips(userId)

			elif(cmd == "getTrip"):
				if params != {}:
					userId = params['userId']
					tripId = params['tripId']
					return self.getTrip(userId,tripId)

			elif(cmd == "getEndPoints"):
				if params != {}:
					userId = params['userId']
					bikeID = params['bikeId']
					return self.getEndPoints(userId,bikeID)

			elif(cmd == "endTrip"):
				if params != {}:
					bikeID = params['bikeId']
					return self.endTrip(bikeID)


	def POST(self, *uri, **params):
		if len(uri) != 0 :
			cmd = uri[0]
			rawData = cherrypy.request.body.read()
			data = json.loads(rawData)

			if(cmd == "registerdevice"):
				deviceData = data
				return self.addDevice(deviceData)
				
			elif(cmd == "setbikedetails"):
				bikeData = data
				return self.setBikeDetails(bikeData['userId'],bikeData['bikeId'])

			elif(cmd == "addUser"):
				userData = data
				return self.addUser(userData)

			elif(cmd == "editUser"):
				userData = data
				if params != {}:
					userId = params['userId']
					return self.editUser(userId, userData)

			elif(cmd == "login"):
				userData = data
				return self.login(userData)

			elif(cmd == "logout"):
				if params != {}:
					userId = params['userId']
					self.logout(userId)


if __name__ == "__main__":
	conf = {
		'/' : {
				'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
				'tool.session.on' : True
		}
	}

	cherrypy.tree.mount(Catalog(),'/',conf)
	cherrypy.engine.start()
	cherrypy.engine.block()
	







		