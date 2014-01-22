from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from MoistureLog import views
from FieldApp import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'Moisture_Event', views.Moisture_Event_ViewSet)
# router.register(r'Weather_Data', views.Weather_Data_ViewSet)
router.register(r'Crop', views.Crop_ViewSet)
router.register(r'Farm_Field', views.Field_ViewSet)
router.register(r'Crop_Area', views.Area_ViewSet)
router.register(r'Valve',views.Valve_ViewSet)
router.register(r'Weather_Station', views.Station_ViewSet)
router.register(r'Sensor', views.Sensor_ViewSet)

urlpatterns = patterns('',
    url(r'^index.html', TemplateView.as_view(template_name="index.html")),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
