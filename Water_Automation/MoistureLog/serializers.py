from django.forms import widgets
from rest_framework import serializers
from MoistureLog.models import Moisture_Event, Weather_Data
from django.contrib.auth.models import User


class Moisture_Event_Serializer(serializers.HyperlinkedModelSerializer):
    MoistureLog = serializers.HyperlinkedRelatedField(many=True, view_name='moisture-detail')

    class Meta:
        model = Moisture_Event
        fields = ('url', 'area_id', 'moisture', 'min', 'max', 'date', 'height')


class Weather_Data_Serializer(serializers.HyperlinkedModelSerializer):
    MoistureLog = serializers.HyperlinkedRelatedField(many=True, view_name='weather-detail')

    class Meta:
        model = Weather_Data
        fields = ('url', 'area_id', 'temperature', 'solar_intensity', 'windspeed', 'humidity',
                  'air_pressure', 'ET', 'date')
