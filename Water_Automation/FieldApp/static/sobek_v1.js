/**
 * Created by luishoracio on 24/01/14.
 */

var from; // picker variables
var to; // picker variables


function hideTag(container) {
    $('#' + container).css('display', 'none')
}

function showTag(container) {
    $('#' + container).css('display', 'block')
}


/**
 * Retrieves the available fields on the Database.
 *
 * @param {String} select_id id of the Selector containing hte fields available
 * @param {String} field2 id of the next available selector
 * @param {String} field3 id of the third selector if empty must use ""
 *
 * */
function getAjaxFarmFields(select_id, field2, field3) {
    $.ajax({
        url: "/Farm_Field/",
        data: { },
        success: function (data) {
            options = "";

            $.each(data, function (index, value) {
                options += '<option value="' + value.field_id + '">' + value.field_name + '</option>';
            });

            $('#' + select_id).html(options);

            if (field2 === 'area') {
                getAreas(field2, select_id, field3);
            }

            if (field2 === 'station') {
                $('#current_station').html("");
                getStationCurrentData(field2, select_id);
            }

            if (field2 === '') {
                $('#current_area').html("");
            }

        }
    });
}

function getAreasOptions(select_id) {
    $.ajax({
        url: "/Crop_Area/",
        data: { },
        success: function (data) {
            options = "";

            $.each(data, function (index, value) {
                options += '<option value="' + value.area_id + '">' + value.area_name + '</option>';
            });

            $('#' + select_id).html(options);
        }
    });
}

function getAreas(select_id, search_id, field2) {
    $.ajax({
        url: "/Area_Search/",
        data: {fk_farm_field: $('#' + search_id).val() },
        success: function (data) {
            var options = "";
            var current_data = "";

            $.each(data, function (index, value) {

                var date_received = "";
                if (value.area_date_received !== "") {
                    var dr = new Date(Date.parse(value.area_date_received));
                    date_received = dr.toLocaleString();
                }

                options += '<option value="' + value.area_id + '">' + value.area_name + '</option>';
                current_data += "<h4>Area: " + value.area_id + "</h4>";
                current_data += "Evotranspiration: " + value.area_ev + "<br/>";
                current_data += "Date: " + date_received + "</p>";
            });

            $('#' + select_id).html(options);

            if (field2 === 'sensor') {
                $('#current_sensor').html("");
                getSensors(field2, select_id);
            }

            if (field2 === 'valve') {
                $('#current_valve').html("");
                getValves(field2, select_id)
            }

            if (field2 === '') {
                $('#current_area').html(current_data);
            }

        }
    });
}

function getStationsOptions(select_id) {
    $.ajax({
        url: "/Weather_Station/",
        data: { },
        success: function (data) {
            var options = "";

            $.each(data, function (index, value) {
                options += '<option value="' + value.station_id + '">' + value.station_id + '</option>';
            });

            $('#' + select_id).html(options);
        }
    });
}

function getStationCurrentData(select_id, search_id) {
    var options = "";
    var current_data = "";
    $.ajax({
        url: "/Station_Search/",
        data: { fk_farm_field: $('#' + search_id).val()},
        success: function (data) {


            $.each(data, function (index, value) {

                var date_received = "";
                if (value.station_date_received !== "") {
                    var dr = new Date(Date.parse(value.station_date_received));
                    date_received = dr.toLocaleString();
                }

                options += '<option value="' + value.station_id + '">' + value.station_id + '</option>';
                current_data += "<h4>Station: " + value.station_id + "</h4>";
                current_data += "<p>Status: " + value.station_status + "<br/>";
                current_data += "Relative Humidity: " + value.station_relative_humidity + "<br/>";
                current_data += "Temperature: " + value.station_temperature + "<br/>";
                current_data += "Wind Speed: " + value.station_wind_speed + "<br/>";
                current_data += "Solar Station: " + value.station_solar_radiation + "<br/>";
                current_data += "Date: " + date_received + "</p>";
            });

            $('#' + select_id).html(options);
            $('#current_station').html(current_data);
        }
    });

    return current_data;
}

function getSensorsOptions(select_id) {
    $.ajax({
        url: "/Sensor/",
        data: { },
        success: function (data) {
            var options = "";

            $.each(data, function (index, value) {
                options += '<option value="' + value.sensor_id + '">' + value.sensor_id + '</option>';
            });

            $('#' + select_id).html(options);
        }
    });
}

function getSensors(select_id, search_id) {
    area = $('#' + search_id).val();

    if (area === null) {
        $('#' + select_id).html("");
        return
    }
    $.ajax({
        url: "/Sensor_Search/",
        data: { fk_area: area},
        success: function (data) {
            var options = "";
            var current_data = "";

            $.each(data, function (index, value) {

                var date_received = "";
                if (value.sensor_date_received !== "") {
                    var dr = new Date(Date.parse(value.sensor_date_received));
                    date_received = dr.toLocaleString();
                }

                options += '<option value="' + value.sensor_id + '">' + value.sensor_id + '</option>';
                current_data += "<h4>Sensor: " + value.sensor_id + "</h4>";
                current_data += "<p>Level 1: " + value.sensor_hl1 + "<br/>";
                current_data += "Level 2: " + value.sensor_hl2 + "<br/>";
                current_data += "Level 3: " + value.sensor_hl3 + "<br/>";
//                current_data += "Temperature: " + value.sensor_temperature + "<br/>";
                current_data += "Date: " + date_received + "</p>";
            });

            $('#' + select_id).html(options);
            $('#current_sensor').html(current_data);
        }
    });
}

function getValvesOptions(select_id) {
    $.ajax({
        url: "/Valve/",
        data: { },
        success: function (data) {
            var options = "";

            $.each(data, function (index, value) {
                options += '<option value="' + value.valve_id + '">' + value.valve_id + '</option>';
            });

            $('#' + select_id).html(options);
        }
    });
}

function getValves(select_id, search_id) {
    area = $('#' + search_id).val();

    if (area === null) {
        $('#' + select_id).html("");
        return
    }
    $.ajax({
        url: "/Valve_Search/",
        data: { fk_area: area},
        success: function (data) {
            var options = "";
            var current_data = "";

            $.each(data, function (index, value) {

                var date_received = "";
                if (value.valve_date_received !== "") {
                    var dr = new Date(Date.parse(value.valve_date_received));
                    date_received = dr.toLocaleString();
                }

                options += '<option value="' + value.valve_id + '">' + value.valve_id + '</option>';
                current_data += "<h4>Valve: " + value.valve_id + "</h4>";
                current_data += "<p>Actuator: " + value.valve_user_define1 + "<br/>";
                current_data += "Status: " + value.valve_status + "<br/>";
                current_data += "Flow: " + value.valve_flow + "<br/>";
                current_data += "Pressure: " + value.valve_pressure + "<br/>";
                current_data += "Date: " + date_received + "</p>";
            });

            $('#' + select_id).html(options);
            $('#current_valve').html(current_data);
        }
    });
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

    from.datetimepicker({
        value: init_date.dateFormat('Y-m-d H:i:s')
    });
    to.datetimepicker({
        value: end_date.dateFormat('Y-m-d H:i:s')
    });

    graphLogs();

}

/**
 * Gets current weather data from /Weather_Station/ Web service
 *
 * @param {Number} station_id The Id of the station to be retreived
 * @oaran {Function} Callback callback Function in charge of processing the JSON from web service
 * */
function getAjaxWeatherData(station_id, callback) {
    $.ajax({
        url: '/Weather_Station/' + station_id,

        success: callback});
}


/**
 * Callback function in charge of processing and displaying the data on the corresponding tags
 *
 * @param data JSON Retreived from the web service
 * */
function weatherCallback(data) {
    var date_received = '';
    if (data.station_date_received !== '') {
        var dr = new Date(Date.parse(data.station_date_received));
        date_received = dr.toLocaleString();

    }

    // Getting Data from received JSON
    var station_id = data.station_id;
    var station_name = data.station_name;
    var relative_humidity = data.station_relative_humidity;
    var radiation = data.station_solar_radiation;
    var status = data.station_status;
    var temperature = data.station_temperature;
    var wind_speed = data.station_wind_speed;
    var battery_level = data.station_user_define1;


    // Selecting the tags
    var id_tag = $('#station_data');
    var date_tag = $('#date_data');
    var humidity_tag = $('#humidity_data');
    var radiation_tag = $('#radiation_data');
    var status_tag = $('#status_data');
    var temperature_tag = $('#temperature_data');
    var wind_tag = $('#wind_data');
    var battery_tag = $('#battery_data');


    // Asign data received to tags
    id_tag.append(station_id);
    date_tag.append(date_received);
    humidity_tag.append(relative_humidity);
    radiation_tag.append(radiation);
    status_tag.append(status);
    temperature_tag.append(temperature);
    wind_tag.append(wind_speed);
    battery_tag.append(battery_level);


}


