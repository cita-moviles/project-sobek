CREATE OR REPLACE FUNCTION fai_sensor() RETURNS TRIGGER AS $fai_sensor$
BEGIN 
	INSERT INTO "FieldApp_sensor_log"
		(log_timestamp, sensor_id_id, sensor_status, sensor_hl1, sensor_hl2, sensor_hl3, sensor_temperature)
	VALUES
	  (now(), NEW.sensor_id, NEW.sensor_status, NEW.sensor_hl1, NEW.sensor_hl2, NEW.sensor_hl3, NEW.sensor_temperature);

	RETURN NEW;
END;
$fai_sensor$ LANGUAGE plpgsql;

CREATE TRIGGER tai_sensor 
	AFTER INSERT OR UPDATE 
	ON "FieldApp_sensor"
	FOR EACH ROW 
	EXECUTE PROCEDURE fai_sensor();

	--
CREATE OR REPLACE FUNCTION fai_valve() RETURNS TRIGGER AS $fai_valve$
BEGIN
	INSERT INTO "FieldApp_valve_log"
		(log_timestamp, valve_id_id, valve_status, valve_flow, valve_pressure, valve_limit)
	VALUES
	  (now(), NEW.valve_id, NEW.valve_status, NEW.valve_flow, NEW.valve_pressure, NEW.valve_limit);
	RETURN new;
END;
$fai_valve$ LANGUAGE plpgsql;

CREATE TRIGGER tai_valve
	AFTER INSERT OR UPDATE
	ON "FieldApp_valve"
	FOR EACH ROW
	EXECUTE PROCEDURE fai_valve();

--
CREATE OR REPLACE FUNCTION fai_area() RETURNS TRIGGER AS $fai_area$
BEGIN
	INSERT INTO "FieldApp_crop_area_log"
		(log_timestamp, area_id_id, area_ev)
	VALUES
	  (now(), NEW.area_id, NEW.area_ev);
	RETURN new;
END;
$fai_area$ LANGUAGE plpgsql;

CREATE TRIGGER tai_area
	AFTER INSERT OR UPDATE
	ON "FieldApp_crop_area"
	FOR EACH ROW
	EXECUTE PROCEDURE fai_area();

--
CREATE OR REPLACE FUNCTION fai_station() RETURNS TRIGGER AS $fai_station$
BEGIN
	INSERT INTO "FieldApp_weather_station_log"
		(log_timestamp, station_id_id, station_status, station_relative_humidity, station_temperature, station_wind_speed, station_solar_radiation)
	VALUES
	  (now(), NEW.station_id, NEW.station_status, NEW.station_relative_humidity, NEW.station_temperature, NEW.station_wind_speed, NEW.station_solar_radiation);
	RETURN new;
END;
$fai_station$ LANGUAGE plpgsql;

CREATE TRIGGER tai_station
	AFTER INSERT OR UPDATE
	ON "FieldApp_weather_station"
	FOR EACH ROW
	EXECUTE PROCEDURE fai_station();