import requests
import  paho.mqtt.client as PahoMQTT
import json 
import re
import random, string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class SuperMicroserviceClass(object):
    def __init__(self,clientID,address='http://127.0.0.1:8080'):
        self.address=address   #### address of the bike catalog
        self.clientID=clientID
        self.broker="" ### message broker for mqtt
        self.port=0
        self._paho_mqtt = PahoMQTT.Client(self.clientID + get_random_string(3), True)
        self._paho_mqtt.on_message = self.myOnMessageReceived

    def GetCache(self,userID: str,url :str ):
        catalog_cache=json.loads(requests.get(url).text)
        if catalog_cache!={}:
            if catalog_cache[0] != {} and catalog_cache[1] != {}:
                self.AddToSession(userID,catalog_cache)
                
    def StartSubscriber(self,topic_name : str,Broker,Port):
        if self.broker!=Broker or self.port!=Port:
            self.broker=Broker
            self.port=Port
            self._paho_mqtt.connect(self.broker, self.port)
            self._paho_mqtt.loop_start()
        self._paho_mqtt.subscribe(topic_name, 2)
        print('StartSubscriber')
    
    def stop(self):
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()
        print('Microservice disconnected')
        

class ID_Finder(object):
    def __init__(self):
        self.regex=r'^(.*?)/'
    def find(self,string):
        try:
            return re.findall(self.regex,string)[0]
        except :
            pass ##error
    def find_where(self,string):
        query=r'where'
        try:
            if re.findall(query,string)[0]!=[]:
                return True
        except:
            return False
        
               
        