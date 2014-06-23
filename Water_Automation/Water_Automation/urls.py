from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from MoistureLog import views
from FieldApp import views

from django.contrib import admin
admin.autodiscover()

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'Crop', views.Crop_ViewSet)
router.register(r'Farm_Field', views.Field_ViewSet)
router.register(r'Crop_Area', views.Area_ViewSet)
router.register(r'Valve', views.Valve_ViewSet)
router.register(r'Weather_Station', views.Station_ViewSet)
router.register(r'Sensor', views.Sensor_ViewSet)

# router.register(r'Moisture_Event', views.Moisture_Event_ViewSet)
# router.register(r'Weather_Data', views.Weather_Data_ViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^Field_Search/', views.FieldSearch.as_view(model='Farm_Field')),
    url(r'^Sensor_Search/', views.SensorSearch.as_view(model='Sensor')),
    url(r'^Area_Search/', views.AreaSearch.as_view(model='Crop_Area')),
    url(r'^Station_Search/', views.StationSearch.as_view(model='Weather_Station')),
    url(r'^Valve_Search/', views.ValveSearch.as_view(model='Valve')),

    url(r'^Crop_Area_Log/', views.Area_Log_ViewSet.as_view(model='Crop_Area_Log')),
    url(r'^Sensor_Log/', views.Sensor_Log_ViewSet.as_view(model='Sensor_Log')),
    url(r'^Valve_Log/', views.Valve_Log_ViewSet.as_view(model='Valve_Log')),
    url(r'^Station_Log/', views.Station_Log_ViewSet.as_view(model='Weather_Station_Log')),
    url(r'^Farm_Field_Log/', views.Farm_Field_Log_ViewSet.as_view(model='Farm_Field_Log')),

    url(r'^index.html', TemplateView.as_view(template_name="index.html")),
    url(r'^sensor.html', TemplateView.as_view(template_name="sensor.html")),
    url(r'^valve.html', TemplateView.as_view(template_name="valve.html")),
    url(r'^station.html', TemplateView.as_view(template_name="station.html")),
    url(r'^area.html', TemplateView.as_view(template_name="area.html")),
    url(r'^configuration.html', TemplateView.as_view(template_name="configuration.html")),
    url(r'^admin/', include(admin.site.urls))
)
