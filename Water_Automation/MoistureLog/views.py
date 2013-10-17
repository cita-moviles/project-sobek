from MoistureLog.models import Moisture_Event, Weather_Data
from MoistureLog.serializers import Moisture_Event_Serializer, Weather_Data_Serializer
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets


class Moisture_Event_ViewSet(viewsets.ModelViewSet):
    queryset = Moisture_Event.objects.all()
    serializer_class = Moisture_Event_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class Weather_Data_ViewSet(viewsets.ModelViewSet):
    queryset = Weather_Data.objects.all()
    serializer_class = Weather_Data_Serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'moisture': reverse('moisture-list', request=request, format=format),
        'weather': reverse('weather-list', request=request, format=format)
    })