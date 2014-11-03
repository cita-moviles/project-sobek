import django_filters
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework_extensions.cache.decorators import (
    cache_response
)
from rest_framework import viewsets
from django.views.generic import TemplateView
from FieldApp.models import Crop, Farm_Field, Crop_Area, Valve, Area_Configuration, Weather_Station, Sensor, \
     Crop_Area_Log, Sensor_Log, Weather_Station_Log, Valve_Log, Farm_Field_Log, Sensor_Agg, Valve_Agg, Crop_Area_Agg, \
     Weather_Station_Agg, Farm_Field_Agg
from FieldApp.serializers import Crop_Serializer, Farm_Field_Serializer, Area_Serializer, \
     Valve_Serializer, Area_Configuration_Serializer, Station_Serializer, Sensor_Serializer, Area_Log_Serializer, \
     Weather_Station_Log_Serializer, Valve_Log_Serializer, Sensor_Log_Serializer, Farm_Field_Log_Serializer, \
     Sensor_Agg_Serializer, Valve_Agg_Serializer, Crop_Area_Agg_Serializer, Weather_Station_Agg_Serializer, \
     Farm_Field_Agg_Serializer


class Crop_ViewSet (viewsets.ModelViewSet):
     queryset = Crop.objects.all ()
     serializer_class = Crop_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Area_ViewSet (viewsets.ModelViewSet):
     queryset = Crop_Area.objects.all ()
     serializer_class = Area_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Valve_ViewSet (viewsets.ModelViewSet):
     queryset = Valve.objects.all ()
     serializer_class = Valve_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Area_Configuration_ViewSet (viewsets.ModelViewSet):
     queryset = Area_Configuration.objects.all ()
     serializer_class = Area_Configuration_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Station_ViewSet (viewsets.ModelViewSet):
     queryset = Weather_Station.objects.all ()
     serializer_class = Station_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Sensor_ViewSet (viewsets.ModelViewSet):
     queryset = Sensor.objects.all ()
     serializer_class = Sensor_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Field_ViewSet (viewsets.ModelViewSet):
     queryset = Farm_Field.objects.all ()
     serializer_class = Farm_Field_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# Filters
class FieldFilter (django_filters.FilterSet):
     class Meta:
          model = Farm_Field
          fields = ['field_id', 'field_name', 'field_description', 'field_imei', 'field_signal', 'field_latitude',
                    'field_longitude', 'field_date_received', 'field_user_define1', 'field_user_define2']


class SensorFilter (django_filters.FilterSet):
     class Meta:
          model = Sensor
          fields = ['sensor_id', 'sensor_status', 'sensor_hl1', 'sensor_hl2', 'sensor_hl3', 'sensor_temperature',
                    'sensor_date_received', 'sensor_user_define1', 'sensor_user_define2', 'fk_area']


class AreaFilter (django_filters.FilterSet):
     class Meta:
          model = Crop_Area
          fields = ['area_id', 'area_name', 'area_date_received', 'area_user_define1', 'area_user_define2',
                    'fk_farm_field', 'fk_crop']


class ValveFilter (django_filters.FilterSet):
     class Meta:
          model = Valve
          fields = ['valve_id', 'valve_name', 'valve_status', 'valve_flow', 'valve_pressure', 'valve_limit',
                    'valve_ideal', 'valve_date_received', 'valve_user_define1', 'valve_user_define2', 'fk_area']


class AreaConfigurationFilter (django_filters.FilterSet):
     class Meta:
          model = Area_Configuration
          fields = ['area_id', 'area_configuration']


class StationFilter (django_filters.FilterSet):
     class Meta:
          model = Weather_Station
          fields = ['station_id', 'station_status', 'station_relative_humidity',
                    'station_temperature', 'station_wind_speed', 'station_solar_radiation',
                    'station_date_received', 'station_user_define1',
                    'station_user_define2', 'fk_farm_field']


# LogFilters
class AreaLogFilter (django_filters.FilterSet):
     year = django_filters.CharFilter (name='log_timestamp', lookup_type='startswith')
     max_ev = django_filters.NumberFilter (name='area_ev', lookup_type='lte')
     max_date = django_filters.DateTimeFilter (name='area_date_received', lookup_type='lte')
     min_date = django_filters.DateTimeFilter (name='area_date_received', lookup_type='gte')

     class Meta:
          model = Crop_Area_Log
          fields = ['area_id', 'log_timestamp', 'area_ev', 'area_date_received']
          order_by = ['area_date_received']

class StationLogFilter (django_filters.FilterSet):
     max_date = django_filters.DateTimeFilter (name='station_date_received', lookup_type='lte')
     min_date = django_filters.DateTimeFilter (name='station_date_received', lookup_type='gte')

     class Meta:
          model = Weather_Station_Log
          fields = ['station_id', 'station_status', 'station_relative_humidity',
                    'station_temperature', 'station_wind_speed', 'station_solar_radiation',
                    'station_date_received']
          order_by = ['station_date_received']

class SensorLogFilter (django_filters.FilterSet):
     max_date = django_filters.DateTimeFilter (name='sensor_date_received', lookup_type='lte')
     min_date = django_filters.DateTimeFilter (name='sensor_date_received', lookup_type='gte')

     class Meta:
          model = Sensor_Log
          fields = ['sensor_id', 'sensor_status', 'sensor_hl1', 'sensor_hl2',
                    'sensor_hl3', 'sensor_temperature', 'sensor_date_received']
          order_by = ['sensor_date_received']

class ValveLogFilter (django_filters.FilterSet):
     max_date = django_filters.DateTimeFilter (name='valve_date_received', lookup_type='lte')
     min_date = django_filters.DateTimeFilter (name='valve_date_received', lookup_type='gte')

     class Meta:
          model = Valve_Log
          fields = ['valve_id', 'valve_status', 'valve_flow', 'valve_pressure',
                    'valve_limit', 'valve_date_received']
          order_by = ['valve_date_received']


class FarmFieldLogFilter (django_filters.FilterSet):
     max_date = django_filters.DateTimeFilter (name='field_date_received', lookup_type='lte')
     min_date = django_filters.DateTimeFilter (name='field_date_received', lookup_type='gte')

     class Meta:
          model = Farm_Field_Log
          fields = ['field_id', 'field_date_received']
          order_by = ['field_date_received']

#Aggregate Model Filters
class SensorAggFilter(django_filters.FilterSet):
    max_date = django_filters.DateTimeFilter(name='sensor_date_received', lookup_type='lte')
    min_date = django_filters.DateTimeFilter(name='sensor_date_received', lookup_type='gte')

    class Meta:
        model = Sensor_Agg
        fields = ['sensor_id', 'sensor_hl1', 'sensor_hl2',
                  'sensor_hl3', 'sensor_temperature', 'sensor_date_received']
        order_by = ['sensor_date_received']

class ValveAggFilter(django_filters.FilterSet):
    max_date = django_filters.DateTimeFilter(name='valve_date_received', lookup_type='lte')
    min_date = django_filters.DateTimeFilter(name='valve_date_received', lookup_type='gte')

    class Meta:
        model = Valve_Agg
        fields = ['valve_id', 'valve_flow', 'valve_pressure', 'valve_date_received']
        order_by = ['valve_date_received']

class AreaAggFilter(django_filters.FilterSet):
    max_date = django_filters.DateTimeFilter(name='area_date_received', lookup_type='lte')
    min_date = django_filters.DateTimeFilter(name='area_date_received', lookup_type='gte')

    class Meta:
        model = Crop_Area_Agg
        fields = ['area_id', 'area_ev', 'area_date_received']
        order_by = ['area_date_received']

class StationAggFilter(django_filters.FilterSet):
    max_date = django_filters.DateTimeFilter(name='station_date_received', lookup_type='lte')
    min_date = django_filters.DateTimeFilter(name='station_date_received', lookup_type='gte')

    class Meta:
        model = Weather_Station_Agg
        fields = ['station_id', 'station_relative_humidity',
                  'station_temperature', 'station_wind_speed', 'station_solar_radiation',
                  'station_date_received']
        order_by = ['station_date_received']

class FieldAggFilter(django_filters.FilterSet):
    max_date = django_filters.DateTimeFilter(name='field_date_received', lookup_type='lte')
    min_date = django_filters.DateTimeFilter(name='field_date_received', lookup_type='gte')

    class Meta:
        model = Farm_Field_Agg
        fields = ['field_id', 'field_signal', 'field_latitude', 'field_longitude', 'field_date_received']
        order_by = ['field_date_received']

#Viewsets
class FieldSearch (generics.ListCreateAPIView):
     queryset = Farm_Field.objects.all ()
     serializer_class = Farm_Field_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = FieldFilter


class SensorSearch (generics.ListCreateAPIView):
     queryset = Sensor.objects.all ()
     serializer_class = Sensor_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = SensorFilter


class AreaSearch (generics.ListCreateAPIView):
     queryset = Crop_Area.objects.all ()
     serializer_class = Area_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = AreaFilter


class ValveSearch (generics.ListCreateAPIView):
     queryset = Valve.objects.all ()
     serializer_class = Valve_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = ValveFilter


class AreaConfigurationSearch (generics.ListCreateAPIView):
     queryset = Area_Configuration.objects.all ()
     serializer_class = Area_Configuration_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = AreaConfigurationFilter


class StationSearch (generics.ListCreateAPIView):
     queryset = Weather_Station.objects.all ()
     serializer_class = Station_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = StationFilter


#LogsViewsets
class Area_Log_ViewSet (generics.ListCreateAPIView):
     queryset = Crop_Area_Log.objects.all ()
     serializer_class = Area_Log_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = AreaLogFilter

class Station_Log_ViewSet (generics.ListCreateAPIView):
     queryset = Weather_Station_Log.objects.all ()
     serializer_class = Weather_Station_Log_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = StationLogFilter


class Sensor_Log_ViewSet (generics.ListCreateAPIView):
     queryset = Sensor_Log.objects.all ()
     serializer_class = Sensor_Log_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = SensorLogFilter


class Valve_Log_ViewSet (generics.ListCreateAPIView):
     queryset = Valve_Log.objects.all ()
     serializer_class = Valve_Log_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = ValveLogFilter


class Farm_Field_Log_ViewSet (generics.ListCreateAPIView):
     queryset = Farm_Field_Log.objects.all ()
     serializer_class = Farm_Field_Log_Serializer
     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
     filter_class = FarmFieldLogFilter


#AggViewSets
class Sensor_Agg_ViewSet(generics.ListCreateAPIView):
    queryset = Sensor_Agg.objects.all()
    serializer_class = Sensor_Agg_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = SensorAggFilter


class Valve_Agg_ViewSet(generics.ListCreateAPIView):
    queryset = Valve_Agg.objects.all()
    serializer_class = Valve_Agg_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = ValveAggFilter


class Crop_Area_Agg_ViewSet(generics.ListCreateAPIView):
    queryset = Crop_Area_Agg.objects.all()
    serializer_class = Crop_Area_Agg_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = AreaAggFilter


class Weather_Station_Agg_ViewSet(generics.ListCreateAPIView):
    queryset = Weather_Station_Agg.objects.all()
    serializer_class = Weather_Station_Agg_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = StationAggFilter


class Farm_Field_Agg_ViewSet(generics.ListCreateAPIView):
    queryset = Farm_Field_Agg.objects.all()
    serializer_class = Farm_Field_Agg_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = FieldAggFilter


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'crop': reverse('crop-list', request=request, format=format),
        'field': reverse('field-list', request=request, format=format),
        'area': reverse('area-list', request=request, format=format),
        'valve': reverse('valve-list', request=request, format=format),
        'station': reverse('station-list', request=request, format=format),
        'sensor': reverse('sensor-list', request=request, format=format),
        'area-log': reverse('area-log-list', request=request, format=format),
        'area-configuration': reverse('area-configuration-list', request=request, format=format)
    })


class IndexView(TemplateView):
    template_name = 'index.html'

