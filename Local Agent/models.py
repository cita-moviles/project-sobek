__author__ = 'Enrique Ramirez'

import csv
import json


class Moisture_Agent(object):
    """ Local Python Agent used to read the Moisture and Weather Data Logs used
    update the data on the Water Automation API"""

    def __init__(self):
        super(Moisture_Agent, self).__init__()

    def read_file(self, file):
        """Return list of rows in csv file
            Keyword arguments:
                file     -- the name of the file to read
        """
        with open(file, 'rb') as f:
            rows = list(csv.reader(f))

        return rows


class Moisture_Event(object):
    """ Object that represents the data acquired from the sensors. on V1 this
        data comes from a CSV file with the following structure

        area_id, moisture, min, max, date

    """

    def __init__(self, area_id, moisture, min, max, date):
        super(Moisture_Event, self).__init__()

        self.area_id = area_id
        self.moisture = moisture
        self.min = min
        self.max = max
        self.date = date

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Weather_Data(object):
    """ Object that represents the data acquired from the sensors. on V1 this
        data comes from a CSV file with the following structure

        area_id, temperature, solar_intensity, windspeed, humidity, air_pressure, ET, date

    """

    def __init__(self, area_id, temperature, solar_intesity, windspeed,
                 humidity, air_pressure, ET, date):
        super(Weather_Data, self).__init__()

        self.area_id = area_id
        self.temperature = temperature
        self.solar_intensity = solar_intesity
        self.windspeed = windspeed
        self.humidity = humidity
        self.air_pressure = air_pressure
        self.ET = ET #evapotranspiration
        self.date = date

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)



