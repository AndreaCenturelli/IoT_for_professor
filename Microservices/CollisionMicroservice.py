import requests
import  paho.mqtt.client as PahoMQTT
import json 
import time
from SuperClass import SuperMicroserviceClass,ID_Finder
import random, string

   #########################################################################################################

class CollisionProtocol(object):
    def __init__(self):
        global SessionDataColl
        # pass 
            
    def SaveCollisionData(self, CollisionData, ID):   #### collision status is the msg.payload, ID is in the userdata
        status=CollisionData['Status']
        if SessionDataColl[ID]['Status']=='Ok' and status=='Accident':
            self.AccidentMessageGenerator(ID)
        elif SessionDataColl[ID]['Status']=='Accident' and status=='Ok':
            self.EverythinOkMessageGenerator(ID)
        SessionDataColl[ID]['Status']=status
        
    def SaveGPSForCollisionData (self,GPSdata,ID):
        lat=GPSdata['latitude']
        long=GPSdata['longitude']
        time=GPSdata['timestamp']
        LastLocation=(lat,long)
        SessionDataColl[ID]["LastLocation"]=LastLocation
        SessionDataColl[ID]["LastTime"]=time 
        
    def TelegramSender(self,bot_message,bot_chatID):
        bot_token = '1117736612:AAHf-Pq_glu5z1Oa6jrU4MGWFcOn4XHo1dw'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
       
    
    def FetchCoordinates(self,ID):
        reply=SessionDataColl[ID]["LastLocation"]
        if reply==():
           reply='error'
        return reply
    
    def FetchNamePronounTeleID(self,ID):
        name=SessionDataColl[ID]['name']
        TeleID=SessionDataColl[ID]['telegram_ID']
        if SessionDataColl[ID]["gender"]=="Male":
            pronoun="his"
        elif  SessionDataColl[ID]["gender"]=="Female":
            pronoun="her"
        else: 
            pronoun="her/his/its/zim/sie/em/ver/ter/em"
        return name,pronoun,TeleID
        
    def AccidentMessageGenerator(self,ID):
        name,pronoun,TeleID=self.FetchNamePronounTeleID(ID)
        reply=self.FetchCoordinates(ID)
        if reply=='error':
            my_message = f"{name} had an accident and the application couldn't get {pronoun} coordinates"
        elif type(reply)==tuple:
            my_message = f"{name} had an accident,{pronoun} coordinates are:LONG={reply[0]}, LAT={reply[1]}"
        self.TelegramSender(my_message,TeleID)
        
    def EverythinOkMessageGenerator(self,ID):
        name,pronoun,TeleID=self.FetchNamePronounTeleID(ID)
        my_message=f"Update: {name} is ok and back on the bike "
        self.TelegramSender(my_message,TeleID)
        
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class CatalogConnector(SuperMicroserviceClass):
    def __init__(self,clientID,address='http://127.0.0.1:8080'):
        ### 2 clients, one for the msgs from the gps topics,
        ### the the other for the msgs from the collision topic
        ### like this bc I need 2 different on_message callbacks
        if  "SessionDataColl" not in globals():
            global SessionDataColl
            SessionDataColl={}
        super().__init__(clientID,address)
        
        self._paho_mqtt_gps= PahoMQTT.Client(self.clientID+'gps'+ get_random_string(3), True) 
        self._paho_mqtt_gps.on_message=self.myOnMessageReceived_gps
        self.CollProt=CollisionProtocol()
        
    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        CollisionData=json.loads(msg.payload)
        ID=ID_Finder().find(msg.topic)
        if CollisionData!='finished':
            self.CollProt.SaveCollisionData(CollisionData, ID)
        elif CollisionData=='finished':
            try:
                self.paho_mqtt.unsubscribe(SessionDataColl[ID]["Topic"])
            except:
                ## already unsubscribed by gps
                pass
            del SessionDataColl[ID]
    
        
    
    def myOnMessageReceived_gps(self, paho_mqtt, userdata, msg):
         CollisionData=json.loads(msg.payload)
         ID=ID_Finder().find(msg.topic)
         if CollisionData!='finished':
             self.CollProt.SaveGPSForCollisionData(CollisionData,ID)
         elif CollisionData=='finished':
             self._paho_mqtt.unsubscribe(SessionDataColl[ID]["Topic_GPS"])
             try:
                 self._paho_mqtt.unsubscribe(SessionDataColl[ID]["Topic"])
             except:
                pass #already unsubscribed by collision
            
             del SessionDataColl[ID]
             
 
         
    # def StartSubscriber(self,topic_name : str, broker : str,port : int):
    def StartSubscriber(self,topic_name : str,topic_name_gps: str, Broker,Port):
        if self.broker!=Broker or self.port!=Port:
            self.broker=Broker
            self.port=Port
            self._paho_mqtt.connect(self.broker, self.port)
            self._paho_mqtt_gps.connect(self.broker, self.port)
            self._paho_mqtt.loop_start()
            self._paho_mqtt_gps.loop_start()
        self._paho_mqtt.subscribe(topic_name, 2)
        self._paho_mqtt_gps.subscribe(topic_name_gps,2) 

    def AddToSession(self,userID: str, catalog_cache : tuple):
        Name=catalog_cache[1]['name']
        Gender=catalog_cache[1]['gender']
        # Status=catalog_cache[key][1]['Status']
        Status='Ok'
        telegram_ID=catalog_cache[1]['telegram_ID_friend']
        topic_name=catalog_cache[0]['Collision']
        topic_name_gps=catalog_cache[0]['GPS']
        SessionDataColl[userID]={'LastLocation':(),'LastTime': '','Name': Name,
                                 'Gender':Gender,'Status':Status,'telegram_ID':telegram_ID,
                                 "Topic":topic_name,"Topic_GPS":topic_name_gps}
        
        Broker=catalog_cache[0]["Broker"]
        Port=catalog_cache[0]["Port"]
        self.StartSubscriber(topic_name,topic_name_gps,Broker,Port)
                    
    def GetUsersInCache(self):
        usersID=json.loads(requests.get(self.address+'/Users').text)
        for userID in usersID:
            if userID not in SessionDataColl.keys():
                self.GetCache(userID)
    
    def GetCache(self,userID: str):
        url=self.address+'/Collision?UserID='+userID
        super().GetCache(userID,url)
    
    def stop(self):
        super().stop()
        self._paho_mqtt_gps.loop_stop()
        self._paho_mqtt_gps.disconnect()
        

if __name__ == '__main__':
    conn=CatalogConnector('pcmio')

    i=0
    while 1:
        conn.GetUsersInCache()
        time.sleep(1)
        i+=1
       
    conn.stop()
   

    