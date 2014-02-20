__author__ = 'admin'

import json
import urllib2, base64

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
        self.fk_area = "http://riego.chi.itesm.mx/Crop_Area/" + str(int(message[3:5])) + "/"


    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/"+str(self.sensor_id)+"/")
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
        self.valve_status = int(message[7:9])
        self.valve_flow = int(message[9:14])
        self.valve_pressure = int(message[14:19])
        self.valve_limit = 0
        self.valve_ideal = 0
        self.fk_area = "http://riego.chi.itesm.mx/Crop_Area/" + str(int(message[3:5])) + "/"
        #self.limit = int(message[21:26])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Valve/"+str(self.valve_id)+"/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())

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
        self.fk_farm_field = "http://riego.chi.itesm.mx/Farm_Field/0/"
        self.fk_crop = "http://riego.chi.itesm.mx/Crop/0/"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/"+str(self.area_id)+"/")
        request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        request.add_header("Content-Type", "application/json")
        request.get_method = lambda: 'PUT'
        print self.to_json()
        result = urllib2.urlopen(request, self.to_json())
        pass


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
        self.station_status = int(message[7:9])
        self.station_relative_humidity = float(message[9:11] + '.' + message[11])
        self.station_temperature = float(message[12:15] + '.' + message[15])
        self.station_wind_speed = int(message[16:19])
        self.station_solar_radiation = int(message[19:23])
        #self.ev = float(message[23:25] + '.' + message[25])
        self.fk_farm_field = "http://riego.chi.itesm.mx/Farm_Field/0/"

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        request = urllib2.Request("http://riego.chi.itesm.mx/Weather_Station/"+str(self.area_id)+"/")
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

        if message[1:3] == "10":
            sensor = Sensor(message)
            print sensor.to_json()
            sensor.upload_to_server()

        elif message[1:3] == "20":
            valve = Valve(message)
            print valve.to_json()

        elif message[1:3] == "30":
            area = Crop_Area(message)
            print area.to_json()

        elif message[1:3] == "40":
            station = Weather_Station(message)
            print station.to_json()

        else:
            print "Nothing cool"

