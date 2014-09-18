__author__ = 'luishoracio'


""""Program that runs every 1 hour to summarize the data"""

import json
import urllib2
import datetime

today = datetime.datetime.today().strftime("%Y-%m-%d")
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
            #print sensor_detail

        if len(res2) > 0:
            print sensor_hl1 / len(res2)
            print sensor_hl2 / len(res2)
            print sensor_hl3 / len(res2)
            print temperature / len(res2)
        else:
            print "No data"

        print ""

        #TODO
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
            area_ev += area_detail['area_ev']

        if len(res2_area) > 0:
            print area_ev / len(res2_area)
        else:
            print("Zero data")
        print ""
        #TODO
        #Save to database

    except urllib2.HTTPError, ex:
        print('Not found ')


def get_valve_log(valveid):
    print "Valve: " + str(valveid)
    url = "http://riego.chi.itesm.mx/Valve_Log/?valve_id=" + str(valveid) + \
        str_today + "&ordering=-valve_date_received"

    req_area = urllib2.Request(url)
    req_area.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
    req_area.add_header("Content-Type", "application/json")
    req_area.get_method = lambda: 'GET'

    try:
        res2_area = json.load(urllib2.urlopen(req_area))
        valve_flow = 0
        valve_pressure = 0

        for valve_detail in res2_area:
            #print valve_detail
            valve_flow += valve_detail['valve_flow']
            valve_pressure += valve_detail['valve_pressure']

        if len(res2_area) > 0:
            print valve_flow / len(res2_area)
            print valve_pressure / len(res2_area)
        else:
            print("Zero data")

        print ""
        #TODO
        #Save to database

    except urllib2.HTTPError, ex:
        print('Not found ')


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
