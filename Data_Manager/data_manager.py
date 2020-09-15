
import json
import cherrypy
from datetime import timezone, datetime
import pytz
import matplotlib.pyplot as plt
import gmplot
import paho.mqtt.client as PahoMQTT
import json
import time
import re
from mysql.connector import MySQLConnection, Error
import mysql
import os
utc = pytz.utc

d = {}
user_dict = {}

class db_connection(object):

    def __init__(self):
        self.user= 'root'
        self.password= 'password'
        self.host = '127.0.0.1'
        self.database = 'db_101'

    def call_procedure(self, procedure_name, args):
        """ Connect to MySQL database """
        try:
            print('Connecting to MySQL database.')
            conn = mysql.connector.connect(host=self.host,
                                         database=self.database,
                                         user=self.user,
                                         password=self.password,
                                         )

            if conn.is_connected():
                print('connection established.')
                try:
                    cursor = conn.cursor()
                    result = cursor.callproc(procedure_name, args)
                    conn.commit()
                except mysql.connector.errors.IntegrityError:
                    print('HTTP:409, Duplicate User ERROR')
                    raise cherrypy.HTTPError(409, "User Details are duplicated")
                cursor.close()
                conn.close()
                print("connection closed")
                return(result)
            else:
                print('connection failed.')
                return 0

        except Error as error:
            print(error)
            return 0

class HR_Speed_Plotter(object):
    def __init__(self, sensortype: str, SessionData: dict):  # sensortype='HeartRate' or 'Speed'
        self.sens = sensortype
        #print(self.sens)
        if self.sens == 'HeartRate':
            self.unit = '[BPM]'
        elif self.sens == 'Speed':
            self.unit = '[km/h]'
        else:
            raise OSError('Sensor not standard')
        self.SessionData = SessionData
        self.ID = list(self.SessionData.keys())[0]
        self.url = "http://127.0.0.1:1350/Plots"

    def PlotData(self):
        self.ID = list(self.SessionData.keys())[0]
        return self.ProduceFigure()

    def ProduceFigure(self):
        date, StartHourMin = self.timestamp2elapsed()
        fig = plt.figure(num=None, figsize=(30, 15), dpi=80, facecolor='w', edgecolor='k')
        plt.plot(self.SessionData[self.ID]["Time"], self.SessionData[self.ID][self.sens], marker='.')
        plt.title(f'Training of {date} \n Started at {StartHourMin} ', size='30')
        plt.xticks(rotation=45)
        plt.xlabel("Time [hour:min:sec]")
        plt.ylabel(f"{self.sens} [BPM]")
        plt.grid(b=True)
        ax = plt.gca()
        ax.tick_params(axis='both', which='major', labelsize=15)
        my_path = os.getcwd()
        plotName = str(self.sens)+str('_')+ self.ID + str('_')+ str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
        address = my_path + "\\Plots\\" + plotName + ".png"
        plt.savefig(address)
        url = self.url + "/" + plotName
        return url  ### Could save the figure from the function.
        #### It prints the figure in the console.

    def timestamp2elapsed(self):
        ### transforms the timestamps for each value in seconds between them.
        ### also returns the starting hours,mins,and date to plot on PlotHRvsTime
        tz = pytz.timezone(self.SessionData[self.ID]["Timezone"])
        start_time = self.SessionData[self.ID]["Time"][0]
        start_time = datetime.strptime(start_time, "%b %d %Y %H:%M:%S %Z")
        date = start_time.strftime("%B %d, %Y")
        StartHourMin = start_time.replace(tzinfo=timezone.utc).astimezone(tz=tz).strftime('%H:%M')
        ### from here on it converts from timestamp to a string <Hour>:<Min>:<Sex>
        datetimes = list(map(lambda x: datetime.strptime(x, "%b %d %Y %H:%M:%S %Z"), self.SessionData[self.ID]["Time"]))
        elapsed = list(map(lambda x: divmod((x - start_time).seconds, 60), datetimes))
        elapsed = list(
            map(lambda x: str(divmod(x[0], 60)[0]).zfill(2) + ":" + str(x[0]).zfill(2) + ":" + str(x[1]).zfill(2),
                elapsed))
        ##### It doesn't consider the microseconds, so it rounds badly
        self.SessionData[self.ID]["Time"] = elapsed
        return date, StartHourMin

    def Min(self):  # don't use Min for speed
        return round(min(self.SessionData[self.ID][self.sens]))

    def Max(self):
        return round(max(self.SessionData[self.ID][self.sens]))

    def Avg(self):
        return round(sum(self.SessionData[self.ID][self.sens]) / len(self.SessionData[self.ID][self.sens]))


class GPS_plotter(object):
    def __init__(self, SessionData: dict):
        self.SessionData = SessionData
        self.ID = list(SessionData.keys())[0]
        self.url = "http://127.0.0.1:1350/GPS"

    def ProduceMap(self):
        max_lat = max(self.SessionData[self.ID]["Latitude"])
        min_lat = min(self.SessionData[self.ID]["Latitude"])
        max_long = max(self.SessionData[self.ID]["Longitude"])
        min_long = min(self.SessionData[self.ID]["Longitude"])
        center_long = (max_long + min_long) / 2
        center_lat = (max_lat + min_lat) / 2
        mappa = gmplot.GoogleMapPlotter(center_lat, center_long, 12)
        mappa.scatter(lats=self.SessionData[self.ID]["Latitude"],
                      lngs=self.SessionData[self.ID]["Longitude"], size=40, marker=False)
        return mappa  ### returns a gmplot object. Either save it or send it to the database

    def SaveMap(self):
        mappa = self.ProduceMap()
        date = datetime.strptime(self.SessionData[self.ID]["Time"][0], "%b %d %Y %H:%M:%S %Z")
        my_path = os.getcwd()
        name = 'GPS' + str('_') + self.ID + str('_') + str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
        address = my_path + "\\Plots\\" + name + ".html"
#        address = "\\GPS_Plots\\" + self.ID + str(datetime.strftime(date, "%d_%m_%Y")) + ".html"
        mappa.draw(address)
        url = self.url + "/" + name
        return url

class User(object):
    def __init__(self):
        self.id = -1
        self.hr_avg = -1
        self.hr_max = -1
        self.hr_min = -1
        self.hr_plot = -1
        self.speed_max = -1
        self.speed_avg = -1
        self.speed_plot = -1
        self.gps_plot = -1

class Client(object):
    def __init__(self, clientName, portNumber, broker):
        self.clientName = clientName
        self._paho_mqtt = PahoMQTT.Client(self.clientName, True)
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
        self.broker = broker
        self.portNumber = portNumber

    def start(self):
        self._paho_mqtt.connect(self.broker, self.portNumber)
        self._paho_mqtt.loop_start()

    def MySubscribe(self, topic: str):
        self._paho_mqtt.subscribe(topic, qos=2)
        print(f'Subscribed to {topic}')

    def MyUnsubscribe(self, topic: str):
        self._paho_mqtt.unsubscribe(topic)
        print(f'Unsubscribed from {topic}')

    def myOnConnect(self, paho_mqtt, userData, flags, rc):
        print(f"COnnected to {self.broker} with result {rc}")

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        user_dict = {}
        sensortype = re.findall(r'([^\/]+$)', str(msg.topic))[0]
        SessionData = json.loads(msg.payload)
        print(str(sensortype)+' Message recieved')
        userid = list(SessionData.keys())[0]
        if sensortype == 'HeartRate':
            if userid in d.keys():
                user_dict = d[userid]
            hr = HR_Speed_Plotter(sensortype, SessionData)
            user_dict['id'] = userid
            user_dict['hr_avg'] = hr.Avg()
            user_dict['hr_max'] = hr.Max()
            user_dict['hr_min'] = hr.Min()
            user_dict['hr_plot'] = hr.PlotData()
            d[userid]=user_dict
            if len(d[userid]) == 9:
                db = db_connection()
                arg = []
                time_now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                arg.extend([user_dict['id'], time_now, user_dict['speed_avg'], user_dict['hr_avg'], user_dict['speed_max'], user_dict['hr_max'], user_dict['hr_min'], user_dict['hr_plot'], user_dict['speed_plot'], user_dict['gps_plot']])
                response = db.call_procedure(procedure_name='USP_SAVE_TRIP', args=arg)
                del d[userid]
        if sensortype == 'Speed':
            if userid in d.keys():
                user_dict = d[userid]
            speed = HR_Speed_Plotter(sensortype, SessionData)
            user_dict['speed_avg'] = speed.Avg()
            user_dict['speed_max'] = speed.Max()
            user_dict['speed_plot'] = speed.PlotData()
            d[userid]=user_dict
            if len(d[userid]) == 9:
                db = db_connection()
                arg = []
                time_now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                arg.extend([user_dict['id'], time_now, user_dict['speed_avg'], user_dict['hr_avg'], user_dict['speed_max'], user_dict['hr_max'], user_dict['hr_min'], user_dict['hr_plot'], user_dict['speed_plot'], user_dict['gps_plot']])
                response = db.call_procedure(procedure_name='USP_SAVE_TRIP', args=arg)
                del d[userid]
        if sensortype == 'GPS':
            if userid in d.keys():
                user_dict = d[userid]
            print('Gps msg recieved')
            gps = GPS_plotter(SessionData)
            user_dict['gps_plot'] = gps.SaveMap()
            if len(d[userid]) == 9:
                #ipdb.set_trace()
                db = db_connection()
                arg = []
                time_now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                arg.extend([user_dict['id'], time_now, user_dict['speed_avg'], user_dict['hr_avg'], user_dict['speed_max'], user_dict['hr_max'], user_dict['hr_min'], user_dict['hr_plot'], user_dict['speed_plot'], user_dict['gps_plot']])
                response = db.call_procedure(procedure_name='USP_SAVE_TRIP', args=arg)
                del d[userid]


    def stop(self):
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

class Data_Manager_API(object):
    exposed = True

    def __init__(self):
        pass

    def GET(self, *uri, **params):
        if len(uri)==1 and len(params.keys())==1:
            arg = list(params.values())
            db = db_connection()
            arg.append(0)
            if uri[0]=='getUser':
                response = db.call_procedure(procedure_name='USP_GET_USER',args=arg)
                return response[-1]
            if uri[0]=='getBike':
                response = db.call_procedure(procedure_name='USP_GET_BIKEDETAILS',args=arg)
                return response[-1]
            if uri[0]=='getTrips':
                response = db.call_procedure(procedure_name='USP_GET_TRIPS',args=arg)
                return response[-1]
            if uri[0]=='getTripbyID':
                response = db.call_procedure(procedure_name='USP_GET_TRIPS', args=arg)
                return response[-1]
            else:
                raise cherrypy.HTTPError(404, "Error message")
        else:
            raise cherrypy.HTTPError(404, "Error message")

    @cherrypy.expose
    def POST(self,*uri):
        body = cherrypy.request.body.read()
        if len(uri)==1 and len(body)!=0:
            json_body = json.loads(body.decode('utf-8'))
            arg = list(json_body.values())
            arg.append(0)
            db = db_connection()
            if uri[0]=='addUser':
                response = db.call_procedure(procedure_name='USP_SAVE_USER',args=arg)
                return response[-1]
            if uri[0] == 'login':
                response = db.call_procedure(procedure_name='USP_USER_LOGIN',args=arg)
                return response[-1]
            if uri[0] == 'updateUser':
                response = db.call_procedure(procedure_name='USP_UPDATE_USER', args=arg)
                return response[-1]
            else:
                raise cherrypy.HTTPError(404, "Error message")
        else:
            raise cherrypy.HTTPError(404, "Error message")

if __name__ == '__main__':

    mqtt_service = Client('Data_Manager_MQTT', 1883, "127.0.0.1")
    mqtt_service.start()
    mqtt_service.MySubscribe('microservice/GPS')
    mqtt_service.MySubscribe('microservice/HeartRate')
    mqtt_service.MySubscribe('microservice/Speed')

    conf = {
        '/':{
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            }
        }

    cherrypy.tree.mount(Data_Manager_API(),'/', conf)
    cherrypy.config.update({'server.socket_host':'127.0.0.1'})
    cherrypy.config.update({'server.socket_port': 8086})
    cherrypy.engine.start()
    cherrypy.engine.block()

