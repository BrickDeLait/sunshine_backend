
from typing import List
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta

import networkService
import weatherPoint
from openMeteoEndpoint import OpenMeteoEndpoint

def get_weather(latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    current_date = datetime.datetime.now()
    past_date = current_date + relativedelta(years= -30)
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "timezone": 'auto',
        "forecast_hours": 48,
        "forecast_days": 10,
        "current": 'temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,cloud_cover,direct_radiation,wind_speed_10m,wind_direction_10m',
        "hourly": 'temperature_2m,apparent_temperature,precipitation,precipitation_probability,relative_humidity_2m,cloud_cover,direct_radiation,wind_speed_10m,wind_direction_10m',
        "daily": "temperature_2m_max,temperature_2m_min,cloud_cover_mean,temperature_2m_mean,apparent_temperature_mean,precipitation_sum,precipitation_probability_mean,relative_humidity_2m_mean,sunrise,sunset,shortwave_radiation_sum,wind_speed_10m_mean,winddirection_10m_dominant",
    }
    
    try:
        #historical_data = get_historical_weather(
        #    latitude= latitude,
        #    longitude= longitude,
        #    start_date= past_date.strftime("%Y-%m-%d"),
        #    end_date= current_date.strftime("%Y-%m-%d"),
        #)
        data = networkService.request(OpenMeteoEndpoint.FORECAST, params)

        hourly_forecast: List[weatherPoint.WeatherEntry] = []
        for index, value in enumerate(data["hourly"]["time"]):
            hourly_forecast.append(
                weatherPoint.WeatherEntry(
                    date= value,
                    temperature= data["hourly"]["temperature_2m"][index],
                    apparent_temperature= data["hourly"]["apparent_temperature"][index],
                    temperature_min= None,
                    temperature_max= None,
                    precipitation= data["hourly"]["precipitation"][index],
                    precipitation_probability= data["hourly"]["precipitation_probability"][index],
                    humidity= data["hourly"]["relative_humidity_2m"][index],
                    cloud_cover= data["hourly"]["cloud_cover"][index],
                    direct_radiation= data["hourly"]["direct_radiation"][index],
                    wind_speed= data["hourly"]["wind_speed_10m"][index],
                    wind_direction= data["hourly"]["wind_direction_10m"][index],
                    sunrise= None,
                    sunset= None
                )
            )
        
        daily_forecast: List[weatherPoint.WeatherEntry] = []
        for index, value in enumerate(data["daily"]["time"]):
            daily_forecast.append(
                weatherPoint.WeatherEntry(
                    date= value,
                    temperature= data["daily"]["temperature_2m_mean"][index],
                    apparent_temperature= data["daily"]["apparent_temperature_mean"][index],
                    temperature_min= data["daily"]["temperature_2m_min"][index],
                    temperature_max= data["daily"]["temperature_2m_max"][index],
                    precipitation= data["daily"]["precipitation_sum"][index],
                    precipitation_probability= data["daily"]["precipitation_probability_mean"][index],
                    humidity= data["daily"]["relative_humidity_2m_mean"][index],
                    cloud_cover= data["daily"]["cloud_cover_mean"][index],
                    direct_radiation= data["daily"]["shortwave_radiation_sum"][index],
                    wind_speed= data["daily"]["wind_speed_10m_mean"][index],
                    wind_direction= data["daily"]["winddirection_10m_dominant"][index],
                    sunrise= data["daily"]["sunrise"][index],
                    sunset= data["daily"]["sunset"][index]
                )
            )
        return weatherPoint.WeatherPoint(
            latitude= data["latitude"], 
            longitude= data["longitude"],
            timezone_abbreviation= data["timezone_abbreviation"],
            current_weather= weatherPoint.WeatherEntry(
                date= data["current"]["time"],
                temperature= data["current"]["temperature_2m"],
                apparent_temperature= data["current"]["apparent_temperature"],
                temperature_min= data["daily"]["temperature_2m_min"][0],
                temperature_max= data["daily"]["temperature_2m_max"][0],
                precipitation= data["current"]["precipitation"],
                precipitation_probability= None,
                humidity= data["current"]["relative_humidity_2m"],
                cloud_cover= data["current"]["cloud_cover"],
                direct_radiation= data["current"]["direct_radiation"],
                wind_speed= data["current"]["wind_speed_10m"],
                wind_direction= data["current"]["wind_direction_10m"],
                sunrise= None,
                sunset= None
            ),
            hourly_forecast= hourly_forecast,
            daily_forecast= daily_forecast
        )
    except Exception as error:
        print(f"An error occured: {error}")
        raise

def get_historical_weather(latitude: float, longitude: float, start_date: str, end_date: str):
    start_date_formatted = __convertStringToDatetime(start_date).strftime("%Y-%m-%d")
    end_date_formatted = __convertStringToDatetime(end_date).strftime("%Y-%m-%d")
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


def __convertStringToDatetime(date_time) -> datetime.datetime:
    return dateutil.parser.isoparse(date_time)

def __process_historical_data(data) -> weatherPoint.WeatherPoint:
    result: List[weatherPoint.WeatherEntry] = []
    for index, value in enumerate(data["daily"]["time"]):
        result.append(
            weatherPoint.WeatherEntry(
                date= value,
                temperature= data["daily"]["temperature_2m_mean"][index],
                apparent_temperature= None,
                temperature_min= data["daily"]["temperature_2m_min"][index],
                temperature_max= data["daily"]["temperature_2m_max"][index],
                precipitation= data["daily"]["precipitation_sum"][index],
                humidity= None,
                cloud_cover= None,
                direct_radiation= None,
                wind_speed= data["daily"]["wind_speed_10m_max"][index],
                wind_direction= None
            )
        )
    
    climate_normals = get_climatological_normals(result)
        
    return weatherPoint.WeatherPoint(
        data["latitude"],
        data["longitude"],
        climate_normals[0],
        climate_normals[1],
        climate_normals[2],
        result
    )

def get_climatological_normals(data: List[weatherPoint.WeatherEntry]):
    avg_temp_min_sum = 0
    avg_temp_max_sum = 0
    avg_precipitation_sum = 0
    data_length = len(data)

    for value in data:
        avg_temp_min_sum += value.temperature_min
        avg_temp_max_sum += value.temperature_max
        avg_precipitation_sum += value.precipitation
    
    avg_temp_min = avg_temp_min_sum/data_length
    avg_temp_max = avg_temp_max_sum/data_length
    avg_precipitation = avg_precipitation_sum/data_length
    return (avg_temp_min, avg_temp_max, avg_precipitation)