__author__ = 'admin'

import json
import urllib2
import datetime
import pytz
import logging
from datetime import timedelta
from dateutil.parser import parse
import requests

currentDate = None


def instantiate_date():
    global currentDate
    currentDate = datetime.datetime.today()


def instantiate_cfg():
    global area_cfg
    area_cfg = 'ROK'


#10
class Sensor:
    def __init__(self, message):
        """ Class that process and creates objects in order to be uploaded to the server
        Pos[0] = ! Start of message
        Pos[1:2] = header
        Pos[3:4] = Area ID
        Pos[5:6] = Sensor iD
        Pos[7:8] = Status
        Pos[9:10] = HL1 integers
        Pos[11] = HL1 Decimals
        Pos[12:13] = HL1 integers
        Pos[14] = HL1 Decimals
        Pos[15:16] = HL1 integers
        Pos[17] = HL1 Decimals
        Pos[18] = Temp Sign
        Pos[19:20] = Temp integers
        Pos[21] = Temp Decimals
        Pos[-1] = # end of message
        """

        self.sensor_id = int(message[3:7])
        self.sensor_status = int(message[7:9])
        self.sensor_hl1 = float(message[9:11] + "." + message[11])
        self.sensor_hl2 = float(message[12:14] + "." + message[14])
        self.sensor_hl3 = float(message[15:17] + "." + message[17])
        self.sensor_temperature = float(message[18:21] + "." + message[21])
        self.sensor_x_position = 0
        self.sensor_y_position = 0
        comma = message.index(',')
        if comma == 22:
            self.sensor_user_define1 = ' '
            self.sensor_user_define2 = ' '
        else:
            self.sensor_user_define1 = message[22: comma]
            terminator = message.index('#')
            if (comma + 1) == terminator:
                self.sensor_user_define2 = ' '
            else:
                self.sensor_user_define2 = message[comma + 1: terminator]
        self.fk_area = "http://riego.chi.itesm.mx/Crop_Area/" + str(int(message[3:5])) + "/"
        global currentDate
        self.sensor_date_received = str(currentDate)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/" + str(self.sensor_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())


#20
class Valve:
    def __init__(self, message):
        """ Class that process and creates objects in order to be uploaded to the server
        Pos[0] = ! Start of message
        Pos[1:2] = header
        Pos[3:7] = Valve ID
        Pos[7:9] = Status
        Pos[9:15] = Flow
        Pos[15:21] = Pressure
        Pos[21:26] = Limit
        Pos[-1] = # end of message
        """
        self.valve_id = int(message[3:7])
        self.valve_name = " "
        self.valve_status = int(message[7:9])
        self.valve_flow = int(message[9:14])
        self.valve_pressure = int(message[14:19])
        self.valve_limit = 0
        self.valve_ideal = 0
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
        self.fk_area = "http://riego.chi.itesm.mx/Crop_Area/" + str(int(message[3:5])) + "/"
        global currentDate
        self.valve_date_received = str(currentDate)
        #self.limit = int(message[21:26])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Valve/" + str(self.valve_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print "---http://riego.chi.itesm.mx/Valve/" + str(self.valve_id) + "/"
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())
        pass


#30
class Crop_Area:
    def __init__(self, message):
        """ Class that process and creates objects in order to be uploaded to the server
          Pos[0] = ! Start of message
          Pos[1:2] = header
          Pos[3:7] = Area ID
          Pos[7:9] = Integers EV
          Pos[9] = Decimals EV
          Pos[-1] = #End of message
          """
        self.area_id = int(message[3:7])
        self.area_ev = float(message[7:9] + "." + message[9])
        self.area_x_position = 0
        self.area_y_position = 0
        comma = message.index(",")
        if comma == 10:
            self.area_user_define1 = ' '
            self.area_user_define2 = ' '
        else:
            self.area_user_define1 = message[10: comma]
            terminator = message.index("#")
            if (comma + 1) == terminator:
                self.area_user_define2 = ' '
            else:
                self.area_user_define2 = message[comma + 1: terminator]
        self.fk_farm_field = "http://riego.chi.itesm.mx/Farm_Field/" + str(int(message[3:5])) + "/"
        self.fk_crop = "http://riego.chi.itesm.mx/Crop/0/"
        global currentDate
        self.area_date_received = str(currentDate)
        global area_cfg
        self.area_name = " "
        self.area_description = " "
        self.get_name_from_server()
        area_cfg = self.get_from_server()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())
        pass

    def get_name_from_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'
        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            self.area_name = result2['area_name']
            self.area_description = result2['area_description']
        except urllib2.HTTPError, ex:
            #logging.exception("Something awful happened!")
            print('Area names not found ' + str(self.area_id))
        pass

    def get_from_server(self):
        area_cfg = ''
        request = urllib2.Request("http://riego.chi.itesm.mx/Area_Configuration/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'GET'

        try:
            result = urllib2.urlopen(request)
            result2 = json.load(result)
            print result2['area_configuration']
            print self.area_user_define1
            if result2['area_configuration'] == self.area_user_define1:
                area_cfg += 'ROK'
                print "No configuration pending"
            else:
                area_cfg += "CFG" + str(self.area_id).zfill(4) + str(result2['area_configuration']) + "#"
                print "Sending pending configuration"

        except urllib2.HTTPError, ex:
            #logging.exception("Something awful happened!")
            print('Area configuration not found ' + str(self.area_id))
        return area_cfg


#40
class Weather_Station:
    def __init__(self, message):
        """ Class that process and creates objects in order to be uploaded to the server
          Pos[0] = ! Start of message
          Pos[1:2] = header
          Pos[3:7] = Weather Station's ID
          Pos[7:9] = Status
          Pos[9:11] = Relative humidity integers
          Pos[11] = Relative humidity decimals
          Pos[12:16] = Temperature Integers
          Pos[16] = Temperature decimals
          Pos[17:20] = Wind speed
          Pos[21:24] = Solar Radiation
          Pos[25:27] = EV Integers
          Pos[27] = EV Decimals
          Pos[-1] = #End of message
          """
        self.station_id = int(message[3:7])
        self.station_name = " "
        self.station_status = int(message[7:9])
        self.station_relative_humidity = float(message[9:11] + '.' + message[11])
        self.station_temperature = float(message[12:15] + '.' + message[15])
        self.station_wind_speed = float(message[16:18] + '.' + message[18:19])
        self.station_solar_radiation = int(message[19:23])
        #self.ev = float(message[23:25] + '.' + message[25])
        comma = message.index(",")
        if comma == 23:
            self.station_user_define1 = ' '
            self.station_user_define2 = ' '
        else:
            self.station_user_define1 = message[23: comma]
            terminator = message.index("#")
            if (comma + 1) == terminator:
                self.station_user_define2 = ' '
            else:
                self.station_user_define2 = message[comma + 1: terminator]
        self.fk_farm_field = "http://riego.chi.itesm.mx/Farm_Field/0/"
        global currentDate
        self.station_date_received = str(currentDate)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Weather_Station/" + str(self.station_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())
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
        self.field_name = " "
        self.field_description = " "
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
        if abs(elapsed_time.total_seconds()) > (3600 * 24 * 31):
            var_current_date = date_now
        else:
            #Substract the timezone from the date
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
        result = urllib2.urlopen(request, self.to_json())
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
        url = "http://riego.chi.itesm.mx/Weather_Station_Agg/" + str(id) + "/"
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
        msglist = message.split('#')

        for msg in msglist:
            try:
                print("------" + msg + "-------")

                if msg[1:3] == "00":
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

            except ValueError:
                print('Non-numeric data: ' + msg)

            except Exception, ex:
                logging.exception("Something awful happened!")
                print('Unexpected error: ' + msg)

        global area_cfg
        print "--" + area_cfg + "---"
        if area_configuration != area_cfg:
            area_configuration = area_cfg

        return area_configuration