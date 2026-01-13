
from typing import List
import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta

import networkService
import weatherPoint
import openMeteoEndpoint

def get_current_weather(latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "timezone": 'auto',
        "current": 'temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,cloud_cover,direct_radiation,wind_speed_10m,wind_direction_10m'
        }
    
    try:

        #current_date = datetime.datetime.now()
        #past_date = current_date + relativedelta(years= -30)
        #historical_data = get_historical_weather(
        #    latitude= latitude,
        #    longitude= longitude,
        #    start_date= past_date.strftime("%Y-%m-%d"),
        #    end_date= current_date.strftime("%Y-%m-%d"),
        #)
        data = networkService.request(openMeteoEndpoint.OpenMeteoEndpoint.FORECAST, params)

        return weatherPoint.WeatherPoint(
            latitude= data["latitude"], 
            longitude= data["longitude"],
            timezone_abbreviation= data["timezone_abbreviation"],
            weather= [
                weatherPoint.WeatherEntry(
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
                )
            ]
        )
    except Exception as error:
        message= f"An error occured in get_current_weather: {error}"
        print(message)
        raise openMeteoEndpoint.WeatherServiceError(500, message)

def get_forecast(forecast_type: openMeteoEndpoint.OpenMeteoForecastType, latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    base_params = {
        "latitude": latitude, 
        "longitude": longitude,
        "timezone": 'auto'
    }
    params = base_params | forecast_type.query_params

    try:
        data = networkService.request(openMeteoEndpoint.OpenMeteoEndpoint.FORECAST, params)

        forecast: List[weatherPoint.WeatherEntry] = []
        for index, value in enumerate(data[forecast_type.dict_key]["time"]):
            forecast.append(
                forecast_type.get_weather_entry(value, index, data)
            )
        
        return weatherPoint.WeatherPoint(
            latitude= data["latitude"], 
            longitude= data["longitude"],
            timezone_abbreviation= data["timezone_abbreviation"],
            weather= forecast
        )    
    except Exception as error:
        message= f"An error occured in get_forecast: {error}"
        print(message)
        raise openMeteoEndpoint.WeatherServiceError(500, message)

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