import requests
import  paho.mqtt.client as PahoMQTT
import json 
import time
from SuperClass import SuperMicroserviceClass
from SuperClass import ID_Finder
import random, string
   #########################################################################################################


class AntiTheftProtocol(object):
    def __init__(self):
        global SessionDataAT
        self.TryAgain=3 #shouldn't happen in the real case, but when u 
        #simulate quickly u might get that a speed>3 is sent before a GPS value
        #hence u need to send the msg again (3 tries, after that it gives up)
        
    def SaveGPSForAT(self,GPSdata,ID):
        lat=GPSdata['latitude']
        long=GPSdata['longitude']
        time=GPSdata['timestamp']
        if SessionDataAT[ID]["FirstLocation"]!=():
            LastLocation=(lat,long)
            SessionDataAT[ID]["LastLocation"]=LastLocation
            SessionDataAT[ID]["LastTime"]=time 
        elif SessionDataAT[ID]["FirstLocation"]==():
            FirstLocation=(lat,long)
            SessionDataAT[ID]["FirstLocation"]=FirstLocation
        else:
            pass ## error
            
    def GetUpdates(self):
        token='1194042903:AAHsCJMW8wiWvPQfrSryNUtCTd7MQLXaqj0'
        url='https://api.telegram.org/bot'+ token+'/getUpdates'
        response=json.loads(requests.get(url).text)
        TeleID=response['result'][-1]['message']['from']['id']
        text=response['result'][-1]['message']['text']
        ID=ID_Finder().find(text)
        if ID!=None:
            if SessionDataAT[ID]['telegram_ID']==TeleID:
                _,last_gps=self.FetchCoordinates(ID)
                if last_gps!=():
                    bot_message=f'Your bike is here: LONG: {last_gps[0]}, LAT:{last_gps[1]}'
                else:
                    bot_message="We couldn't get the coordinates, your bike is gone mate"
            else: 
                bot_message="Your user ID doesn't match our database informations"
        elif ID_Finder().find_where(text)==True: #recognizes 'where's my bike', 'where my bike at' etc
            bot_message='Insert your user ID (3 letters and 3 numbers)'
        else:
            bot_message='Command not recognized'
        send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + str(TeleID) + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_text).json()   
        
    def TelegramSender(self,bot_message,bot_chatID):
        bot_token = '1194042903:AAHsCJMW8wiWvPQfrSryNUtCTd7MQLXaqj0'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        return response.json()
    
    def TheftCheck(self,ID):
        last_gps=SessionDataAT[ID]["LastLocation"]
        first_gps=SessionDataAT[ID]['FirstLocation']
        if SessionDataAT[ID]["Stolen"]==False and first_gps!=last_gps: 
            self.AlarmMessageGenerator(ID,last_gps)
            if self.TryAgain==0: #either u get the gps data or u abandon hope after 3 tries
                SessionDataAT[ID]["Stolen"]=True 
                self.TryAgain=3
                
            
    def FetchTeleID(self,ID):
        TeleID=SessionDataAT[ID]['telegram_ID']
        return TeleID
     
    def SendStartAT(self,ID):
        try:
            TeleID=self.FetchTeleID(ID)
            my_message='The anti-theft mode is now active on your bike'
            self.TelegramSender(my_message,TeleID)
        except:
             pass ##errror 
    
    def SendStopAT(self,ID):
        try:
            TeleID=self.FetchTeleID(ID)
            my_message='The anti-theft mode is now deactivated on your bike'
            self.TelegramSender(my_message,TeleID)
        except:
            pass ##errror
        
    def AlarmMessageGenerator(self,ID,LastLocation):
        TeleID=self.FetchTeleID(ID)
        if LastLocation==():
            my_message = f"Your bike has been stolen, we can't get the coordinates right now"
            self.TryAgain-=1
        else: 
            my_message = f"Your bike has been stolen here: LONG={LastLocation[0]}, LAT={LastLocation[1]}"
            self.TryAgain=0
        self.TelegramSender(my_message,TeleID)
    
        
########################################################################################################################àà
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
class AntiTheftConnector(SuperMicroserviceClass):
    def __init__(self,clientID,address='http://127.0.0.1:8080'):
        ### 2 clients, one for the msgs from the gps topics,
        ### the the other for the msgs from the collision topic
        ### like this bc I need 2 different on_message callbacks
        if  "SessionDataAT" not in globals():
            global SessionDataAT
            SessionDataAT={}
        self.address=address   #### address of the bike catalog
        self.clientID=clientID
        self.broker="" ### message broker for mqtt
        self.port=0
        self._paho_mqtt = PahoMQTT.Client(self.clientID, False)
        self._paho_mqtt.on_message = self.myOnMessageReceived
        self._paho_mqtt_gps= PahoMQTT.Client(self.clientID+'gps'+ get_random_string(3), False) 
        self._paho_mqtt_gps.on_message=self.myOnMessageReceived_gps
        self._paho_mqtt_speed= PahoMQTT.Client(self.clientID+'speed'+ get_random_string(3), False) 
        self._paho_mqtt_speed.on_message=self.myOnMessageReceived_speed
        self.ATProt=AntiTheftProtocol()
        
    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
         anti_theft_status=json.loads(msg.payload)
         ID=ID_Finder().find(msg.topic)
         self.StatusCheck(anti_theft_status,ID)
    
    def myOnMessageReceived_gps(self, paho_mqtt, userdata, msg):
        GPSData=json.loads(msg.payload)
        ID=ID_Finder().find(msg.topic)
        if GPSData!='finished':
            self.ATProt.SaveGPSForAT(GPSData, ID)
        elif GPSData=='finished':
            
            try:
                self._paho_mqtt.unsubscribe(SessionDataAT[ID]["Topic_GPS"])
                self._paho_mqtt.unsubscribe(SessionDataAT[ID]["Topic_Speed"])
            except:
                pass # already deleted
    
    def myOnMessageReceived_speed(self, paho_mqtt, userdata, msg):
        SpeedData=json.loads(msg.payload)
        ID=ID_Finder().find(msg.topic)
        if SpeedData!='finished':
            if SpeedData['value']>3:
                self.ATProt.TheftCheck(ID)
            else:
                pass ## not stolen 
        elif SpeedData=='finished':
            try:
                self._paho_mqtt.unsubscribe(SessionDataAT[ID]["Topic_GPS"])
                self._paho_mqtt.unsubscribe(SessionDataAT[ID]["Topic_Speed"])
            except:
                pass # already deleted
        
    def StatusCheck(self,ATData,ID):
        new_status=ATData['Status']
        old_status=SessionDataAT[ID]['Status']  
        if new_status==True and old_status==False:
            self.StartSubscriberGpsSpeed(ID)
            self.ATProt.SendStartAT(ID)
        elif new_status==False and old_status==True:
            self.UnsubscribeGpsSpeed(ID)
            self.ATProt.SendStopAT(ID)
        SessionDataAT[ID]['Status']=new_status

    def StartSubscriber(self,topic_name : str,topic_name_gps: str,topic_name_speed:str, Broker,Port):
        if self.broker!=Broker or self.port!=Port:
            self.broker=Broker
            self.port=Port
            self._paho_mqtt.connect(self.broker, self.port)
            self._paho_mqtt.loop_start()
            self._paho_mqtt_gps.connect(self.broker, self.port)
            self._paho_mqtt_gps.loop_start()
            self._paho_mqtt_speed.connect(self.broker, self.port)
            self._paho_mqtt_speed.loop_start()
        self._paho_mqtt.subscribe(topic_name, 2)
    
    def UnsubscribeAntiTheft(self,ID): #technically never called, practically u have to
        topic_name=SessionDataAT[ID]['Topic']
        self._paho_mqtt.unsubscribe(topic_name)
        try:
            self.UnsubscribeGpsSpeed(ID)
        except:
            pass #already unsubscribed by the end of GPS and speed data
        
        
    def StartSubscriberGpsSpeed(self,ID):
        topic_name_gps=SessionDataAT[ID]['Topic_GPS']
        topic_name_speed=SessionDataAT[ID]['Topic_Speed']
        self._paho_mqtt_gps.subscribe(topic_name_gps,2)
        self._paho_mqtt_speed.subscribe(topic_name_speed,2) 
    
    def UnsubscribeGpsSpeed(self,ID):
        topic_name_gps=SessionDataAT[ID]['Topic_GPS']
        topic_name_speed=SessionDataAT[ID]['Topic_Speed']
        self._paho_mqtt_gps.unsubscribe(topic_name_gps)
        self._paho_mqtt_speed.unsubscribe(topic_name_speed) 

    def AddToSession(self,userID: str, catalog_cache : tuple):
        topic_name=catalog_cache[0]['AntiTheft']
        topic_name_gps=catalog_cache[0]['GPS']
        topic_name_speed=catalog_cache[0]['Speed']
        
        telegram_ID=catalog_cache[1]['telegram_ID_user']
        SessionDataAT[userID]={'Status':False ,'Stolen':False
                               ,'Topic_GPS':topic_name_gps,
                               'Topic':topic_name,
                                 'Topic_Speed':topic_name_speed,'telegram_ID':telegram_ID,
                                 'FirstLocation':(),
                                 'LastLocation':(), 'LastTime':'','Speed':0}
        Broker=catalog_cache[0]["Broker"]
        Port=catalog_cache[0]["Port"]
        self.StartSubscriber(topic_name,topic_name_gps,topic_name_speed,Broker,Port)
                    
    def GetUsersInCache(self):
        usersID=json.loads(requests.get(self.address+'/Users').text)
        for userID in usersID:
            if userID not in SessionDataAT.keys():
                self.GetCache(userID)
    
    def GetCache(self,userID: str):
        url=self.address+'/AntiTheft?UserID='+userID
        super().GetCache(userID,url)

        

if __name__ == '__main__':
    conn=AntiTheftConnector('pcmio')

    i=0
    while 1:
        conn.GetUsersInCache()
        time.sleep(1)
        i+=1
    conn.UnsubscribeAntiTheft('abc123') #shouldn't be there, but it's not to recieve
    #the past messages. If I don't put it it doesn't unsubscribe
    conn.stop()