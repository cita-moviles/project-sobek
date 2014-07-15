/**
 * Created by luishoracio on 24/01/14.
 */

function navigate(adress){
    window.location.replace(adress);
}

function hideTag(container){
    $('#' + container).css('display','none')
}

function showTag(container){
    $('#' + container).css('display','block')
}

function getFields(select_id, field2, field3){
    $.ajax({
        url: "/Farm_Field/",
        data: { },
        success:function(data){
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.field_id + '">' + value.field_name + '</option>';
            });

            $('#'+select_id).html(options);

            if (field2 === 'area'){
                getAreas(field2, select_id, field3);
            }

            if (field2 === 'station'){
                $('#current_station').html("");
                getStations(field2, select_id);
            }

            if (field2 === ''){
                $('#current_area').html("");
            }

        }
    });
}

function getAreas(select_id){
    $.ajax({
        url: "/Crop_Area/",
        data: { },
        success:function(data){
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.area_id + '">' + value.area_name + '</option>';
            });

            $('#'+select_id).html(options);
        }
    });
}

function getAreas(select_id, search_id, field2){
    $.ajax({
        url: "/Area_Search/",
        data: {fk_farm_field: $('#' + search_id).val() },
        success:function(data){
            var options = "";
            var current_data = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.area_id + '">' + value.area_name + '</option>';
                current_data += "<h4>Area: " + value.area_id + "</h4>";
                current_data += "Evotranspiration: " + value.area_ev + "<br/>";
                current_data += "Date: " + value.area_date_received + "</p>";
            });

            $('#'+select_id).html(options);

            if (field2 === 'sensor'){
                $('#current_sensor').html("");
                getSensors(field2,select_id);
            }

            if (field2 === 'valve'){
                $('#current_valve').html("");
                getValves(field2, select_id )
            }

            if (field2 === ''){
                $('#current_area').html(current_data);
            }

        }
    });
}

function getStations(select_id){
    $.ajax({
        url: "/Weather_Station/",
        data: { },
        success:function(data){
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.station_id + '">' + value.station_id + '</option>';
            });

            $('#'+select_id).html(options);
        }
    });
}

function getStations(select_id, search_id){
    $.ajax({
        url: "/Station_Search/",
        data: { fk_farm_field: $('#' + search_id).val()},
        success:function(data){
            var options = "";
            var current_data = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.station_id + '">' + value.station_id + '</option>';
                current_data += "<h4>Station: " + value.station_id + "</h4>";
                current_data += "<p>Status: " + value.station_status + "<br/>";
                current_data += "Relative Humidity: " + value.station_relative_humidity + "<br/>";
                current_data += "Temperature: " + value.station_temperature + "<br/>";
                current_data += "Wind Speed: " + value.station_wind_speed + "<br/>";
                current_data += "Solar Station: " + value.station_solar_radiation + "<br/>";
                current_data += "Date: " + value.sensor_date_received + "</p>";
            });

            $('#'+select_id).html(options);
            $('#current_station').html(current_data);
        }
    });
}

function getSensors(select_id){
    $.ajax({
        url: "/Sensor/",
        data: { },
        success:function(data){
            var options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.sensor_id + '">' + value.sensor_id + '</option>';
            });

            $('#'+select_id).html(options);
        }
    });
}

function getSensors(select_id, search_id){
    area = $('#'+ search_id).val();

    if (area === null){
        $('#'+select_id).html("");
        return
    }
    $.ajax({
        url: "/Sensor_Search/",
        data: { fk_area: area},
        success:function(data){
            var options = "";
            var current_data = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.sensor_id + '">' + value.sensor_id + '</option>';
                current_data += "<h4>Sensor: " + value.sensor_id + "</h4>";
                current_data += "<p>Level 1: " + value.sensor_hl1 + "<br/>";
                current_data += "Level 2: " + value.sensor_hl2 + "<br/>";
                current_data += "Level 3: " + value.sensor_hl3 + "<br/>";
                current_data += "Temperature: " + value.sensor_temperature + "<br/>";
                current_data += "Date: " + value.sensor_date_received + "</p>";
            });

            $('#'+select_id).html(options);
            $('#current_sensor').html(current_data);
        }
    });
}

function getValves(select_id){
    $.ajax({
        url: "/Valve/",
        data: { },
        success:function(data){
            var options = "";
            var current_data = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.valve_id + '">' + value.valve_id + '</option>';
                current_data += "<h4>Valve: " + value.valve_id + "</h4>";
                current_data += "<p>Actuator: " + value.valve_user_define_1 + "<br/>";
                current_data += "Status: " + value.valve_status + "<br/>";
                current_data += "Flow: " + value.valve_flow + "<br/>";
                current_data += "Pressure: " + value.valve_pressure + "</p>";
            });

            $('#'+select_id).html(options);
            $('#current_valve').html(current_data);
        }
    });
}

function getValves(select_id, search_id){
    area = $('#'+ search_id).val();

    if (area === null){
        $('#'+select_id).html("");
        return
    }
    $.ajax({
        url: "/Valve_Search/",
        data: { fk_area: area},
        success:function(data){
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.valve_id + '">' + value.valve_id + '</option>';
            });

            $('#'+select_id).html(options);
        }
    });
}