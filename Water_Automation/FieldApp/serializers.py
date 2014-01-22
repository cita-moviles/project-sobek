__author__ = 'admin'

from django.forms import widgets
from rest_framework import serializers
from FieldApp.models import Crop, Farm_Field, Crop_Area, Valve, Weather_Station, Sensor


class Crop_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='crop-detail')

    class Meta:
        model = Crop
        fields = ('crop_id', 'crom_name', 'crop_description', 'crop_ev')


class Farm_Field_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='field-detail')

    class Meta:
        model = Farm_Field
        fields = ('field_id', 'field_name', 'field_description', 'field_latitude', 'field_longitude')


class Area_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='area-detail')

    class Meta:
        model = Crop_Area
        fields = (
            'area_id', 'area_name', 'area_description', 'area_ev', 'area_x_position', 'area_y_position',
            'fk_farm_field', 'fk_crop_id')


class Valve_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='valve-detail')

    class Meta:
        model = Valve
        fields = (
            'valve_id', 'valve_name', 'valve_status', 'valve_flow', 'valve_pressure', 'valve_limit', 'valve_ideal',
            'fk_area'
        )


class Station_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='station-detail')

    class Meta:
        model = Weather_Station
        fields = (
            'station_id','station_name','station_status','station_relative_humidity','station_temperature',
            'station_wind_speed','station_solar_radiation','fk_farm_field'
        )


class Sensor_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='sensor-detail')

    class Meta:
        model = Sensor
        fields = (
            'sensor_id','sensor_status','sensor_hl1','sensor_hl2','sensor_hl3','sensor_temperature','sensor_x_position',
            'sensor_y_position','fk_area'
        )
