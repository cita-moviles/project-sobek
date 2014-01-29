# Create your views here.
import django_filters
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import renderers
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.views.generic import TemplateView
from FieldApp.models import Crop, Farm_Field, Crop_Area, Valve, Weather_Station, Sensor, Crop_Area_Log, \
    Sensor_Log, Weather_Station_Log, Valve_Log
from FieldApp.serializers import Crop_Serializer, Farm_Field_Serializer, Area_Serializer, \
    Valve_Serializer, Station_Serializer, Sensor_Serializer, Area_Log_Serializer, Weather_Station_Log_Serializer, \
    Valve_Log_Serializer, Sensor_Log_Serializer


class Crop_ViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = Crop_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Field_ViewSet(viewsets.ModelViewSet):
    queryset = Farm_Field.objects.all()
    serializer_class = Farm_Field_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Area_ViewSet(viewsets.ModelViewSet):
    queryset = Crop_Area.objects.all()
    serializer_class = Area_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Valve_ViewSet(viewsets.ModelViewSet):
    queryset = Valve.objects.all()
    serializer_class = Valve_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Station_ViewSet(viewsets.ModelViewSet):
    queryset = Weather_Station.objects.all()
    serializer_class = Station_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class Sensor_ViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = Sensor_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


#Insert into LOGS

"""
class Area_Log_ViewSet(viewsets.ModelViewSet):
    queryset = Crop_Area_Log.objects.all()
    serializer_class = Area_Log_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
"""


#Filters
class AreaFilter(django_filters.FilterSet):
    class Meta:
        model = Crop_Area_Log
        fields = ['area_id', 'log_timestamp', 'area_ev']


class StationFilter(django_filters.FilterSet):
    class Meta:
        model = Weather_Station_Log
        fields = ['station_id', 'station_status', 'station_relative_humidity',
                  'station_temperature', 'station_wind_speed', 'station_solar_radiation']


class SensorFilter(django_filters.FilterSet):
    class Meta:
        model = Sensor_Log
        fields = ['sensor_id', 'sensor_status', 'sensor_hl1', 'sensor_hl2',
                  'sensor_hl3', 'sensor_temperature']


class ValveFilter(django_filters.FilterSet):
    class Meta:
        model = Valve_Log
        fields = ['valve_id', 'valve_status', 'valve_flow', 'valve_pressure', 'valve_limit']


class Area_Log_ViewSet(generics.ListCreateAPIView):
    queryset = Crop_Area_Log.objects.all()
    serializer_class = Area_Log_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = AreaFilter


class Station_Log_ViewSet(generics.ListCreateAPIView):
    queryset = Weather_Station_Log.objects.all()
    serializer_class = Weather_Station_Log_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = StationFilter


class Sensor_Log_ViewSet(generics.ListCreateAPIView):
    queryset = Sensor_Log.objects.all()
    serializer_class = Sensor_Log_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = SensorFilter


class Valve_Log_ViewSet(generics.ListCreateAPIView):
    queryset = Valve_Log.objects.all()
    serializer_class = Valve_Log_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = ValveFilter


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'crop': reverse('crop-list', request=request, format=format),
        'field': reverse('field-list', request=request, format=format),
        'area': reverse('area-list', request=request, format=format),
        'valve': reverse('valve-list', request=request, format=format),
        'station': reverse('station-list', request=request, format=format),
        'sensor': reverse('sensor-list', request=request, format=format),
        'area-log': reverse('area-log-list', request=request, format=format)
    })

class IndexView(TemplateView):
    template_name = 'index.html'