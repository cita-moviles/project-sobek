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
                getStations(field2, select_id);
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
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.area_id + '">' + value.area_name + '</option>';
            });

            $('#'+select_id).html(options);

            if (field2 === 'sensor'){
                getSensors(field2,select_id);
            }
            if (field2 === 'valve'){
                getValves(field2, select_id )
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
                options += '<option value="' + value.station_id + '">' + value.station_name + '</option>';
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
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.station_id + '">' + value.station_name + '</option>';
            });

            $('#'+select_id).html(options);
        }
    });
}

function getSensors(select_id){
    $.ajax({
        url: "/Sensor/",
        data: { },
        success:function(data){
            options = "";

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
            options = "";

            $.each(data, function( index, value ) {
                options += '<option value="' + value.valve_id + '">' + value.valve_id + '</option>';
            });

            $('#'+select_id).html(options);
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

/*
function getAreasEv(){
    $.ajax({
        url: "/Moisture_Event/",
        data: { },
        success:function(data){
            time_array =[];
            ev_array = [];
            $.each(data, function( index, value ) {

                time_array.push(value.log_timestamp);
                ev_array.push(value.area_ev);
            });

            var evChart = {
                labels : time3_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : moisture3_array
                    }
                ]
            }
            var weather_lineChart = new Chart(document.getElementById("weather_canvas").getContext("2d")).Line(lineChartData);
        }
    });
}
*/
function graph(){
    $.ajax({
        url: "/Moisture_Event/",
        data: { },
        success: function( data ) {
            time_array =[];
            moisture_array=[];
            min_array=[];
            max_array=[];
            actuator_array = [];
            height_array = [];

            moisture1_array = [];
            moisture2_array = [];
            moisture3_array = [];

            time1_array = [];
            time2_array = [];
            time3_array = [];

            $.each(data, function( index, value ) {
                time_array.push(value.date);
                moisture_array.push(value.moisture);
                min_array.push(value.min);
                max_array.push(value.max);
                actuator_array.push(value.actuator_state);
                height_array.push(value.height);

                switch (value.height){
                    case 1:
                        moisture1_array.push(value.moisture);
                        time1_array.push(value.date);
                        break;
                    case 2:
                        moisture2_array.push(value.moisture);
                        time2_array.push(value.date);
                        break;
                    case 3:
                        moisture3_array.push(value.moisture);
                        time3_array.push(value.date);
                        break;
                }
            });

            /*var lineChartData = {
                labels : time_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : max_array
                    },
                    {
                        fillColor : "rgba(220,220,220,0.5)",
                        strokeColor : "rgba(220,220,220,1)",
                        pointColor : "rgba(220,220,220,1)",
                        pointStrokeColor : "#fff",
                        data : moisture_array
                    },
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        pointColor : "rgba(151,187,205,1)",
                        pointStrokeColor : "#fff",
                        data : min_array
                    }
                ]

            }

            var lineChartData = {
                labels : time_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : height_array
                    },
                    {
                        fillColor : "rgba(220,220,220,0.5)",
                        strokeColor : "rgba(220,220,220,1)",
                        pointColor : "rgba(220,220,220,1)",
                        pointStrokeColor : "#fff",
                        data : moisture_array
                    }
                ]
            }*/


            var height1Chart = {
                labels : time1_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : moisture1_array
                    }
                ]
            }

            var height2Chart = {
                labels : time2_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : moisture2_array
                    }
                ]
            }

            var height3Chart = {
                labels : time3_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : moisture3_array
                    }
                ]
            }

            var actuatorChartData = {
                labels : time_array,
                datasets : [
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        pointColor : "rgba(151,187,205,1)",
                        pointStrokeColor : "#fff",
                        data : actuator_array
                    }
                ]

            }

            //var moisture_lineChart = new Chart(document.getElementById("moisture_canvas").getContext("2d")).Line(lineChartData);
            var moisture1_lineChart = new Chart(document.getElementById("moisture1_canvas").getContext("2d")).Line(height1Chart);
            var moisture2_lineChart = new Chart(document.getElementById("moisture2_canvas").getContext("2d")).Line(height2Chart);
            var moisture3_lineChart = new Chart(document.getElementById("moisture3_canvas").getContext("2d")).Line(height3Chart);
            var actuator_lineChart = new Chart(document.getElementById("actuator_canvas").getContext("2d")).Line(actuatorChartData);
        }
    });

    $.ajax({
        url: "/Weather_Data/",
        data: {
        },
        success: function( data ) {

            time_array = [];
            temperature_array = [];
            solar_array = [];
            windspeed_array = [];
            humidity_array = [];
            airpressure_array = [];
            et_array = [];

            $.each(data, function( index, value ) {
                time_array.push(value.date);
                temperature_array.push(value.temperature);
                solar_array.push(value.solar_intensity);
                windspeed_array.push(value.windspeed);
                humidity_array.push(value.humidity);
                airpressure_array.push(value.air_pressure);
                et_array.push(value.ET);
            });

            var lineChartData = {
                labels : time_array,
                datasets : [
                    {
                        fillColor : "rgba(204,0,0,0.5)",
                        strokeColor : "rgba(204,0,0,1)",
                        pointColor : "rgba(204,0,0,1)",
                        pointStrokeColor : "#fff",
                        data : temperature_array
                    },
                    {
                        fillColor : "rgba(220,220,220,0.5)",
                        strokeColor : "rgba(220,220,220,1)",
                        pointColor : "rgba(220,220,220,1)",
                        pointStrokeColor : "#fff",
                        data : solar_array
                    },
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        pointColor : "rgba(151,187,205,1)",
                        pointStrokeColor : "#fff",
                        data : windspeed_array
                    },
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        pointColor : "rgba(151,187,205,1)",
                        pointStrokeColor : "#fff",
                        data : humidity_array
                    },
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        pointColor : "rgba(151,187,205,1)",
                        pointStrokeColor : "#fff",
                        data : airpressure_array
                    },
                    {
                        fillColor : "rgba(151,187,205,0.5)",
                        strokeColor : "rgba(151,187,205,1)",
                        pointColor : "rgba(151,187,205,1)",
                        pointStrokeColor : "#fff",
                        data : et_array
                    }
                ]

            }

            var weather_lineChart = new Chart(document.getElementById("weather_canvas").getContext("2d")).Line(lineChartData);
        }
    });

}