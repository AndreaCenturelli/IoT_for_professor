import json
import requests 
import uuid
import cherrypy
import datetime
from tzlocal import get_localzone # $ pip install tzlocal

localtimezone = str(get_localzone())

class CatalogOperations(object):
	def __init__(self):
		self.userDict = {}
		self.bikeDict = {}
		self.deviceDict = {}
		self.SensorNameList = ['Collision','GPS','Speed','HeartRate','AntiTheft']
		self.catalog_cache = {}
		self.windowData = {}
		self.url = "http://127.0.0.1:8086"
		with open('devices.json', 'w') as outfile:
			json.dump(self.deviceDict, outfile)

	def addUser(self, userData):
		#add url call if sucessfull make catalog cache for user
		uri = "/addUser"
		url = self.url + uri 
		response = requests.post(url, json = userData)
		data = {}
		#response from request
		if response.status_code == 200:
			data = json.loads(response.text)
			userId = data['id']
			data['Timezone'] = localtimezone
			self.userDict[userId] = data
			self.catalog_cache[userId] = ({},data)
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---") 


		return json.dumps(data)


	def editUser(self, userId, userData):
		#edit url call if sucessfull update catalog cache for user
		uri = "/updateUser"
		url = self.url + uri
		params = {'userId' : userId}
		response = requests.post(url, params = params, json = userData)
		data = {}
		#response from request
		if response.status_code == 200:
			data = json.loads(response.text)
			self.userDict[userId] = data
			self.catalog_cache[userId][1] = data
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---") 


		return json.dumps(data)

	def retrieveUser(self, userId):
		result = ""
		if userId in self.userDict:
			result = self.userDict[userId]
		else:
			#url to retrieve user
			uri = "/getUser"
			url = self.url + uri
			response = requests.get(url)
			if response.status_code == 200:
				result = json.loads(response.text)
			elif response.status_code == 400:
				raise cherrypy.HTTPError(400,"---")

		return json.dumps(result)

	def getAllTrips(self, userId):
		result = ""
		uri = "/getTrips"
		params = {'userId' : userId}
		url = self.url + uri
		response = requests.get(url,params)
		
		if response.status_code == 200:
			result = response.text
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---")
		
		return result

	def getTrip(self, userId, tripId):
		result = ""
		uri = "/getTripbyID"
		params = {'userId' : userId, 'tripId': tripId}
		url = self.url + uri
		response = requests.get(url,params)
		
		if response.status_code == 200:
			result = response.text
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---")
		
		return result


	def retrieveBrokerAndUserId(self, bikeId):
		result = ""
		if bikeId in self.bikeDict:
			result = self.bikeDict
		else:
			result = {'broker' : '', 'port_number' : 0, 'userId' : ''}

		return json.dumps(result)


	def getBrokerDetails(self, bikeId):
		result = ""
		uri = "/getBike"
		url = self.url + uri
		params = {'bikeId' : bikeId}
		response = requests.get(url, params)

		if response.status_code == 200:
			result = response.text
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---")
		
		return json.loads(result)

	def addDevice(self, deviceData):
		with open('devices.json') as file:
			self.deviceDict = json.load(file)
		data = json.loads(deviceData)
		deviceId = data['deviceId']
		data.pop('deviceId')
		if deviceId not in self.deviceDict:
			print(data)
			self.deviceDict[deviceId] = data


		with open('devices.json', 'w') as outfile:
			json.dump(self.deviceDict, outfile)

		return deviceData

	def login(self, userDetails):
		uri = "/login"
		url = self.url + uri
		response = requests.post(url, json = userDetails)

		#response from request 
		data = {}

		if response.status_code == 200:
			data = json.loads(response.text)
			userId = data['id']
			data['Timezone'] = localtimezone
			self.userDict[userId] = data
			self.catalog_cache[userId] = ({},data)
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---") 

		return json.dumps(data)

	def logOut(self, userId):
		self.userDict.pop(userId)
		self.catalog_cache.pop(userId)
		self.delValue(userId, self.bikeDict)
		
	def setBikeDetails(self, userId, bikeId):
		data = {}
		details = self.getBrokerDetails(bikeId)
		data['broker'] = details['broker']
		data['port_number'] = details['port_number']
		data['userId'] = userId
		data['url'] = details['url']
		bikeDetails = json.dumps(data)
		self.bikeDict[bikeId] = bikeDetails

		uri = "/setDetails"
		bikeurl = details['url'] + uri 
		response = requests.post(bikeurl, json = bikeDetails)

		#response from request
		if response.status_code == 200:
			pass
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---")

		return bikeDetails

	def getAllDevices(self, deviceType):
		#deviceType can be GPS, Speed, Heart Rate, Collision
		# return array of devices in a format -  a device is in format {'deviceId' : '', 'available_resources' : [], 'end_points' : []}
		with open('devices.json') as file:
			self.deviceDict = json.load(file)
			
		deviceEndPoints = []
		for key, value in self.deviceDict.items(): 
			valueDict = json.loads(value)
			if deviceType in valueDict['available_resources']:
				deviceEndPoints.extend(valueDict['end_points'])

		deviceDict = {}
		deviceDict[deviceType] = deviceEndPoints

		# return available endpoints - an end point is in format {'broker' : 'broker_url', 'topic' : topic details, 'port_number' : 1883}
		return json.dumps(deviceDict)


	def getEndPoints(self, userId, bikeId):
		#for UI
		data = json.loads(self.bikeDict[bikeId])
		bikeurl = data['url']
		uri = "/startTrip"
		bikeurl = bikeurl + uri
		response = requests.get(bikeurl)

		#response from request
		if response.status_code == 200:
			pass
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---")

		with open('devices.json') as file:
			self.deviceDict = json.load(file)
			
		deviceEndPoints = []
		for key, value in self.deviceDict.items(): 
			valueDict = value
			if valueDict['available_resources'][0] in ["Speed","HeartRate"]:
				endpoints = list(val for val in valueDict['end_points'] if val['type'] == "MQQT" and val['topic'].split('/')[0] == userId)
				endPoint = {}
				endPoint['Type'] = valueDict['available_resources'][0]
				endPoint['broker'] = endpoints[0]['broker']
				endPoint['port'] = endpoints[0]['port_number']
				endPoint['topic'] = endpoints[0]['topic']
				deviceEndPoints.append(endPoint)

		deviceDict = {}
		deviceDict['endPoints'] = deviceEndPoints

		# return available endpoints - an end point is in format {'broker' : 'broker_url', 'topic' : topic details, 'port_number' : 1883}
		return json.dumps(deviceDict)

	def getAllDevicesByUser(self, userID, deviceType):
		with open('devices.json') as file:
			self.deviceDict = json.load(file)
			
		deviceEndPoints = []
		devices = {}
		for key, value in self.deviceDict.items(): 
			valueDict = value
			if deviceType in self.SensorNameList:
				endpoints = list(val for val in valueDict['end_points'] if val['type'] == "MQQT" and val['topic'].split('/')[0] == userID)
				devices[valueDict['available_resources'][0]] = endpoints[0]['topic']
				devices['Broker'] = endpoints[0]['broker']
				devices['Port'] = endpoints[0]['port_number']


		
		return devices

	def microserviceGet(self,userID, deviceType):
		result = ""
		if bool(self.catalog_cache[userID][0]):
			result = json.dumps(self.catalog_cache[userID])
		else:
			devices = self.getAllDevicesByUser(userID, deviceType)
			user = self.catalog_cache[userID][1]
			self.catalog_cache[userID]= (devices,user)
			result = json.dumps(self.catalog_cache[userID])

		return result

	def endTrip(self, bikeId):
		result = ""
		uri = "/endTrip"
		url = json.loads(self.bikeDict[bikeId])['url'] + uri
	
		response = requests.get(url)

		if response.status_code == 200:
			pass
		elif response.status_code == 400:
			raise cherrypy.HTTPError(400,"---")
		
		return result

	# function to return key for any value 
	def delValue(self,val, my_dict): 
		for key, value in my_dict.items(): 
			if val == value:
				my_dict.pop(key)

	def usersGet(self):
		return json.dumps(list(self.catalog_cache.keys()))




		