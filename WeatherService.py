
from typing import List
import datetime
import dateutil.parser

import networkService
from DataModels import weatherPoint, climatePoint
import openMeteoEndpoint

def get_current_weather(latitude: float, longitude: float) -> weatherPoint.WeatherPoint:
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "timezone": 'auto',
        "current": 'temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,cloud_cover,direct_radiation,wind_speed_10m,wind_direction_10m',
        "daily": "temperature_2m_min,temperature_2m_max",
        }
    
    try:
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
    
def get_climate_normals(latitude: float, longitude: float) -> climatePoint.ClimatePoint:
    reference_from_date = "1991-01-01"
    reference_to_date = "2020-12-31"

    try:
        historical_data = get_historical_weather(
            latitude= latitude,
            longitude= longitude,
            start_date= reference_from_date,
            end_date= reference_to_date,
        )
        print(f"data returned from climate API at : {datetime.datetime.now()}")
        return climatePoint.ClimatePoint(
            latitude,
            longitude,
            __process_historical_data(historical_data)
        )
    except Exception as error:
        message= f"An error occured in get_climate_normals: {error}"
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
        "daily": "temperature_2m_mean,precipitation_sum,sunshine_duration",
        "timezone": "auto"
    }
    try:
        data = networkService.request(openMeteoEndpoint.OpenMeteoEndpoint.HISTORICAL, params)
        return data
    except Exception as error:
        message= f"An error occured in get_historical_weather: {error}"
        print(message)
        raise openMeteoEndpoint.WeatherServiceError(500, message)


def __convertStringToDatetime(date_time) -> datetime.datetime:
    return dateutil.parser.isoparse(date_time)

def __process_historical_data(data) -> List[climatePoint.ClimateNormal]:
    result: List[climatePoint.ClimateNormal] = []
    for index, value in enumerate(data["daily"]["time"]):
        result.append(
            climatePoint.ClimateNormal(
                date= value,
                temperature= data["daily"]["temperature_2m_mean"][index],
                precipitation= data["daily"]["precipitation_sum"][index],
                sunshine_duration= data["daily"]["sunshine_duration"][index]
            )
        )
        
    print(f"Finished processing data at : {datetime.datetime.now()}")
    return result
