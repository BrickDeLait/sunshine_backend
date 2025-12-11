
import networkService
import weatherPoint
from openMeteoEndpoint import OpenMeteoEndpoint

import datetime
import dateutil.parser
from typing import List

def get_current_weather(latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "current": 'temperature_2m,wind_speed_10m,precipitation'
    }
    try:
        data = networkService.request(OpenMeteoEndpoint.FORECAST, params)
        return weatherPoint.WeatherPoint(
            data["latitude"], 
            data["longitude"],
            [
                weatherPoint.WeatherEntry(
                    date= data["current"]["time"],
                    temperature= data["current"]["temperature_2m"],
                    wind_speed= data["current"]["wind_speed_10m"],
                    temperature_min= None,
                    temperature_max= None,
                    precipitation_sum= data["current"]["precipitation"]
                )
            ]
        )
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
        "daily": "temperature_2m_mean,wind_speed_10m_max,temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "auto"
    }
    try:
        data = networkService.request(OpenMeteoEndpoint.HISTORICAL, params)
        return __process_historical_data(data)
    except Exception as error:
        print(f"An error occured: {error}")
        raise

def __convert(date_time) -> datetime.datetime:
    return dateutil.parser.isoparse(date_time)

def __process_historical_data(data) -> weatherPoint.WeatherPoint:
    result: List[weatherPoint.WeatherEntry] = []
    for index, value in enumerate(data["daily"]["time"]):
        result.append(
            weatherPoint.WeatherEntry(
                date= value,
                temperature= data["daily"]["temperature_2m_mean"][index],
                wind_speed= data["daily"]["wind_speed_10m_max"][index],
                temperature_min= data["daily"]["temperature_2m_min"][index],
                temperature_max= data["daily"]["temperature_2m_max"][index],
                precipitation_sum= data["daily"]["precipitation_sum"][index]
            )
        )
        
    return weatherPoint.WeatherPoint(
        data["latitude"],
        data["longitude"],
        result
    )