__author__ = 'admin'

import urllib2, base64
message = '{"sensor_id":"0","sensor_temperature":"0.5","sensor_status":"0","sensor_hl1":"22","sensor_hl2":"03.2","sensor_hl3":"03.2","sensor_x_position":"0","sensor_y_position":"0","fk_area":"http://127.0.0.1:8000/Crop_Area/0/"}'

request = urllib2.Request("http://riego.chi.itesm.mx/Sensor/0/")
base64string = base64.encodestring('admin:admin').replace('\n', '')
request.add_header("Authorization", "Basic YWRtaW46YWRtaW4=")
request.add_header("Content-Type", "application/json")
request.get_method = lambda: 'PUT'
result = urllib2.urlopen(request, message)