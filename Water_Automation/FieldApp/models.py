from django.db import models


# Create your models here.
class Crop(models.Model):
    crop_id = models.IntegerField(primary_key=True)
    crop_name = models.CharField(max_length=50)
    crop_description = models.TextField(max_length=200)
    crop_ev = models.FloatField()


class Farm_Field(models.Model):
    field_id = models.IntegerField(primary_key=True)
    field_name = models.CharField(max_length=50)
    field_description = models.TextField(max_length=200)
    field_latitude = models.FloatField()
    field_longitude = models.FloatField()


class Crop_Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=50)
    area_description = models.TextField(max_length=200)
    area_ev = models.FloatField()
    area_x_position = models.IntegerField()
    area_y_position = models.IntegerField()
    fk_farm_field = models.ForeignKey('Farm_Field')
    fk_crop = models.ForeignKey('Crop')


class Valve(models.Model):
    valve_id = models.IntegerField(primary_key=True)
    valve_name = models.CharField(max_length=50)
    valve_status = models.SmallIntegerField(max_length=2)
    valve_flow = models.FloatField()
    valve_pressure = models.FloatField()
    valve_limit = models.FloatField()
    valve_ideal = models.FloatField()
    fk_area = models.ForeignKey('Crop_Area')


class Weather_Station(models.Model):
    station_id = models.IntegerField(primary_key=True)
    station_name = models.CharField(max_length=50)
    station_status = models.SmallIntegerField(max_length=2)
    station_relative_humidity = models.FloatField()
    station_temperature = models.FloatField()
    station_wind_speed = models.FloatField()
    station_solar_radiation = models.FloatField()
    fk_farm_field = models.ForeignKey('Farm_Field')


class Sensor(models.Model):
    sensor_id = models.IntegerField(primary_key=True)
    sensor_status = models.SmallIntegerField(max_length=2)
    sensor_hl1 = models.FloatField()
    sensor_hl2 = models.FloatField()
    sensor_hl3 = models.FloatField()
    sensor_temperature = models.FloatField()
    sensor_x_position = models.IntegerField()
    sensor_y_position = models.IntegerField()
    fk_area = models.ForeignKey('Crop_Area')


#Logs
class Sensor_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    sensor_id = models.ForeignKey('Sensor')
    sensor_status = models.SmallIntegerField(max_length=2)
    sensor_hl1 = models.FloatField()
    sensor_hl2 = models.FloatField()
    sensor_hl3 = models.FloatField()
    sensor_temperature = models.FloatField()


class Valve_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    valve_id = models.ForeignKey('Valve')
    valve_status = models.SmallIntegerField(max_length=2)
    valve_flow = models.FloatField()
    valve_pressure = models.FloatField()
    valve_limit = models.FloatField()


class Crop_Area_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    area_id = models.ForeignKey('Crop_Area')
    area_ev = models.FloatField()


class Weather_Station_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    station_id = models.ForeignKey('Weather_Station')
    station_status = models.SmallIntegerField(max_length=2)
    station_relative_humidity = models.FloatField()
    station_temperature = models.FloatField()
    station_wind_speed = models.FloatField()
    station_solar_radiation = models.FloatField()