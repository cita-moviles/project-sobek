__author__ = 'admin'

import json
import urllib2
import datetime
import pytz
import logging
from datetime import timedelta
from dateutil.parser import parse
import requests
from HexConverter import HexConverter
import re
currentDate = None


def instantiate_date():
    global currentDate
    currentDate = datetime.datetime.today()


def instantiate_cfg():
    global area_cfg
    area_cfg = 'ROK'


#10
class Sensor:
    def __init__(self, message, field_id, area_id):
        """
        Pos[0] = 'S' or 'C' Start of message
        Pos[1] = Sensor ID
        Pos[2:4] = SM1
        Pos[4:6] = SM2
        Pos[6:8] = SM3
        Pos[8] = Battery
        Pos[9] = RSSI
        Pos[10] = Error code
        """
        if message[0] == 'S':
            self.sensor_id = int(field_id+area_id+message[1])
            self.sensor_hl1 = float(message[2:4]) # + "." + message[11])
            self.sensor_hl2 = float(message[4:6]) #+ "." + message[14])
            self.sensor_hl3 = float(message[6:8]) #+ "." + message[17])
        elif message[0] == 'C':
            self.sensor_id = int(field_id+area_id+'0')
            self.sensor_hl1 = float(message[2:4])
            self.sensor_hl2 = 0
            self.sensor_hl3 = 0
        #print self.sensor_id
        self.sensor_status = 0
        self.sensor_temperature = 0
        self.sensor_x_position = 0
        self.sensor_y_position = 0
        self.sensor_user_define1 = ' '
        self.sensor_user_define2 = ' '
        global currentDate
        self.sensor_date_received = str(currentDate)
        self.fk_area = " "
        self.sensor_name = " "
        self.get_from_server(field_id+area_id)
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/" + str(self.sensor_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        try:
            result = urllib2.urlopen(request, self.to_json())
        except urllib2.HTTPError, ex:
            print('Server error response')
        pass
    def get_from_server(self, id):
        request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/" + str(self.sensor_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'
        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            self.fk_area = "http://riego.chi.itesm.mx/Crop_Area/" + id + "/"
            self.sensor_name = result2['sensor_name']
        except urllib2.HTTPError:
            print('There was an error retrieving server info')
        pass


#20
class Valve:
    def __init__(self, message, field_id, area_id):
        """
        Pos[0] = 'A' Start of message
        Pos[1] = Valve ID
        Pos[2] = Valve Status
        Pos[3:5] = Flow
        Pos[5] = Battery
        Pos[6] = RSSI
        Pos[7] = Error code
        """
        self.valve_id = int(field_id+area_id+message[1])
        self.valve_status = int(message[2])
        self.valve_flow = int(message[3:5])
        self.valve_pressure = 0
        self.valve_limit = 0
        self.valve_ideal = 0
        """
        comma = message.index(',')
        if (comma is not None) and comma == 19:
            self.valve_user_define1 = ' '
            self.valve_user_define2 = ' '
        else:
            self.valve_user_define1 = message[19: comma]
            terminator = message.index("#")
            if (comma + 1) == terminator:
                self.valve_user_define2 = ' '
            else:
                self.valve_user_define2 = message[comma + 1: terminator]
        """

        global currentDate
        self.valve_date_received = str(currentDate)
        #self.limit = int(message[21:26])

        self.fk_area = " "
        self.valve_name = " "
        self.get_from_server(field_id+area_id)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Valve/" + str(self.valve_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print "---http://riego.chi.itesm.mx/Valve/" + str(self.valve_id) + "/"
        print self.to_json()
        try:
            result = urllib2.urlopen(request, self.to_json())
        except urllib2.HTTPError, ex:
            print('Server error response')
        pass

    def get_from_server(self, id):
        request = urllib2.Request("http://riego.chi.itesm.mx/Valve/" + str(self.valve_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'
        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            self.fk_area = "http://riego.chi.itesm.mx/Crop_Area/" + id + "/"
            self.valve_name = result2['valve_name']
        except urllib2.HTTPError:
            print('There was an error retrieving server info')
        pass

#30
class Crop_Area:
    def __init__(self, message, field_id, station_ev):
        """
          Pos[0] = 'R' Start of message
          Pos[1] = Area ID
          Pos[2] = Number of sensors
        """
        self.area_id = int(field_id+message[1])
        self.area_ev = station_ev
        self.area_x_position = 0
        self.area_y_position = 0
        self.area_user_define1 = ' '
        self.area_user_define2 = ' '
        self.fk_farm_field = " "
        self.fk_crop = " "
        self.area_name = " "
        self.area_description = " "
        self.get_name_from_server(field_id)

        global currentDate
        self.area_date_received = str(currentDate)
        global area_cfg
        area_cfg = self.get_from_server(field_id)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        try:
            result = urllib2.urlopen(request, self.to_json())
        except urllib2.HTTPError, ex:
            print('Server error response')
        pass


    def get_name_from_server(self, id):
        request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'
        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            self.area_name = result2['area_name']
            self.area_description = result2['area_description']
            self.fk_crop = result2['fk_crop']
            self.fk_farm_field =  "http://riego.chi.itesm.mx/Farm_Field/" + id + "/"
        except urllib2.HTTPError, ex:
            #logging.exception("Something awful happened!")
            print('Area names not found ' + str(self.area_id))
            pass

    def get_from_server(self, field_id):
        local_area_cfg = ''
        request = urllib2.Request("http://riego.chi.itesm.mx/Area_Configuration/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'

        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            print "Server Config: " + result2['area_configuration']
            if result2['area_configuration'] == "ROK":
                local_area_cfg += result2['area_configuration'][2] + '0'*6
            else:
                data = result2['area_configuration']
                global config_mode
                config_mode = True
                str_field_id = data[0:2]
                str_area_id = data[2]
                str_mode = data[3]
                local_area_cfg += str_area_id
                if str_mode == '1':
                    state = data[4]
                    local_area_cfg += state
                elif str_mode == '2':
                    auto_data = data[4:]
                    min_data = auto_data.split('#')[0]
                    max_data = auto_data.split('#')[1]
                    local_area_cfg += min_data + max_data
                elif str_mode == '3':
                    timer_data = data[4:]
                    days = timer_data.split['#'][0]
                    time = timer_data.split['#'][1]
                    start = time.split['#'][0]
                    duration = time.split['#'][1]
                    local_area_cfg += days + start + duration
        except urllib2.HTTPError, ex:
            #logging.exception("Something awful happened!")
            print('Area configuration not found ' + str(self.area_id))
        return local_area_cfg

    def normalize_cfg(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Area_Configuration/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        try:
            rok = {"area_id": self.area_id, "area_configuration": "ROK"}
            rok_json = json.dumps(rok, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            result = urllib2.urlopen(request,rok_json)
            pass
        except urllib2.HTTPError, ex:
            print('Area config not found!')
            pass

#40
class Weather_Station:
    def __init__(self, message, field_id):
        """
        Pos[0] = 'W' Start of message
        Pos[1] = Weather node ID
        Pos[2:4] = Radiation
        Pos[4:6] = Humidity
        Pos[6:8] = Temperature
        Pos[8:10] = Wind
        Pos[10:12] = Rain
        Pos[12:14] = Eto
        Pos[14] = Battery
        Pos[15] = RSSI
        Pos[16] = Error code
        """
        """
        self.station_id = int(field_id+message[1])
        self.station_name = " "
        self.station_status = int(message[14])
        self.station_relative_humidity = float(message[4:6]) # + '.' + message[11])
        self.station_temperature = float(message[6:8]) # + '.' + message[15])
        self.station_wind_speed = float(message[8:10]) # + '.' + message[18:19])
        self.station_solar_radiation = int(message[2:4])
        self.station_ev = float(message[12:14])"""
        msg = message.split('#')
        self.station_id = int(field_id+msg[0][1])
        self.station_name = " "
        self.station_status = int(msg[9])
        self.station_relative_humidity = float(msg[2])
        self.station_temperature = float(msg[3])
        self.station_wind_speed = float(msg[4])
        self.station_solar_radiation = int(msg[1])
        self.station_ev = float(msg[6])
        self.station_user_define1 = str(msg[5])
        self.station_user_define2 = str(msg[9])

        global currentDate
        self.station_date_received = str(currentDate)
        self.fk_farm_field = " "
        self.station_name = " "
        self.get_from_server(field_id)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Weather_Station/" + str(self.station_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        try:
            result = urllib2.urlopen(request, self.to_json())
        except urllib2.HTTPError, ex:
            print('Server error response')
        pass

    def get_from_server(self, id):
        request = urllib2.Request("http://riego.chi.itesm.mx/Weather_Station/" + str(self.station_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'

        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            self.fk_farm_field = "http://riego.chi.itesm.mx/Farm_Field/" + id + "/"
            self.station_name = result2['station_name']
        except urllib2.HTTPError, ex:
            print('Field ID not found ' + str(self.station_id))
        pass



#50
class Farm_Field:
    def __init__(self, message):
        """ Class that process and creates objects in order to be uploaded to the server
          Pos[0] = ! Start of message
          Pos[1:2] = header
          Pos[3:7] = Farm_Field's ID
          Pos[7:9] = Signal
          Pos[9:11] = Latitude
          Pos[11] = Longitude
          Pos[12:16] = User_define1
          Pos[16] = User_define2
          Pos[-1] = #End of message
          #!50000101289600679420718-106.0925920028.6701220,0
        """
        self.field_id = int(message[3:7])
        self.field_imei = int(message[7:22])
        self.field_signal = int(message[22:24])
        self.field_latitude = float(message[24:35])
        self.field_longitude = float(message[35:46])

        comma = message.index(",")
        if comma == 46:
            self.field_user_define1 = ' '
            self.field_user_define2 = ' '
        else:
            self.field_user_define1 = message[46: comma]
            terminator = message.index("#")
            if (comma + 1) == terminator:
                self.field_user_define2 = ' '
            else:
                self.field_user_define2 = message[comma + 1: terminator]

        self.field_name = " "
        self.field_description = " "
        self.get_from_server()

        global currentDate
        #TimeZone
        str_timezone_diff = datetime.datetime.now(pytz.timezone('America/Chihuahua')).strftime('%z')
        #String Builder
        tmp_current_date = "20" + message[46:48] + "-" + message[49:51] + "-" + message[52:54] + "T" + \
            self.field_user_define2 + ".000000"
        #Device Date
        var_current_date = parse(tmp_current_date)
        #Server Date
        date_now = datetime.datetime.today()
        #Time Diff
        elapsed_time = date_now - var_current_date
        #If the timediff > 1 month, use the Server Date

        date_c = var_current_date + timedelta(hours=int(str_timezone_diff[0] + str_timezone_diff[2]))
        #Format String
        currentDate = date_c.strftime("%Y-%m-%dT%H:%M:%S.000000") + str_timezone_diff
        self.field_date_received = str(currentDate)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Farm_Field/" + str(self.field_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        try:
            result = urllib2.urlopen(request, self.to_json())
        except urllib2.HTTPError, ex:
            print('Server error response')
        pass

    def get_from_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Farm_Field/" + str(self.field_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'
        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            self.field_name = result2['field_name']
            self.field_description = result2['field_description']
        except urllib2.HTTPError, ex:
            #logging.exception("Something awful happened!")
            print('Field names not found ' + str(self.field_id))
        pass

class Sensor_Agg:
    def __init__(self, sensor_id, sensor_hl1, sensor_hl2, sensor_hl3, sensor_temperature, sensor_date_received):
        self.sensor_hl1 = sensor_hl1
        self.sensor_hl2 = sensor_hl2
        self.sensor_hl3 = sensor_hl3
        self.sensor_temperature = sensor_temperature
        self.sensor_date_received = sensor_date_received
        self.sensor_id = sensor_id



    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self, id):
        url = "http://riego.chi.itesm.mx/Sensor_Agg/" + str(id) + "/"
        print "Uploading to " + url
        headers = {"Authorization": "Basic YWRtaW46YWRtaW4=",
                   "Content-Type": "application/json"}
        print self.to_json()
        request = requests.post(url, data=self.to_json(), headers=headers)
        print request.status_code

class Valve_Agg:
    def __init__(self, valve_id, valve_flow, valve_pressure,  valve_date_received):
        self.valve_flow = valve_flow
        self.valve_pressure = valve_pressure
        self.valve_date_received = valve_date_received
        self.valve_id = valve_id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self, id):
        url = "http://riego.chi.itesm.mx/Valve_Agg/" + str(id) + "/"
        print "Uploading to " + url
        headers = {"Authorization": "Basic YWRtaW46YWRtaW4=",
                   "Content-Type": "application/json"}
        print self.to_json()
        request = requests.post(url, data=self.to_json(), headers=headers)
        print request.status_code

class Crop_Area_Agg:
    def __init__(self, area_id, area_ev, area_date_received):
        self.area_ev = area_ev
        self.area_date_received = area_date_received
        self.area_id = area_id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self, id):
        url = "http://riego.chi.itesm.mx/Crop_Area_Agg/" + str(id) + "/"
        print "Uploading to " + url
        headers = {"Authorization": "Basic YWRtaW46YWRtaW4=",
                   "Content-Type": "application/json"}
        print self.to_json()
        request = requests.post(url, data=self.to_json(), headers=headers)
        print request.status_code

class Weather_Station_Agg:
    def __init__(self, station_id, station_relative_humidity, station_temp, station_wind_speed,
                 station_solar_radiation, station_date_received):
        self.station_relative_humidity = station_relative_humidity
        self.station_temperature = station_temp
        self.station_wind_speed = station_wind_speed
        self.station_solar_radiation = station_solar_radiation
        self.station_date_received = station_date_received
        self.station_id = station_id


    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self, id):
        url = "http://riego.chi.itesm.mx/Station_Agg/" + str(id) + "/"
        headers = {"Authorization": "Basic YWRtaW46YWRtaW4=",
                   "Content-Type": "application/json"}
        print self.to_json()
        request = requests.post(url, data=self.to_json(), headers=headers)
        print request.status_code

class Farm_Field_Agg:
    def __init__(self, field_id, field_signal, field_latitude, field_longitude, field_date_received):
        self.field_signal = field_signal
        self.field_latitude = field_latitude
        self.field_longitude = field_longitude
        self.field_date_received = field_date_received
        self.field_id = field_id

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self, fieldid):
        url = "http://riego.chi.itesm.mx/Farm_Field_Agg/" + str(id) + "/"
        print "Uploading to " + url
        headers = {"Authorization": "Basic YWRtaW46YWRtaW4=",
                   "Content-Type": "application/json"}
        print self.to_json()
        request = requests.post(url, data=self.to_json(), headers=headers)
        print request.status_code



class MessageProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_message(message):
        global currentDate

        if currentDate is None:
            instantiate_date()

        instantiate_cfg()

        print currentDate
        area_configuration = "ROK"
        msg_areas = 'G'
        msglist = message.split('#')
        converter = HexConverter()
        global config_mode
        config_mode = False

        for msg in msglist:
            try:
                print("------" + msg + "-------")

                """if msg[1:3] == "00":
                    print("KEEP ALIVE")

                elif msg[1:3] == "10":
                    sensor = Sensor(msg + "#")
                    #print sensor.to_json()
                    sensor.upload_to_server()

                elif msg[1:3] == "20":
                    valve = Valve(msg + "#")
                    #print valve.to_json()
                    valve.upload_to_server()

                elif msg[1:3] == "30":
                    area = Crop_Area(msg + "#")
                    #print area.to_json()
                    area.upload_to_server()

                elif msg[1:3] == "40":
                    station = Weather_Station(msg + "#")
                    #print station.to_json()
                    station.upload_to_server()

                elif msg[1:3] == "50":
                    field = Farm_Field(msg + "#")
                    #print field.to_json()
                    field.upload_to_server()

                else:
                    print "Nothing cool > " + msg
                """
                if msg[1:3] == "50":
                    field = Farm_Field(msg + "#")
                    #print field.to_json()
                    field.upload_to_server()

                elif msg[0] == "F":

                    msg = converter.convert(msg)
                    f_data = re.split('W', msg)[0]
                    w_data = 'W'+re.split('W', msg)[1].split('R')[0]

                    #msg -> Farm_Field
                    field_id = f_data[1:3]
                    no_of_areas = f_data[3]

                    #w_data -> Weather
                    print "STATIONS"
                    station = Weather_Station(w_data, field_id[1])
                    #print station.to_json()
                    station.upload_to_server()

                    #First, build the configuration message
                    msg_areas += str(field_id)

                    #r_data -> Area
                    for index in xrange(int(no_of_areas)):
                        #gets the data for the areas
                        r_data = 'R'+re.split('W', msg)[1].split('R')[index+1].split('C')[0]
                        print "AREAS"
                        area = Crop_Area(r_data, field_id[1],station.station_ev)
                        #area configuration setup

                        global area_cfg
                        print "--" + area_cfg + "---"

                        if area_configuration != area_cfg:
                            area_configuration = area_cfg
                            msg_areas += area_configuration
                            #normalize the db to ROK
                            area.normalize_cfg()

                        #print area.to_json()
                        area.upload_to_server()
                        #gets the data for the consolidated sensor
                        sc_data = 'C'+re.split('W', msg)[1].split('R')[index+1].split('C')[1].split('S')[0]
                        area_id = r_data[1]
                        print "CONSOLIDATED SENSORS"
                        sensor = Sensor(sc_data, field_id[1], area_id)
                        #print sensor.to_json()
                        sensor.upload_to_server()
                        no_of_sensors = int(r_data[2])
                        #gets the data for all the sensors
                        for index2 in xrange(index,int(no_of_sensors)+index):
                            s_data = 'S'+re.split('W', msg)[1].split('R')[index2+1].split('C')[1].split('S')[1].split('A')[0]
                            area_id = r_data[1]
                            print "SENSORS"
                            sensor = Sensor(s_data, field_id[1], area_id)
                            #print sensor.to_json()
                            sensor.upload_to_server()
                            #gets the data for the actuators
                            a_data = 'A'+re.split('W', msg)[1].split('R')[index2+1].split('C')[1].split('S')[1].split('A')[1]
                            print "ACTUATORS"
                            actuator = Valve(a_data, field_id[1], area_id)
                            #print actuator.to_json()
                            actuator.upload_to_server()
                else:
                    print "Nothing cool > " + msg

            except ValueError:
                print('Non-numeric data: ' + msg)

            except Exception, ex:
                logging.exception("Something awful happened!")
                print('Unexpected error: ' + msg)

            #if the area config has been changed, return it
            if config_mode:
                print "Sending configuration"
                print msg_areas
                return msg_areas
            else:
                print "No configuration pending"
                return 'ROK'
            """
            g = chr(71)
            f1 = chr(0) + chr(1) + chr(1) + chr(2) + chr(15) + chr(19) + chr(30) + chr(22) + chr(0)
            f2 = chr(2) + chr(2) + chr(16) + chr(14) + chr(29) + chr(0) + chr(0)
            f3 = chr(3) + chr(0)*6
            f4 = chr(4) + chr(0)*6
            f5 = chr(5) + chr(0)*6
            f6 = chr(6) + chr(0)*6
            f7 = chr(7) + chr(0)*6
            f8 = chr(8) + chr(0)*6
            f9 = chr(9) + chr(0)*6
            f10 = chr(10) + chr(0)*6
            return g + f1 + f2 + f3 + f4 + f5 + f6 + f7 +f8 +f9 +f10"""
