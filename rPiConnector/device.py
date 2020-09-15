import uuid 

class Device(object):

	def __init__(self, avResources):
		self.deviceId = str(uuid.uuid4())
		self.endPoints = []
		self.avResources = avResources
		
	def addEndPoint(self, endPoint):
		print(endPoint)
		self.endPoints.append(endPoint)