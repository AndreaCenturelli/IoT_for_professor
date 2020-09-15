import paho.mqtt.client as PahoMQTT
import json
import time

class Client(object):
    def __init__(self, clientName, topic, portNumber, broker, device):
        self._paho_mqtt=PahoMQTT.Client(clientName,False)
        self._paho_mqtt.on_connect=self.myOnConnect
        self.topic=topic
        self.broker=broker
        self.device=device
        self.portNumber=portNumber 
        
    def start(self):
        self._paho_mqtt.connect(self.broker,self.portNumber)
        self._paho_mqtt.loop_start()
    
    def myOnConnect(self,paho_mqtt,userData,flags,rc):
        print(f"COnnected to {self.broker} with result {rc}")
        endPoint = {}
        endPoint['type'] = "MQQT"
        endPoint['broker'] = self.broker
        endPoint['topic'] = self.topic
        endPoint['port_number'] = self.portNumber
        self.device.addEndPoint(endPoint)      
    
    def myPublish(self,jsonMessage):
        self._paho_mqtt.publish(self.topic, jsonMessage)
        
        
    def stop(self):
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()



