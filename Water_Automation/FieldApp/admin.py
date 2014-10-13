__author__ = 'Enrique Ramirez'

from django.contrib import admin
from models import Crop, Crop_Area, Farm_Field, Sensor, Valve, Weather_Station, Area_Configuration


class CropAdmin(admin.ModelAdmin):
    # Configure which parameters to display and configure on the admin screen
    fields = [

        'crop_id',
        'crop_name',
        'crop_description',
        'crop_ev',
        'crop_user_define1',
        'crop_user_define2'

    ]
    # Define how will appear the list of crops on the admin screen
    list_display = ('crop_id', 'crop_name')


class AreaAdmin(admin.ModelAdmin):
    fields = [

        'area_id',
        'area_name',
        'area_description',
        'area_ev',
        'area_x_position',
        'area_y_position',
        'area_date_received',
        'area_user_define1',
        'area_user_define2',
        'fk_farm_field',
        'fk_crop'

    ]

    list_display = ('area_id', 'area_name', 'area_date_received', 'fk_farm_field', 'fk_crop')


class FieldAdmin(admin.ModelAdmin):
    fields = [

        'field_id',
        'field_name',
        'field_description',
        'field_imei',
        'field_latitude',
        'field_longitude',
        'field_date_received',
        'field_user_define1',
        'field_user_define2'

    ]

    list_display = ('field_id', 'field_name', 'field_imei',)


class SensorAdmin(admin.ModelAdmin):
    fields = [

        'sensor_id',
        'sensor_name',
        'sensor_status',
        'sensor_x_position',
        'sensor_y_position',
        'sensor_user_define1',
        'sensor_user_define2',
        'sensor_date_received',
        'fk_area'

    ]
    list_display = ('sensor_id', 'sensor_name', 'sensor_status', 'sensor_date_received', 'fk_area')


class ValveAdmin(admin.ModelAdmin):
    fields = [

        'valve_id',
        'valve_name',
        'valve_limit',
        'valve_ideal',
        'valve_status',
        'valve_flow',
        'valve_date_received',
        'valve_user_define1',
        'valve_user_define2',
        'fk_area',

    ]

    list_display = ('valve_id', 'valve_name', 'valve_limit', 'valve_ideal', 'valve_date_received', 'fk_area')


class StationAdmin(admin.ModelAdmin):
    fields = [

        'station_id',
        'station_name',
        'station_date_received',
        'station_user_define1',
        'station_user_define2',
        'fk_farm_field'

    ]

    list_display = ('station_id', 'station_name', 'station_date_received', 'fk_farm_field')


class ConfigAdmin(admin.ModelAdmin):
    fields = [

        'area_id',
        'area_configuration'
    ]

    list_display = ('area_id',)


# Register all the models for admin
admin.site.register(Crop, CropAdmin)
admin.site.register(Crop_Area, AreaAdmin)
admin.site.register(Farm_Field, FieldAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(Valve, ValveAdmin)
admin.site.register(Weather_Station, StationAdmin)
admin.site.register(Area_Configuration, ConfigAdmin)