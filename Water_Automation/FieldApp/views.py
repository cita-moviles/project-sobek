# Create your views here.
from FieldApp.models import Crop, Farm_Field, Crop_Area, Valve, Weather_Station, Sensor
from FieldApp.serializers import Crop_Serializer, Farm_Field_Serializer, Area_Serializer, \
    Valve_Serializer, Station_Serializer, Sensor_Serializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from django.views.generic import TemplateView


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

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'crop': reverse('crop-list', request=request, format=format),
        'field': reverse('field-list', request=request, format=format),
        'area': reverse('area-list', request=request, format=format),
        'valve': reverse('valve-list', request=request, format=format),
        'station': reverse('station-list', request=request, format=format),
        'sensor': reverse('sensor-list', request=request, format=format)
    })

class IndexView(TemplateView):
    template_name = 'index.html'