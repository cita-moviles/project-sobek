from django.db import models

# Create your models here.
class Moisture_Event(models.Model):
    area_id = models.IntegerField()
    moisture = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    date = models.FloatField()

class Weather_Data(models.Model):
    area_id = models.IntegerField()
    temperature  = models.FloatField()
    solar_intensity = models.FloatField()
    windspeed = models.FloatField()
    humidity = models.FloatField()
    air_pressure = models.FloatField()
    ET = models.FloatField()
    date = models.DateTimeField()