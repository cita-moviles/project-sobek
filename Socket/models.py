__author__ = 'admin'

import json
import urllib2
import datetime
import pytz
import logging
from datetime import timedelta
from dateutil.parser import parse
from time import strftime

currentDate = None


def instanciate_date():
    global currentDate
    currentDate = datetime.datetime.today()


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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/" + str(self.sensor_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())


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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Valve/" + str(self.valve_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        #result = urllib2.urlopen(request, self.to_json())
        pass


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
        self.area_x_position = 0
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
        self.area_configuration = self.get_from_server()


    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/" + str(self.area_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())
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
            print('Valve configuration not found ' + str(self.area_id))
        return area_cfg


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
        self.station_wind_speed = int(message[16:19])
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
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Weather_Station/" + str(self.station_id) + "/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())
        pass


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
        strTimezoneDiff = datetime.datetime.now(pytz.timezone('America/Chihuahua')).strftime('%z')
        tmpcurrentDate = "20" + message[46:48] + "-" + message[49:51] + "-" + message[52:54] + "T" + \
                      self.field_user_define2 + ".000000"
        varcurrentDate = parse(tmpcurrentDate)
        dateC = varcurrentDate + timedelta(hours=int(strTimezoneDiff[0] + strTimezoneDiff[2]))
        currentDate = dateC.strftime("%Y-%m-%dT%H:%M:%S.000000") + strTimezoneDiff
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


class MessageProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_message(message):
        global currentDate

        if currentDate is None:
            instanciate_date()

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
                    area_configuration = area.area_configuration

                elif msg[1:3] == "40":
                    station = Weather_Station(msg + "#")
                    #print station.to_json()
                    station.upload_to_server()

                elif msg[1:3] == "50":
                    field = Farm_Field(msg + "#")
                    #print field.to_json()
                    field.upload_to_server()

                else:
                    print "Nothing cool"

            except ValueError:
                print('Non-numeric data: ' + msg)

            except Exception, ex:
                logging.exception("Something awful happened!")
                print('Unexpected error: ' + msg)

        return area_configuration