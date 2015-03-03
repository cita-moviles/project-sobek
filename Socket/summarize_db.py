__author__ = 'luishoracio'


""""Program that runs every 1 hour to summarize the data"""

import json
import urllib2
import datetime

from models import Sensor_Agg, Valve_Agg, Crop_Area_Agg, Weather_Station_Agg, Farm_Field_Agg

today = datetime.datetime.today().strftime("%Y-%m-%d")
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
str_today = "&min_date=" + today + "%2000:00:00" + "&max_date=" + today + "%2023:59:59"


def get_sensor_log(sensorid):
    print "Sensor: " + str(sensorid)
    url = "http://riego.chi.itesm.mx/Sensor_Log/?sensor_id=" + str(sensorid) + \
        str_today + "&ordering=-sensor_date_received"

    req = urllib2.Request(url)
    req.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
    req.add_header("Content-Type", "application/json")
    req.get_method = lambda: 'GET'

    try:
        res2 = json.load(urllib2.urlopen(req))
        sensor_hl1 = 0
        sensor_hl2 = 0
        sensor_hl3 = 0
        temperature = 0

        for sensor_detail in res2:
            sensor_hl1 += sensor_detail['sensor_hl1']
            sensor_hl2 += sensor_detail['sensor_hl2']
            sensor_hl3 += sensor_detail['sensor_hl3']
            temperature += sensor_detail['sensor_temperature']
            sensor_id = sensor_detail['sensor_id']
            #print sensor_detail

        if len(res2) > 0:
            avg_sensor_hl1 = sensor_hl1 / len(res2)
            avg_sensor_hl2 = sensor_hl2 / len(res2)
            avg_sensor_hl3 = sensor_hl3 / len(res2)
            avg_temperature = temperature / len(res2)
            sensor = Sensor_Agg(sensor_id, avg_sensor_hl1, avg_sensor_hl2, avg_sensor_hl3, avg_temperature, current_time)
            sensor.to_json()
            sensor.upload_to_server(sensorid)
        else:
            print "No data"

        print ""


        #Save to database
        # * Socket model === Django Model
        # 1. Build object for database.
          # sensor_hl1
          # sensor_hl2
          # sensor_hl3
          # sensor_temperature
          # sensor_date_received = current_time

        # 2. object.to_json() from model
        # 3. object.upload_to_server() from model
        # 4. Profit


    except urllib2.HTTPError, ex:
        #logging.exception("Something awful happened!")
        print('Not found ')


def get_area_log(areaid):
    print "Area: " + str(areaid)
    url = "http://riego.chi.itesm.mx/Crop_Area_Log/?area_id=" + str(areaid) + \
        str_today + "&ordering=-area_date_received"

    req_area = urllib2.Request(url)
    req_area.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
    req_area.add_header("Content-Type", "application/json")
    req_area.get_method = lambda: 'GET'

    try:
        res2_area = json.load(urllib2.urlopen(req_area))
        area_ev = 0

        for area_detail in res2_area:
            area_id = area_detail['area_id']
            area_ev += area_detail['area_ev']

        if len(res2_area) > 0:
            avg_area_ev = area_ev / len(res2_area)
            #Save to database
            crop_area = Crop_Area_Agg(area_id, avg_area_ev, current_time)
            crop_area.to_json()
            crop_area.upload_to_server(areaid)
        else:
            print("Zero data")
        print ""

    except urllib2.HTTPError, ex:
        print('Not found ')


def get_valve_log(valveid):
    print "Valve: " + str(valveid)
    url = "http://riego.chi.itesm.mx/Valve_Log/?valve_id=" + str(valveid) + \
        str_today + "&ordering=-valve_date_received"

    req_valve = urllib2.Request(url)
    req_valve.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
    req_valve.add_header("Content-Type", "application/json")
    req_valve.get_method = lambda: 'GET'

    try:
        res2_valve = json.load(urllib2.urlopen(req_valve))
        valve_flow = 0
        valve_pressure = 0

        for valve_detail in res2_valve:
            #print valve_detail
            valve_id = valve_detail['valve_id']
            valve_flow += valve_detail['valve_flow']
            valve_pressure += valve_detail['valve_pressure']


        if len(res2_valve) > 0:
            avg_valve_flow = valve_flow / len(res2_valve)
            avg_valve_pressure = valve_pressure / len(res2_valve)
            valve = Valve_Agg(valve_id, avg_valve_flow, avg_valve_pressure, current_time)
            valve.to_json()
            valve.upload_to_server(valveid)
        else:
            print("Zero data")

        print ""

        #Save to database



    except urllib2.HTTPError, ex:
        print('Not found ')
##Weather_Station
def get_station_log(stationid):
        print "Station: " + str(stationid)
        url = "http://riego.chi.itesm.mx/Station_Log/?station_id=" + str(stationid) + \
            str_today + "&ordering=-station_date_received"

        req_station = urllib2.Request(url)
        req_station.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        req_station.add_header("Content-Type", "application/json")
        req_station.get_method = lambda: 'GET'

        try:
            res2_station = json.load(urllib2.urlopen(req_station))
            station_relative_humidity = 0
            station_temperature = 0
            station_wind_speed = 0
            station_solar_radiation = 0
            station_ev = 0

            for station_detail in res2_station:
                #print station_detail
                station_id = station_detail['station_id']
                station_relative_humidity += station_detail['station_relative_humidity']
                station_temperature += station_detail['station_temperature']
                station_wind_speed += station_detail['station_wind_speed']
                station_solar_radiation += station_detail['station_solar_radiation']
                station_ev += station_detail['station_ev']
            if len(res2_station) > 0:
                avg_station_humidity = station_relative_humidity / len(res2_station)
                avg_station_temp = station_temperature / len(res2_station)
                avg_station_wind = station_wind_speed / len(res2_station)
                avg_station_radiation = station_solar_radiation / len (res2_station)
                avg_station_ev = station_ev / len(station_ev)
                station = Weather_Station_Agg(station_id, avg_station_humidity,avg_station_temp,avg_station_wind,
                                          avg_station_radiation,avg_station_ev,current_time)
                station.to_json()
                station.upload_to_server(stationid)
            else:
                print("Zero data")

            print ""

            #Save to database



        except urllib2.HTTPError, ex:
            print('Not found ')

##Farm_Field
def get_field_log(fieldid):
        print "Field: " + str(fieldid)
        url = "http://riego.chi.itesm.mx/Farm_Field_Log/?field_id=" + str(fieldid) + \
            str_today + "&ordering=-field_date_received"

        req_field = urllib2.Request(url)
        req_field.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
        req_field.add_header("Content-Type", "application/json")
        req_field.get_method = lambda: 'GET'

        try:
            res2_field = json.load(urllib2.urlopen(req_field))
            field_signal = 0
            field_latitude = 0
            field_longitude = 0

            for field_detail in res2_field:
                #print field_detail
                field_id = field_detail['field_id']
                field_signal += field_detail['field_signal']
                field_latitude += field_detail['field_latitude']
                field_longitude += field_detail['field_longitude']

            if len(res2_field) > 0:
                avg_field_signal = field_signal / len(res2_field)
                avg_field_latitude = field_latitude / len(res2_field)
                avg_field_longitude = field_longitude / len(res2_field)
                field = Farm_Field_Agg(field_id, avg_field_signal, avg_field_latitude, avg_field_longitude, current_time)
                field.to_json()
                field.upload_to_server(fieldid)
            else:
                print("Zero data")

            print ""





        except urllib2.HTTPError, ex:
            print('Not found ')


##Execute

## Sensor exe
request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/")
request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
request.add_header("Content-Type", "application/json")
request.get_method = lambda: 'GET'

try:
    print "-----------"
    result = urllib2.urlopen(request)
    result2 = json.load(result)
    for sensor in result2:
        sensor_id = sensor['sensor_id']
        get_sensor_log(sensor_id)

except urllib2.HTTPError, ex:
    print('Not found ')

## Area exe
request = urllib2.Request("http://riego.chi.itesm.mx/Crop_Area/")
request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
request.add_header("Content-Type", "application/json")
request.get_method = lambda: 'GET'

try:
    print "-----------"
    result = urllib2.urlopen(request)
    result2 = json.load(result)
    #print result2
    for area in result2:
        area_id = area['area_id']
        get_area_log(area_id)

except urllib2.HTTPError, ex:
    print('Not found ')

## Valve exe
request = urllib2.Request("http://riego.chi.itesm.mx/Valve/")
request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
request.add_header("Content-Type", "application/json")
request.get_method = lambda: 'GET'

try:
    print "-----------"
    result = urllib2.urlopen(request)
    result2 = json.load(result)
    #print result2
    for valve in result2:
        valve_id = valve['valve_id']
        get_valve_log(valve_id)

except urllib2.HTTPError, ex:
    print('Not found ')

## Station exe
request = urllib2.Request("http://riego.chi.itesm.mx/Weather_Station/")
request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
request.add_header("Content-Type", "application/json")
request.get_method = lambda: 'GET'

try:
    print "-----------"
    result = urllib2.urlopen(request)
    result2 = json.load(result)
    for station in result2:
        station_id = station['station_id']
        get_station_log(station_id)


except urllib2.HTTPError, ex:
    print('Not found ')

## Field exe
request = urllib2.Request("http://riego.chi.itesm.mx/Farm_Field/")
request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
request.add_header("Content-Type", "application/json")
request.get_method = lambda: 'GET'

try:
    print "-----------"
    result = urllib2.urlopen(request)
    result2 = json.load(result)
    for field in result2:
        field_id = field['field_id']
        get_field_log(field_id)

except urllib2.HTTPError, ex:
    print('Not found ')
