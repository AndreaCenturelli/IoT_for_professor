import requests
import  paho.mqtt.client as PahoMQTT
import json 
import time
import datetime
from datetime import timezone
import matplotlib.pyplot as plt 
# from PerformanceCalculations import PerformanceHR
from WindowGenerator import WinGenerator
from SuperClass import SuperMicroserviceClass,ID_Finder
import pytz

class PerformanceHR(object):
    
    def __init__(self): ########## maybe put the ID instead of the Dictionary as args.
        global SessionDataHR
      
    def SaveHRvalues(self,ID: str,HRdata: dict ):
        HR=HRdata['value']
        time=HRdata['timestamp']
        SessionDataHR[ID]["HeartRate"].append(HR)
        SessionDataHR[ID]["Time"].append(time) 
        
        
class HeartRateConnector(SuperMicroserviceClass):
    def __init__(self,clientID,address='http://127.0.0.1:8080'):
        if  "SessionDataHR" not in globals():
             global SessionDataHR
             SessionDataHR={}
        super().__init__(clientID,address)
        self.PerfHR=PerformanceHR() 

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        HRData=json.loads(msg.payload)
        ID=ID_Finder().find(msg.topic)
        if HRData!='finished':
            self.PerfHR.SaveHRvalues(ID,HRData)
            
        elif  HRData=='finished':
            msg={}
            msg[ID]=SessionDataHR[ID]
            self._paho_mqtt.publish('microservice/HeartRate',json.dumps(msg),qos=2,retain=False)
            self._paho_mqtt.unsubscribe(SessionDataHR[ID]['Topic'])
            del SessionDataHR[ID]
        else :
            raise OSError('Message not standard')

    def AddToSession(self, userID: str ,catalog_cache : tuple):
        Broker=catalog_cache[0]["Broker"]
        Port=catalog_cache[0]["Port"]
        min_window,max_window=WinGenerator(catalog_cache[1]).Window()
        
        json_msg=json.dumps((min_window,max_window))
        requests.post(self.address+'/HRWindow?UserID='+userID,json=json_msg)
        topic_name=catalog_cache[0]["HeartRate"]
        tz=catalog_cache[1]["Timezone"]
        SessionDataHR[userID]= {"Window":(min_window,max_window),"Timezone":tz,"HeartRate":[],"Time":[],"Topic": topic_name}
        
        self.StartSubscriber(topic_name,Broker,Port)
        
    def GetUsersInCache(self):
        usersID=json.loads(requests.get(self.address+'/Users').text)
        for userID in usersID:
            if userID not in SessionDataHR.keys():
                self.GetCache(userID)
        
    def GetCache(self,userID: str):
        url=self.address+'/HeartRate?UserID='+userID
        super().GetCache(userID,url)
                

            
if __name__ == '__main__':
    conn=HeartRateConnector('pcmio')

    i=0
    while 1:
        conn.GetUsersInCache()
        time.sleep(1)
        i+=1
       
    conn.stop()
   