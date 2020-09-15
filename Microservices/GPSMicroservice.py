import requests
import  paho.mqtt.client as PahoMQTT
import json 
import time
import datetime
import gmplot
# from PerformanceCalculations import GPSplotter
from SuperClass import SuperMicroserviceClass, ID_Finder

class GPSplotter(object):
    def __init__(self):
        global SessionDataGPS
    
    def SaveGPSvalues(self,ID: str,GPSdata : dict ):
        lat=GPSdata['latitude']
        long=GPSdata['longitude']
        time=GPSdata['timestamp']
        SessionDataGPS[ID]["Latitude"].append(lat)
        SessionDataGPS[ID]["Longitude"].append(long)
        SessionDataGPS[ID]["Time"].append(time)

        
   #########################################################################################################

class GPSConnector(SuperMicroserviceClass):
    def __init__(self,clientID,address='http://127.0.0.1:8080'):
        if  "SessionDataGPS" not in globals():
            global SessionDataGPS
            SessionDataGPS={}
        super().__init__(clientID,address)
        self.GPSplot=GPSplotter()
        
    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        GPSData=json.loads(msg.payload)
        ID=ID_Finder().find(msg.topic)
    
        if GPSData!='finished':
            self.GPSplot.SaveGPSvalues(ID,GPSData)
        elif  GPSData=='finished':
            msg={}
            msg[ID]=SessionDataGPS[ID]
            self._paho_mqtt.publish('microservice/GPS',json.dumps(msg),qos=2,retain=False)
            self._paho_mqtt.unsubscribe(SessionDataGPS[ID]["Topic"])
            del SessionDataGPS[ID]
  
    def AddToSession(self, userID: str ,catalog_cache : tuple):
        tz=catalog_cache[1]["Timezone"]
        topic_name=catalog_cache[0]["GPS"]

        SessionDataGPS[userID]={"Latitude":[],"Longitude":[],"Time":[],"Timezone":tz,"Topic":topic_name}
        Broker=catalog_cache[0]["Broker"]
        Port=catalog_cache[0]["Port"]
        
        self.StartSubscriber(topic_name,Broker,Port)
        
       
    def GetUsersInCache(self):
        usersID=json.loads(requests.get(self.address+'/Users').text)
        for userID in usersID:
            if userID not in SessionDataGPS.keys():
                self.GetCache(userID)
        
    
    def GetCache(self,userID: str):
        url=self.address+'/GPS?UserID='+userID
        super().GetCache(userID,url)

            
            
if __name__ == '__main__':
    conn=GPSConnector('pcmio')
    i=0
    while 1:
        conn.GetUsersInCache()
        time.sleep(1)
        i+=1
       
    conn.stop()