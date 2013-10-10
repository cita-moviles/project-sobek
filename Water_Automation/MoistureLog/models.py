from django.db import models

# Create your models here.
class MoistureEvent(models.Model):
    area_id = models.IntegerField()
    date = models.DateTimeField()
    moisture = models.FloatField()
    minimum_moisture