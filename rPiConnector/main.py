import requests
import serial
from mqqtClient import Client
from rPiConnector import Connector
from device import Device
from connectorREST import ConnectorRest
import cherrypy
import json
from datetime import datetime
import pytz
utc = pytz.utc
import time


def makeSerialConnections(ports):
    serialConnections = []
    count = 0
    for port in ports:
        ser = serial.Serial(
            port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
            )

        serialConnections.append(ser)

        if serialConnections[count].isOpen():
            print(serialConnections[count].name + 'is open..')
        count = count + 1
        
    return serialConnections
    
if __name__=="__main__":
    ports = ['COM6', 'COM8', 'COM10', 'COM12']

    serialConnections = makeSerialConnections(ports)

    connector = Connector()

    conf = {
    '/' : {
        'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
        'tool.session.on' : True
        }
      }


    connectorRest = ConnectorRest(connector)

    cherrypy.tree.mount(connectorRest,'/',conf)
    cherrypy.server.unsubscribe()
    server1 = cherrypy._cpserver.Server()
    server1.socket_port=3141
    server1._socket_host="127.0.0.1"
    server1.thread_pool=2
    server1.subscribe()

    cherrypy.engine.start()

    broker = ''
    userId = ''
    portNumber = 0

    while broker == '':
      broker = connector.broker
      userId = connector.userId
      portNumber = connector.portNumber

    gpsTopic = userId + '/GPS'
    gpsDevice = Device(['GPS'])
    gpsClient = Client('gpsClient', gpsTopic, portNumber, broker, gpsDevice)

    collisionTopic = userId + '/Collision'
    collisionDevice = Device(['Collision'])
    collisionClient = Client('collisionClient', collisionTopic, portNumber, broker, collisionDevice)

    speedTopic = userId + '/Speed'
    speedDevice = Device(['Speed'])
    speedClient = Client('speedClient', speedTopic, portNumber, broker, speedDevice)

    heartRateTopic = userId + '/Heartrate'
    heartRateDevice = Device(['HeartRate'])
    heartRateClient = Client('heartRateClient', heartRateTopic,portNumber,broker, heartRateDevice)

    antiTheftTopic = userId + '/AntiTheft'
    antiTheftDevice = Device(['AntiTheft'])
    antiTheftClient = Client('antiTheftClient', antiTheftTopic,portNumber,broker, antiTheftDevice)

    gpsClient.start()

    collisionClient.start()
    
    speedClient.start()
    
    heartRateClient.start()

    antiTheftClient.start()
    

    time.sleep(1)

    connector.registerDevice(gpsDevice)
    connector.registerDevice(collisionDevice)
    connector.registerDevice(speedDevice)
    connector.registerDevice(heartRateDevice)
    connector.registerDevice(antiTheftDevice)

    flag = False

    while 1:
      gpsdata = serialConnections[0].readline().decode('utf-8')
      collisionData = serialConnections[1].readline().decode('utf-8')
      speedData = serialConnections[2].readline().decode('utf-8')
      heartRateData = serialConnections[3].readline().decode('utf-8')
      antiTheftdata = {}
      antiTheftdata['type'] = "AT"
      antiTheftdata['timestamp'] = datetime.now(utc).strftime("%b %d %Y %H:%M:%S %Z")
      antiTheftdata['Status'] = not connectorRest.tripStatus
      antTheftresult = json.dumps(antiTheftdata)

      if len(gpsdata) !=0 and connectorRest.tripStatus:
        gpsClient.myPublish(gpsdata)
        flag = False
       
      if len(collisionData) !=0 and connectorRest.tripStatus:
        collisionClient.myPublish(collisionData)
        flag = False
        
      if len(heartRateData) !=0 and connectorRest.tripStatus:
        heartRateClient.myPublish(heartRateData)
        flag = False
        
      if len(speedData) !=0 and connectorRest.tripStatus:
        speedClient.myPublish(speedData)
        flag = False     

      if not connectorRest.tripStatus and not flag:
        gpsClient.myPublish(json.dumps('finished'))
        time.sleep(0.5)
        collisionClient.myPublish(json.dumps('finished'))
        time.sleep(0.5)
        heartRateClient.myPublish(json.dumps('finished'))
        time.sleep(0.5)
        speedClient.myPublish(json.dumps('finished'))
        flag = True

      antiTheftClient.myPublish(antTheftresult)
      time.sleep(0.5)

    cherrypy.engine.block()

