__author__ = 'admin'
from rest_framework import serializers

from models import Crop, Farm_Field, Crop_Area, Valve, Area_Configuration, Weather_Station, Sensor, \
    Crop_Area_Log, Weather_Station_Log, Sensor_Log, Valve_Log, Farm_Field_Log, Sensor_Agg, Valve_Agg, \
    Crop_Area_Agg, Weather_Station_Agg, Farm_Field_Agg



class Crop_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='crop-detail')

    class Meta:
        model = Crop
        fields = ('crop_id', 'crop_name', 'crop_description', 'crop_ev', 'crop_date_received',
                  'crop_user_define1', 'crop_user_define2')


class Farm_Field_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='field-detail')

    class Meta:
        model = Farm_Field
        fields = ('field_id', 'field_name', 'field_description', 'field_imei', 'field_signal',
                  'field_latitude', 'field_longitude', 'field_date_received', 'field_user_define1', 'field_user_define2')


class Area_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='area-detail')

    class Meta:
        model = Crop_Area
        fields = (
            'area_id', 'area_name', 'area_description', 'area_ev', 'area_x_position', 'area_y_position',
            'area_date_received', 'area_user_define1', 'area_user_define2', 'fk_farm_field', 'fk_crop'
        )


class Area_Configuration_Serializer(serializers.ModelSerializer):
    area_id = serializers.RelatedField()

    class Meta:
        model = Area_Configuration
        fields = (
            'area_id', 'area_configuration'
        )


class Valve_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='valve-detail')

    class Meta:
        model = Valve
        fields = (
            'valve_id', 'valve_name', 'valve_status', 'valve_flow', 'valve_pressure', 'valve_limit', 'valve_ideal',
            'valve_date_received', 'valve_user_define1', 'valve_user_define2', 'fk_area'
        )


class Station_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='station-detail')

    class Meta:
        model = Weather_Station
        fields = (
            'station_id', 'station_name', 'station_status', 'station_relative_humidity', 'station_temperature',
            'station_wind_speed', 'station_solar_radiation', 'station_date_received',
            'station_user_define1', 'station_user_define2', 'fk_farm_field'
        )


class Sensor_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='sensor-detail')

    class Meta:
        model = Sensor
        fields = (
            'sensor_id', 'sensor_name', 'sensor_status', 'sensor_hl1', 'sensor_hl2', 'sensor_hl3', 'sensor_temperature',
            'sensor_x_position', 'sensor_y_position', 'sensor_date_received',
            'sensor_user_define1', 'sensor_user_define2', 'fk_area'
        )


#LOGS
class Farm_Field_Log_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='field-log-detail')

    class Meta:
        model = Farm_Field_Log
        fields = ('log_number', 'log_timestamp', 'field_id', 'field_imei', 'field_signal', 'field_date_received',
                  'field_user_define1', 'field_user_define2')


class Area_Log_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='area-log-detail')

    class Meta:
        model = Crop_Area_Log
        fields = ('log_number', 'log_timestamp', 'area_id', 'area_ev', 'area_date_received',
                  'area_user_define1', 'area_user_define2')


class Weather_Station_Log_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='station-log-detail')

    class Meta:
        model = Weather_Station_Log
        fields = ('log_number', 'log_timestamp', 'station_id', 'station_status', 'station_relative_humidity',
                  'station_temperature', 'station_wind_speed', 'station_solar_radiation',
                  'station_date_received', 'station_user_define1', 'station_user_define2')


class Sensor_Log_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='sensor-log-detail')

    class Meta:
        model = Sensor_Log
        fields = ('log_number', 'log_timestamp', 'sensor_id', 'sensor_status', 'sensor_hl1', 'sensor_hl2',
                  'sensor_hl3', 'sensor_temperature', 'sensor_date_received',
                  'sensor_user_define1', 'sensor_user_define2')


class Valve_Log_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='valve-log-detail')

    class Meta:
        model = Valve_Log
        fields = ('log_number', 'log_timestamp', 'valve_id', 'valve_status', 'valve_flow', 'valve_pressure',
                  'valve_limit', 'valve_date_received', 'valve_user_define1', 'valve_user_define2')

#AGGREGATE
class Sensor_Agg_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='sensor-agg-detail')

    class Meta:
        model = Sensor_Agg
        fields = ('agg_id', 'agg_date', 'sensor_id', 'sensor_hl1', 'sensor_hl2',
                  'sensor_hl3', 'sensor_temperature', 'sensor_date_received')


class Valve_Agg_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='valve-agg-detail')

    class Meta:
        model = Valve_Agg
        fields = ('agg_id', 'agg_date', 'valve_id', 'valve_flow', 'valve_pressure',
                  'valve_date_received')


class Crop_Area_Agg_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='crop-area-agg-detail')

    class Meta:
        model = Crop_Area_Agg
        fields = ('agg_id', 'agg_date', 'area_id', 'area_ev', 'area_date_received')


class Weather_Station_Agg_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='weather-station-agg-detail')

    class Meta:
        model = Weather_Station_Agg
        fields = ('agg_id', 'agg_date', 'station_id', 'station_status', 'station_relative_humidty',
                  'station_temperature', 'station_wind_speed', 'station_solar_radiation', 'station_date_received')


class Farm_Field_Agg_Serializer(serializers.HyperlinkedModelSerializer):
    FieldApp = serializers.HyperlinkedRelatedField(many=True, view_name='farm-field-agg-detail')

    class Meta:
        model = Farm_Field_Agg
        fields = ('agg_id', 'agg_date', 'field_id', 'field_imei', 'field_signal', 'field_latitude',
                  'field_longitude', 'field_date_received')