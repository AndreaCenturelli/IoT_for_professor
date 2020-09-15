import requests
import  paho.mqtt.client as PahoMQTT
import json 
import time
import datetime
import matplotlib.pyplot as plt 
# from PerformanceCalculations import PerformanceHR
from WindowGenerator import WinGenerator
from SuperClass import SuperMicroserviceClass,ID_Finder
import msvcrt

class PerformanceSpeed(object):
    
    def __init__(self): ########## maybe put the ID instead of the Dictionary as args.
        global SessionDataSpeed
        
    def SaveSpeedvalues(self,ID: str,SpeedData: dict ):
        Speed=SpeedData['value']
        time=SpeedData['timestamp']
        SessionDataSpeed[ID]["Speed"].append(Speed)
        SessionDataSpeed[ID]["Time"].append(time)


class SpeedConnector(SuperMicroserviceClass):
    def __init__(self,clientID,address='http://127.0.0.1:8080'):
        if  "SessionDataSpeed" not in globals():
            global SessionDataSpeed
            SessionDataSpeed={}
        super().__init__(clientID,address)
        self.PerfSpeed=PerformanceSpeed()
        
    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        SpeedData=json.loads(msg.payload)
        ID=ID_Finder().find(msg.topic)
        if SpeedData!='finished':
            self.PerfSpeed.SaveSpeedvalues(ID,SpeedData) 
        elif  SpeedData=='finished':
            msg={}
            msg[ID]=SessionDataSpeed[ID]
            self._paho_mqtt.publish('microservice/Speed',json.dumps(msg),qos=2,retain=False)
            self._paho_mqtt.unsubscribe(SessionDataSpeed[ID]['Topic'])   
            del SessionDataSpeed[ID]
               
            
    def AddToSession(self, userID: str ,catalog_cache : tuple):
        tz=catalog_cache[1]["Timezone"]
        Broker=catalog_cache[0]["Broker"]
        Port=catalog_cache[0]["Port"]
        topic_name=catalog_cache[0]["Speed"]
        SessionDataSpeed[userID]= {"Speed":[],"Time":[],"Timezone":tz,"Topic":topic_name}
        self.StartSubscriber(topic_name,Broker,Port)
        
    def GetUsersInCache(self):
        usersID=json.loads(requests.get(self.address+'/Users').text)
        for userID in usersID:
            if userID not in SessionDataSpeed.keys():
                self.GetCache(userID)
        
    def GetCache(self,userID: str):
        url=self.address+'/Speed?UserID='+userID
        super().GetCache(userID,url)    
        
                
            
if __name__ == '__main__':
    conn=SpeedConnector('pcmio')
    i=0
    while 1:
       conn.GetUsersInCache()
       time.sleep(1)
       i+=1
       
    conn.stop()
           
