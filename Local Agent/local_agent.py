from models import Moisture_Agent, Moisture_Event, Weather_Data
import json

agent = Moisture_Agent()

#reading the moisture log file
events_rows = agent.read_file('moisture_log.csv')
events = []

#reading the weather data file
weather_rows = agent.read_file('weather_data_log.csv')
weather_data = []

#processing the event data
for row in events_rows:
    event = Moisture_Event(row[0], row[1], row[2], row[3], row[4])
    events.append(event)

#processing the weather data
for weather_row in weather_rows:
    weather_info = Weather_Data(weather_row[0], weather_row[1], weather_row[2], weather_row[3],
                                weather_row[4], weather_row[5], weather_row[6],weather_row[7])
    print weather_info.to_JSON()


