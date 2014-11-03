from django.db import models


class Crop(models.Model):
    crop_id = models.IntegerField(primary_key=True)
    crop_name = models.CharField(max_length=50)
    crop_description = models.TextField(max_length=200)
    crop_ev = models.FloatField()
    crop_date_received = models.DateTimeField(null=True, blank=True)
    crop_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    crop_user_define2 = models.TextField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.crop_name


class Farm_Field(models.Model):
    field_id = models.IntegerField(primary_key=True)
    field_name = models.CharField(max_length=50)
    field_description = models.TextField(max_length=200)
    field_imei = models.TextField(max_length=15)
    field_signal = models.FloatField(null=True, blank=True, default=0)
    field_latitude = models.FloatField()
    field_longitude = models.FloatField()
    field_date_received = models.DateTimeField(null=True, blank=True)
    field_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    field_user_define2 = models.TextField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return self.field_name


class Crop_Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=50)
    area_description = models.TextField(max_length=200)
    area_ev = models.FloatField(null=True, blank=True)
    area_x_position = models.IntegerField()
    area_y_position = models.IntegerField()
    area_date_received = models.DateTimeField(null=True, blank=True)
    area_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    area_user_define2 = models.TextField(max_length=250, null=True, blank=True)
    fk_farm_field = models.ForeignKey('Farm_Field')
    fk_crop = models.ForeignKey('Crop')

    def __unicode__(self):
        return self.area_name


class Area_Configuration(models.Model):
    area_id = models.ForeignKey('Crop_Area', primary_key=True)
    area_configuration = models.TextField(max_length=250, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.area_configuration)


class Valve(models.Model):
    valve_id = models.IntegerField(primary_key=True)
    valve_name = models.CharField(max_length=50)
    valve_status = models.SmallIntegerField(max_length=2, default=0)
    valve_flow = models.FloatField(null=True, blank=True, default=0)
    valve_pressure = models.FloatField(null=True, blank=True, default=0)
    valve_limit = models.FloatField(null=True, blank=True, default=0)
    valve_ideal = models.FloatField(null=True, blank=True, default=0)
    valve_date_received = models.DateTimeField(null=True, blank=True)
    valve_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    valve_user_define2 = models.TextField(max_length=250, null=True, blank=True)
    fk_area = models.ForeignKey('Crop_Area')

    def __unicode__(self):
        return self.valve_name


class Weather_Station(models.Model):
    station_id = models.IntegerField(primary_key=True)
    station_name = models.CharField(max_length=50)
    station_status = models.SmallIntegerField(max_length=2, default=0)
    station_relative_humidity = models.FloatField(null=True, blank=True, default = 0)
    station_temperature = models.FloatField(null=True, blank=True, default = 0)
    station_wind_speed = models.FloatField(null=True, blank=True, default = 0)
    station_solar_radiation = models.FloatField(null=True, blank=True, default = 0)
    station_date_received = models.DateTimeField(null=True, blank=True)
    station_user_define1 = models.TextField(max_length=250, null=True,
                                            blank=True)
    station_user_define2 = models.TextField(max_length=250, null=True,
                                            blank=True)
    fk_farm_field = models.ForeignKey('Farm_Field')

    def __unicode__(self):
        return self.station_name


class Sensor(models.Model):
    sensor_id = models.IntegerField(primary_key=True)
    sensor_name = models.CharField(max_length=59)
    sensor_status = models.SmallIntegerField(max_length=2)
    sensor_hl1 = models.FloatField(null=True, blank=True, default = 0)
    sensor_hl2 = models.FloatField(null=True, blank=True, default = 0)
    sensor_hl3 = models.FloatField(null=True, blank=True, default = 0)
    sensor_temperature = models.FloatField(null=True, blank=True, default = 0)
    sensor_x_position = models.IntegerField(null=True, blank=True)
    sensor_y_position = models.IntegerField(null=True, blank=True)
    sensor_date_received = models.DateTimeField(null=True, blank=True)
    sensor_user_define1 = models.TextField(max_length=250, null=True,
                                           blank=True)
    sensor_user_define2 = models.TextField(max_length=250, null=True,
                                           blank=True)
    fk_area = models.ForeignKey('Crop_Area')

    def __unicode__(self):
        return self.sensor_name
# Logs
class Sensor_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    sensor_id = models.ForeignKey('Sensor')
    sensor_status = models.SmallIntegerField(max_length=2)
    sensor_hl1 = models.FloatField()
    sensor_hl2 = models.FloatField()
    sensor_hl3 = models.FloatField()
    sensor_temperature = models.FloatField()
    sensor_date_received = models.DateTimeField(db_index=True)
    sensor_user_define1 = models.TextField(max_length=250, null=True,
                                           blank=True)
    sensor_user_define2 = models.TextField(max_length=250, null=True,
                                           blank=True)
    class Meta:
        unique_together = ["sensor_id", "sensor_date_received"]

    def __unicode__(self):
        return self.log_number


class Valve_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    valve_id = models.ForeignKey('Valve')
    valve_status = models.SmallIntegerField(max_length=2)
    valve_flow = models.FloatField()
    valve_pressure = models.FloatField()
    valve_limit = models.FloatField()
    valve_date_received = models.DateTimeField(db_index=True)
    valve_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    valve_user_define2 = models.TextField(max_length=250, null=True, blank=True)

    class Meta:
        unique_together = ["valve_id", "valve_date_received"]

    def __unicode__(self):
        return self.log_number


class Crop_Area_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    area_id = models.ForeignKey('Crop_Area')
    area_ev = models.FloatField()
    area_date_received = models.DateTimeField(db_index=True)
    area_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    area_user_define2 = models.TextField(max_length=250, null=True, blank=True)

    class Meta:
        unique_together = ["area_id", "area_date_received"]

    def __unicode__(self):
        return self.log_number


class Weather_Station_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    station_id = models.ForeignKey('Weather_Station')
    station_status = models.SmallIntegerField(max_length=2)
    station_relative_humidity = models.FloatField()
    station_temperature = models.FloatField()
    station_wind_speed = models.FloatField()
    station_solar_radiation = models.FloatField()
    station_date_received = models.DateTimeField(db_index=True)
    station_user_define1 = models.TextField(max_length=250, null=True,
                                            blank=True)
    station_user_define2 = models.TextField(max_length=250, null=True,
                                            blank=True)

    class Meta:
        unique_together = ["station_id", "station_date_received"]

    def __unicode__(self):
        return self.log_number


class Farm_Field_Log(models.Model):
    log_number = models.AutoField(primary_key=True)
    log_timestamp = models.DateTimeField(auto_now=True)
    field_id = models.ForeignKey('Farm_Field')
    field_imei = models.TextField(max_length=15)
    field_signal = models.FloatField()
    field_latitude = models.FloatField()
    field_longitude = models.FloatField()
    field_date_received = models.DateTimeField(db_index=True)
    field_user_define1 = models.TextField(max_length=250, null=True, blank=True)
    field_user_define2 = models.TextField(max_length=250, null=True, blank=True)

    class Meta:
        unique_together = ["field_id", "field_date_received"]

    def __unicode__(self):
        return self.log_number

## Aggregated Models
class Sensor_Agg(models.Model):
    agg_id = models.AutoField(primary_key=True)
    agg_date = models.DateTimeField(auto_now=True)
    sensor_id = models.ForeignKey('Sensor')
    sensor_hl1 = models.FloatField()
    sensor_hl2 = models.FloatField()
    sensor_hl3 = models.FloatField()
    sensor_temperature = models.FloatField()
    sensor_date_received = models.DateTimeField(db_index=True)


class Valve_Agg(models.Model):
    agg_id = models.AutoField(primary_key=True)
    agg_date = models.DateTimeField(auto_now=True)
    valve_id = models.ForeignKey('Valve')
    valve_flow = models.FloatField()
    valve_pressure = models.FloatField()
    valve_date_received = models.DateTimeField(db_index=True)

class Crop_Area_Agg(models.Model):
    agg_id = models.AutoField(primary_key=True)
    agg_date = models.DateTimeField(auto_now=True)
    area_id = models.ForeignKey('Crop_Area')
    area_ev = models.FloatField()
    area_date_received = models.DateTimeField(db_index=True)

class Weather_Station_Agg(models.Model):
    agg_id = models.AutoField(primary_key=True)
    agg_date = models.DateTimeField(auto_now=True)
    station_id = models.ForeignKey('Weather_Station')
    station_relative_humidity = models.FloatField()
    station_temperature = models.FloatField()
    station_wind_speed = models.FloatField()
    station_solar_radiation = models.FloatField()
    station_date_received = models.DateTimeField(db_index=True)

class Farm_Field_Agg(models.Model):
    agg_id = models.AutoField(primary_key=True)
    agg_date = models.DateTimeField(auto_now=True)
    field_id = models.ForeignKey('Farm_Field')
    field_signal = models.FloatField()
    field_latitude = models.FloatField()
    field_longitude = models.FloatField()
    field_date_received = models.DateTimeField(db_index=True)
