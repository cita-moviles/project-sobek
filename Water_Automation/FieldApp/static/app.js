/**
 * Created by Enrique Ramírez on 8/20/14.
 */

var use_agg;
/**
 * Helper Function that hides an element from the page.
 *
 * @param {String} tag_id the name of the container.
 * */
function hideTag(tag_id) {
    //TODO: add animation for more chrome!
    $('#' + tag_id).css('display', 'none');
}

/**
 * Helper Function that displays an element from the page.
 *
 * @param {String} tag_id the name of the container.
 * */
function showTag(tag_id) {
    //TODO: add animation for more chrome!
    $('#' + tag_id).css('display', 'block');
}


/**
 * Queries the web service for all the available Farm Fields in the application.
 *
 * @param {Function} callback The callback function in charge of processing and displaying the data.
 * */
function getFarmFields(callback) {
    //TODO: for future versions check for Farm Fields associated with an specific user.
    //TODO: Add optional values for error, and complete events.
    $.ajax({
        url: '/Farm_Field/',
        data: {},
        success: callback
    });
}

/**
 * Queries for all the Crop Areas available in the database.
 *
 * @param {Function}callback function in charge of processing and displaying the information.
 */
function getAreas(callback) {

    $.ajax({
        url: '/Crop_Area/',
        data: {},
        success: callback

    });

}

/**
 * Queries for the available areas for an specific field
 *
 *
 * @param {Number} field_id id number of the field to query for.
 * @param {Function} callback function in charge of processing and displaying the information.
 * */
function getAreasForField(field_id, callback) {

    $.ajax({

        url: '/Area_Search/',
        data: {fk_farm_field: field_id},
        success: callback

    });

}


/**
 * Retrieves all the available weather stations
 *
 * @param {Function}callback function in charge of processing and displaying the information.
 */
function getWeatherStations(callback) {

    $.ajax({
            url: '/Weather_Station/',
            data: {},
            success: callback
        }
    );

}


/**
 * Queries for the available weather stations for an specific field
 *
 *
 * @param {Number} field_id id number of the field to query for.
 * @param {Function} callback function in charge of processing and displaying the information.
 * */
function getWeatherStationForField(field_id, callback) {

    $.ajax({
        url: '/Station_Search/',
        data: {fk_farm_field: field_id},
        success: callback
    });

}

/**
 * Retrieves all the available sensors
 *
 * @param {Function}callback function in charge of processing and displaying the information.
 */
function getSensors(callback) {

    $.ajax({
        url: '/Sensor/',
        data: {},
        success: callback
    });

}

/**
 * Retrieves all the sensors for a given area
 *
 * @param {Number} area_id Identification number of the desired area
 * @param {Function} callback Function in charge of processing and displaying information
 * */
function getSensorsForArea(area_id, callback) {

    $.ajax({
        url: '/Sensor_Search/',
        data: {fk_area: area_id},
        success: callback
    });

}


/**
 * Retrieves all the Valves available
 *
 * @param {Function} callback callback function in charge of processing and displaying the information
 *
 * */
function getValves(callback) {

    $.ajax({
        url: '/Valve/',
        data: {},
        success: callback
    });

}


/**
 * Retrieves all the available valves for a given area.
 *
 * @param {Number} area_id Identification number of the desired area
 * @param {Function} callback Function in charge of processing and displaying information
 * */
function getValvesForArea(area_id, callback) {

    $.ajax({
        url: '/Valve_Search',
        data: {fk_area: area_id},
        success: callback

    });

}


/**
 * Gets the stored sensor logs of a specific sensor and a pair of dates.
 *
 * @param {Number} sensor_id Identification number of the sensor.
 *
 * @param {Date} start_date The initial date to look from
 * @param {Date} end_date The final date to look from
 * @param {Function} before_callback Callback function to be runned before the ajax request is executed.
 * @param {Function} success_callback Callback function that process and displays the information retrieved from ajax
 *
 * */
function getSensorLog(sensor_id, start_date, end_date,before_callback, success_callback) {

    $.ajax({
        url: "/Sensor_Log/",
        data: {
            sensor_id: sensor_id,
            min_date: start_date.dateFormat('Y-m-d H:i:s'),
            max_date: end_date.dateFormat('Y-m-d H:i:s'),
            ordering: "-sensor_date_received"
        },
        beforeSend: before_callback,
        success: function (data) {

            var moisture_array = [];
            moisture_array.push(['Time', 'HL1', 'HL2', 'HL3']);

            if (data.length == 0) {
                moisture_array.push([end_date.dateFormat('Y-m-d H:i:s'),
                    0, 0, 0]);
            } else {
                $.each(data, function (index, value) {
                    var date_received = new Date(Date.parse(value.sensor_date_received));
                    var temp_array = [];
                    temp_array.push(date_received);
                    temp_array.push(value.sensor_hl1);
                    temp_array.push(value.sensor_hl2);
                    temp_array.push(value.sensor_hl3);
                    moisture_array.push(temp_array);

                });
            }

            var data_moisture = google.visualization.arrayToDataTable(moisture_array);

            var chart_moisture = new google.visualization.LineChart(document.getElementById('moisture_chart'));

            var options = {
                title: 'Soil Moisture',
                smoothLine: true
            };

            $('#progress_message').text("Done!");
            $('#progress').animate({width: 100});
            chart_moisture.draw(data_moisture, options);

        }
    });

}

/**
 * Callback function that displays the loading section of the page
 * */
function displayLoading() {
    $('#progress').animate({width: 0});
    $('#progress_message').text("Loading");
    //$('#spinner').css('display', 'inline-block');

}

/**
 * Callback function that hides the loading section of the page
 * */
function hideLoading() {
    $('#progress_message').text("Done!");
    $('#progress').animate({width: 100});
    //$('#spinner').css('display', 'none');
}


/**
 * Initializes the date pickers with the proper configuration for the app.
 *
 *  @param {String} from_picker The id of the picker for the starting date.
 * @param {String} to_picker
 *
 * */
function initDatePickers(from_picker, to_picker) {
    var init_date;
    var end_date;
    from = from_picker;
    to = to_picker;
    from = jQuery(from_picker).datetimepicker({

        closeOnDateSelect: true,
        defaultChecked: true,
        onSelectDate: function (current_time, $input) {
            init_date = current_time.dateFormat('Y-m-d H:i:s');
        }

    });
    to = jQuery(to_picker).datetimepicker({
        closeOnDateSelect: true,
        defaultChecked: true,
        onSelectDate: function (current_time, $input) {
            end_date = current_time.dateFormat('Y-m-d H:i:s');

        }
    });

    return [init_date, end_date]

}

/**
 * Create a date object for the past 6 and 24 hours or for last 7,15 and 30 days.
 *
 * @param {Number} option 1 = 6 hours, 2 = 24 hours, 3 = 7 days, 4 = 15 days, 5 = 30 days.
 * */

function quick_date(option) {
    init_date = new Date();
    end_date = new Date();

    switch (option) {

        case 1: //6 hours
            init_date.setHours(end_date.getHours() - 6);
            use_agg=0;
            break;

        case 2: //24 hours
            init_date.setHours(end_date.getHours() - 24);
            use_agg=0;
            break;

        case 3: //7 days
            init_date.setDate(end_date.getDate() - 7);
            use_agg=0;
            break;

        case 4: //15 days
            init_date.setDate(end_date.getDate() - 15);
            use_agg=1;
            break;

        case 5: //30 days
            init_date.setDate(end_date.getDate() - 30);
            use_agg=1;
            break;
    }
    from.datetimepicker({
        value: init_date.dateFormat('Y-m-d H:i:s')
    });
    to.datetimepicker({
        value: end_date.dateFormat('Y-m-d H:i:s')
    });
    console.log(use_agg);
    return use_agg;
    graphLogs();

}

/**
 * Gets current weather data from /Weather_Station/ Web service
 *
 * @param {Number} station_id The Id of the station to be retreived
 * @oaran {Function} Callback callback Function in charge of processing the JSON from web service
 * */
function getAjaxWeatherData(station_id) {
    $.ajax({
        url: '/Weather_Station/'+station_id,
    success: function (data){
        weatherCallback(data);
    }

    });
}

/**
 * Callback function in charge of processing and displaying the data on the corresponding tags
 *
 * @param data JSON Retreived from the web service
 * */
function weatherCallback(data) {

        var date_received = '';
        var dr = new Date(Date.parse(data.station_date_received));
        date_received = dr.toLocaleString();

        // Getting Data from received JSON
        var station_id = "<p>Station ID: "+ data.station_id + "</p>";
        var date = "<p>Date received: "+ date_received + "</p>"
        var station_name = "<p>Station Name: "+data.station_name + "</p>";
        var relative_humidity = "<p>Humidity: "+(data.station_relative_humidity + '%')+ "</p>";
        var radiation = "<p>Radiation: "+ (data.station_solar_radiation + " W&frasl;m<sup>2</sup>")+ "</p>";
        var status = "<p>Status: " + data.station_status + "</p>";
        var temperature = "<p>Temperature: " + (data.station_temperature + ' ºC')+ "</p>";
        var wind_speed = "<p>Wind Speed: "+ (data.station_wind_speed + " m&frasl;s")+ "</p>";
        var rain = "<p>Rain: " + (data.station_user_define1 + " mm")+ "</p>";
        //var battery_level = data.station_user_define1;

        // Selecting the tags
        var id_tag = $('#station_data');
        var date_tag = $('#date_data');
        var humidity_tag = $('#humidity_data');
        var radiation_tag = $('#radiation_data');
        var status_tag = $('#status_data');
        var temperature_tag = $('#temperature_data');
        var wind_tag = $('#wind_data');
        var rain_tag = $('#rain_data');
        var battery_tag = $('#battery_data');


        // Asign data received to tags
        id_tag.html(station_id);
        date_tag.html(date);
        humidity_tag.html(relative_humidity);
        radiation_tag.html(radiation);

        if (data.station_status === 0) {
            status_tag.html('<p>Status: OK</p>');
        } else {
            status_tag.html('<p>Status: Communication Error</p>');
        }


        temperature_tag.html(temperature);
        wind_tag.html(wind_speed);
        //battery_tag.append(battery_level);
        rain_tag.html(rain);

}


/**
 * Requests the ajax data and displays the graphs in their corresponding container
 *
 * @param {String} start Starting date for the request
 * @param {String} end The final date for the request, most of the time is the current date.
 * @param {Function} callback Function that will handle the data retrieved from the web service
 *
 * */
function getSensorLogs(start, end, callback) {
    var sensor_id = $('#sensor').val();

    $.ajax({
        url: "/Sensor_Log/",
        data: {
            sensor_id: sensor_id,
            min_date: start.dateFormat('Y-m-d H:i:s'),
            max_date: end.dateFormat('Y-m-d H:i:s'),
            ordering: "-sensor_date_received"
        },
        beforeSend: displayLoading,
        success: callback
    });

}

/**
 * Requests the Evotranspiration log data from the web service
 *
 * @param {Number} area_id Identification number for the area.
 * @param {String} start_date Starting date for the request
 * @param {String} end_date The final date for the request, most of the time is the current date.
 * @param {Function} callback Function that will handle the data retrieved from the web service
 * */
function getEvotranspirationLog(area_id, start_date, end_date, callback) {
    var evo_graph_data;
    //PRUEBA:
    //console.log(sensor_id);
    /*if (use_agg===0){
        evo_graph_data= "/Crop_Area_Log/";
    }
    else {
        evo_graph_data= "/Crop_Area_Agg/";
    } */
    evo_graph_data = "/Crop_Area_Log/";
    $.ajax({
        url: evo_graph_data,
        data: {
            area_id: area_id,
            min_date: start_date.dateFormat('Y-m-d H:i:s'),
            max_date: end_date.dateFormat('Y-m-d H:i:s'),
            ordering: "-area_date_received"
        },

        success: callback
    });


}

/**
 * Request the Valve log from the web services
 * @param {Number} sensor_id Identification number for the sensor.
 * @param {String} start_date Starting date for the request
 * @param {String} end_date The final date for the request, most of the time is the current date.
 * @param {Function} callback Function that will handle the data retrieved from the web service
 * */
function getValveLog(valve_id, start_date, end_date, callback) {

    $.ajax({
        url: "/Valve_Log/",
        data: {
            valve_id: valve_id,
            min_date: start_date.dateFormat('Y-m-d H:i:s'),
            max_date: end_date.dateFormat('Y-m-d H:i:s'),
            ordering: "-valve_date_received"
        },
        success: callback

    });

}

/**
 * Gets the current information for all the valves of a given area
 *
 *
 * */
function getCurrentValves(area_id, callback) {
    $.ajax({
        url: "/Valve_Search/",
        data: { fk_area: area_id},
        success: callback
    });
}

/**
 * Return Final date
 * */

function getStartingDate(option) {

    var init_date = new Date();
    var end_date = new Date();

    switch (option) {

        case 1: //6 hours
            init_date.setHours(end_date.getHours() - 6);
            break;

        case 2: //24 hours
            init_date.setHours(end_date.getHours() - 24);
            break;

        case 3: //7 days
            init_date.setDate(end_date.getDate() - 7);
            break;

        case 4: //15 days
            init_date.setDate(end_date.getDate() - 15);
            break;

        case 5: //30 days
            init_date.setDate(end_date.getDate() - 30);
            break;
    }

    return init_date;
}

