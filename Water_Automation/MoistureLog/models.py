from django.db import models


class Moisture_Event(models.Model):
    area_id = models.IntegerField()
    moisture = models.FloatField()
    min = models.FloatField()
    max = models.FloatField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        super(Moisture_Event, self).save(*args, **kwargs)

    class Meta:
        ordering = ('date',)


class Weather_Data(models.Model):
    area_id = models.IntegerField()
    temperature  = models.FloatField()
    solar_intensity = models.FloatField()
    windspeed = models.FloatField()
    humidity = models.FloatField()
    air_pressure = models.FloatField()
    ET = models.FloatField()
    date = models.DateTimeField()

    def save(self, *args, **kwargs):
        super(Weather_Data, self).save(*args, **kwargs)

    class Meta:
        ordering = ('date',)