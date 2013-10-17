from django.conf.urls import patterns, url, include
from MoistureLog import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'Moisture_Event', views.Moisture_Event_ViewSet)
router.register(r'Weather_Data', views.Weather_Data_ViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
