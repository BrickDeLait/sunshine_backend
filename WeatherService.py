
import networkService
import weatherPoint
from openMeteoEndpoint import OpenMeteoEndpoint

import datetime
import dateutil.parser

def get_current_weather(latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "current": 'temperature_2m,wind_speed_10m'
    }
    try:
        data = networkService.request(OpenMeteoEndpoint.FORECAST, params)
        return weatherPoint.WeatherPoint(data["latitude"], data["longitude"], data["current"]["temperature_2m"], data["current"]["wind_speed_10m"])
    except Exception as error:
        print(f"An error occured: {error}")
        raise

def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    start_date_formatted = __convert(start_date).strftime("%Y-%m-%d")
    end_date_formatted = __convert(end_date).strftime("%Y-%m-%d")
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "start_date": start_date_formatted,
        "end_date": end_date_formatted,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }
    try:
        data = networkService.request(OpenMeteoEndpoint.HISTORICAL, params)
        return weatherPoint.HistoricalWeatherPoint(
            data["latitude"],
            data["longitude"],
            data["daily"]["temperature_2m_max"],
            data["daily"]["temperature_2m_min"],
            data["daily"]["precipitation_sum"])
    except Exception as error:
        print(f"An error occured: {error}")
        raise

def __convert(date_time) -> datetime.datetime:
    return dateutil.parser.isoparse(date_time)