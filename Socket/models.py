__author__ = 'admin'

import json
import requests
from base64 import b64encode


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

        self.id = int(message[3:7])
        self.status = int(message[7:9])
        self.hl1 = float(message[9:11] + "." + message[11])
        self.hl2 = float(message[12:14] + "." + message[14])
        self.hl3 = float(message[15:17] + "." + message[17])
        self.temp = float(message[18:21] + "." + message[21])


    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        ip_address = "http://riego.chi.itesm.mx"

        url_event = ip_address + "/Sensor/" + str(self.id) + "/"
        userAndPass = b64encode(b"admin:admin").decode('ascii')
        print userAndPass
        headers = {'Content-type': 'application/json', 'Authorization': 'Basic %s' % userAndPass}

        req = requests.put(url_event, data=self.to_json(), headers=headers)
        pass


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
        self.id = int(message[3:7])
        self.status = int(message[7:9])
        self.flow = int(message[9:14])
        self.pressure = int(message[14:19])
        #self.limit = int(message[21:26])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        #TODO: create http request for the server.

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
        self.id = int(message[3:7])
        self.ev = float(message[7:9] + "." + message[9])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        #TODO: create http request for the server.
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
        self.id = int(message[3:7])
        self.status = int(message[7:9])
        self.humidity = float(message[9:11] + '.' + message[11])
        self.temperature = float(message[12:15] + '.' + message[15])
        self.wind_speed = int(message[16:19])
        self.solar_radiation = int(message[19:23])
        #self.ev = float(message[23:25] + '.' + message[25])

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def upload_to_server(self):
        #TODO: create http request for the server.
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
            print "keep alive"

